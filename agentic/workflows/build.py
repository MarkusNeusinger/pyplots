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

import os
import sys
import json
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agent import AgentPromptRequest, prompt_claude_code_with_retry, generate_short_id
from state import WorkflowState

# Output file names
OUTPUT_JSONL = "cli_raw_output.jsonl"
SUMMARY_JSON = "cli_summary_output.json"

# Template path
IMPLEMENT_TEMPLATE = "agentic/commands/implement.md"


def load_template(template_path: str, working_dir: str) -> str:
    """Load a template file from the working directory."""
    full_path = os.path.join(working_dir, template_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Template not found: {full_path}")
    with open(full_path, "r") as f:
        return f.read()


def render_template(template: str, variables: dict) -> str:
    """Render a template by replacing $1, $2, $ARGUMENTS variables."""
    result = template
    for key, value in variables.items():
        if key.isdigit():
            result = result.replace(f"${key}", str(value))
    if "ARGUMENTS" in variables:
        result = result.replace("$ARGUMENTS", str(variables["ARGUMENTS"]))
    return result


def resolve_state(run_id: str, plan_file: str, working_dir: str, console: Console) -> WorkflowState:
    """Resolve state from --run-id, stdin pipe, or --plan-file.

    Priority:
        1. --run-id  → load from agentic/runs/{run_id}/state.json
        2. stdin     → piped JSON from plan.py
        3. --plan-file → create minimal state with just the plan path
    """
    # Priority 1: explicit run-id
    if run_id:
        state = WorkflowState.load(run_id, working_dir)
        if not state:
            console.print(f"[bold red]No state found for run-id: {run_id}[/bold red]")
            console.print(f"Expected: agentic/runs/{run_id}/state.json")
            console.print("\nRun plan.py first to create a plan and state.")
            sys.exit(1)
        return state

    # Priority 2: piped stdin from plan.py
    state = WorkflowState.from_stdin()
    if state:
        return state

    # Priority 3: direct plan file (no prior state)
    if plan_file:
        new_run_id = generate_short_id()
        state = WorkflowState(run_id=new_run_id, prompt="(from plan file)")
        state.update(plan_file=plan_file)
        return state

    # No state source
    console.print("[bold red]No state source provided.[/bold red]")
    console.print("\nUsage:")
    console.print("  uv run agentic/workflows/build.py --run-id <id>")
    console.print('  uv run agentic/workflows/plan.py "task" | uv run agentic/workflows/build.py')
    console.print("  uv run agentic/workflows/build.py --plan-file agentic/specs/260205-fix-api.md")
    sys.exit(1)


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
    state = resolve_state(run_id, plan_file, working_dir, console)

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
