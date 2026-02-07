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
Standalone build workflow — implements a plan created by plan.py.

Reads state from a previous plan.py run (via --run-id or stdin pipe)
and executes the implementation using implement.md.

Usage:
    # With explicit run-id
    uv run agentic/workflows/build.py --run-id abc12345

    # Piped from plan.py
    uv run agentic/workflows/plan.py "fix the bug" | uv run agentic/workflows/build.py

    # With plan file directly (no prior state needed)
    uv run agentic/workflows/build.py --plan-file agentic/specs/260205-fix-api.md
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

from agent import OUTPUT_JSONL, SUMMARY_JSON, AgentPromptRequest, prompt_claude_code_with_retry
from state import resolve_state
from template import load_template, render_template


# Template path
IMPLEMENT_TEMPLATE = "agentic/commands/implement.md"

# Usage hint for resolve_state error message
BUILD_USAGE_HINT = (
    "  uv run agentic/workflows/build.py --run-id <id>\n"
    '  uv run agentic/workflows/plan.py "task" | uv run agentic/workflows/build.py\n'
    "  uv run agentic/workflows/build.py --plan-file agentic/specs/260205-fix-api.md"
)


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous plan.py execution")
@click.option("--plan-file", default=None, type=click.Path(), help="Path to plan file directly (creates new run)")
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
def main(run_id: str, plan_file: str, model: str, working_dir: str, cli: str):
    """Implement a plan created by plan.py."""
    # Detect piping: Rich to stderr, JSON state to stdout
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    # ── Resolve state ───────────────────────────────────────────────
    state = resolve_state(run_id, working_dir, console, plan_file=plan_file, usage_hint=BUILD_USAGE_HINT)

    # Verify plan file
    plan_path = state.plan_file
    if not plan_path:
        console.print("[bold red]No plan_file in state. Run plan.py first.[/bold red]")
        sys.exit(1)

    plan_full_path = os.path.join(working_dir, plan_path)
    if not os.path.exists(plan_full_path):
        console.print(f"[bold red]Plan file not found: {plan_full_path}[/bold red]")
        sys.exit(1)

    # ── Configuration ───────────────────────────────────────────────
    console.print(
        Panel(
            f"[bold blue]Build Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]Task Type:[/cyan] {state.task_type or 'unknown'}\n"
            f"[cyan]Plan:[/cyan] {plan_path}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}",
            title="[bold blue]Build Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Implementation ──────────────────────────────────────────────
    console.print(Rule("[bold yellow]Implementation (implement.md)[/bold yellow]"))
    console.print()

    # Read plan content
    with open(plan_full_path, "r") as f:
        plan_content = f.read()

    # Render implement template
    try:
        implement_template = load_template(IMPLEMENT_TEMPLATE, working_dir)
    except FileNotFoundError as e:
        console.print(Panel(str(e), title="[bold red]Template Error[/bold red]", border_style="red"))
        sys.exit(2)

    implement_prompt = render_template(implement_template, {"ARGUMENTS": plan_content})

    # Create output directory
    builder_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/builder")
    os.makedirs(builder_output_dir, exist_ok=True)

    implement_request = AgentPromptRequest(
        prompt=implement_prompt,
        run_id=state.run_id,
        agent_name="builder",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(builder_output_dir, OUTPUT_JSONL),
        working_dir=working_dir,
    )

    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()
    info_table.add_row("Plan File", plan_path)
    info_table.add_row("Model", model)
    info_table.add_row("Agent", "builder")

    console.print(Panel(info_table, title="[bold blue]Builder Inputs[/bold blue]", border_style="blue"))
    console.print()

    with console.status("[bold yellow]Implementing plan...[/bold yellow]"):
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

    # Save summary
    with open(os.path.join(builder_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "implementation",
                "run_id": state.run_id,
                "plan_path": plan_path,
                "model": model,
                "success": response.success,
                "session_id": response.session_id,
                "output": response.output,
            },
            f,
            indent=2,
        )

    # Save state
    state.save(working_dir, phase="build")
    console.print(f"\n[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    # Output state for potential further piping
    if is_piped:
        state.to_stdout()

    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()
