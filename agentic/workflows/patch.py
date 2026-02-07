#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pydantic",
#   "pydantic-settings",
#   "python-dotenv",
#   "click",
#   "rich",
# ]
# ///
"""
Lightweight patch workflow — skip planning, implement directly.

For quick fixes and small changes that don't need a full plan phase.
Optionally runs test and review after implementation.

Usage:
    # Quick patch (implement only)
    uv run agentic/workflows/patch.py "Fix the typo in README.md"

    # Patch with tests
    uv run agentic/workflows/patch.py "Fix the 404 error" --test

    # Patch with test + review
    uv run agentic/workflows/patch.py "Update the API response format" --test --review

    # Full patch pipeline (test + review)
    uv run agentic/workflows/patch.py "Add input validation" --test --review --model large
"""

import json
import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table


# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agent import OUTPUT_JSONL, SUMMARY_JSON, AgentPromptRequest, generate_short_id, prompt_claude_code_with_retry
from state import WorkflowState
from template import load_template, render_template


# Template path
IMPLEMENT_TEMPLATE = "agentic/commands/implement.md"


@click.command()
@click.argument("prompt", required=True)
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="large",
    help="Model tier for implementation (default: large)",
)
@click.option(
    "--working-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Working directory (default: current directory)",
)
@click.option(
    "--cli",
    type=click.Choice(["claude", "copilot", "gemini"]),
    default="claude",
    help="CLI tool to use (default: claude)",
)
@click.option("--test", "run_test", is_flag=True, help="Run tests after implementation")
@click.option("--review", "run_review", is_flag=True, help="Run review after implementation")
def main(prompt: str, model: str, working_dir: str, cli: str, run_test: bool, run_review: bool):
    """Implement a quick patch without planning."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    run_id = generate_short_id()

    if not working_dir:
        working_dir = os.getcwd()

    state = WorkflowState(run_id=run_id, prompt=prompt)
    state.update(task_type="patch")

    # ── Configuration ───────────────────────────────────────────────
    phases = ["Implement"]
    if run_test:
        phases.append("Test")
    if run_review:
        phases.append("Review")

    console.print(
        Panel(
            f"[bold blue]Patch Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {run_id}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Phases:[/cyan] {' → '.join(phases)}\n"
            f"[cyan]Prompt:[/cyan] {prompt}",
            title="[bold blue]Patch Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Phase 1: Implement directly ─────────────────────────────────
    console.print(Rule("[bold yellow]Phase 1: Implementation (implement.md)[/bold yellow]"))
    console.print()

    try:
        implement_template = load_template(IMPLEMENT_TEMPLATE, working_dir)
    except FileNotFoundError as e:
        console.print(Panel(str(e), title="[bold red]Template Error[/bold red]", border_style="red"))
        sys.exit(2)

    # Use the prompt directly as the plan content
    implement_prompt = render_template(implement_template, {"ARGUMENTS": prompt})

    patcher_output_dir = os.path.join(working_dir, f"agentic/runs/{run_id}/patcher")
    os.makedirs(patcher_output_dir, exist_ok=True)

    implement_request = AgentPromptRequest(
        prompt=implement_prompt,
        run_id=run_id,
        agent_name="patcher",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(patcher_output_dir, OUTPUT_JSONL),
        working_dir=working_dir,
    )

    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()
    info_table.add_row("Template", IMPLEMENT_TEMPLATE)
    info_table.add_row("Model", model)
    info_table.add_row("Agent", "patcher")

    console.print(Panel(info_table, title="[bold blue]Patcher Inputs[/bold blue]", border_style="blue"))
    console.print()

    with console.status("[bold yellow]Implementing patch...[/bold yellow]"):
        response = prompt_claude_code_with_retry(implement_request)

    if response.success:
        console.print(
            Panel(
                response.output,
                title="[bold green]Implementation Success[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        console.print(
            Panel(
                response.output, title="[bold red]Implementation Failed[/bold red]", border_style="red", padding=(1, 2)
            )
        )
        state.save(working_dir, phase="patch")
        if is_piped:
            state.to_stdout()
        sys.exit(1)

    # Save implementation summary
    with open(os.path.join(patcher_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "patch_implementation",
                "run_id": run_id,
                "model": model,
                "success": response.success,
                "session_id": response.session_id,
                "output": response.output,
            },
            f,
            indent=2,
        )

    state.save(working_dir, phase="patch")

    # ── Phase 2: Test (optional) ────────────────────────────────────
    test_rc = 0
    if run_test:
        console.print()
        console.print(Rule("[bold yellow]Phase 2: Test (with auto-fix)[/bold yellow]"))
        console.print()

        from orchestrator import run_phase

        test_args = ["--run-id", run_id, "--model", model, "--cli", cli]
        if working_dir:
            test_args.extend(["--working-dir", working_dir])

        test_rc, _ = run_phase("test.py", test_args, console, "Test")

        if test_rc != 0:
            console.print("[bold yellow]Tests failed, continuing.[/bold yellow]")

    # ── Phase 3: Review (optional) ──────────────────────────────────
    review_rc = 0
    if run_review:
        console.print()
        phase_num = 3 if run_test else 2
        console.print(Rule(f"[bold yellow]Phase {phase_num}: Review[/bold yellow]"))
        console.print()

        from orchestrator import run_phase

        review_args = ["--run-id", run_id, "--model", model, "--cli", cli]
        if working_dir:
            review_args.extend(["--working-dir", working_dir])

        review_rc, review_stdout = run_phase("review.py", review_args, console, "Review", capture_stdout=is_piped)

    # ── Summary ─────────────────────────────────────────────────────
    console.print()
    console.print(Rule("[bold blue]Patch Summary[/bold blue]"))
    console.print()

    results = [("Implement", 0)]
    if run_test:
        results.append(("Test", test_rc))
    if run_review:
        results.append(("Review", review_rc))

    for name, rc in results:
        status = "[green]PASS[/green]" if rc == 0 else "[red]FAIL[/red]"
        console.print(f"  {name}: {status}")

    console.print()
    console.print(f"[bold cyan]Run ID:[/bold cyan] {run_id}")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{run_id}/state.json")

    if is_piped:
        state.to_stdout()

    # Implementation failure is fatal, test/review failures are not
    final_rc = test_rc or review_rc
    sys.exit(final_rc)


if __name__ == "__main__":
    main()
