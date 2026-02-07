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
Standalone commit workflow — stages changes and creates a conventional commit.

Reads state from a previous workflow run and uses commit.md to generate
a properly formatted commit message.

Usage:
    # With run-id from a previous build/review
    uv run agentic/workflows/commit.py --run-id abc12345

    # Piped from document.py
    uv run agentic/workflows/document.py --run-id abc12345 | uv run agentic/workflows/commit.py
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
COMMIT_TEMPLATE = "agentic/commands/commit.md"

# Usage hint for resolve_state error message
COMMIT_USAGE_HINT = (
    "  uv run agentic/workflows/commit.py --run-id <id>\n"
    "  uv run agentic/workflows/document.py --run-id <id> | uv run agentic/workflows/commit.py"
)


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous workflow execution")
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="medium",
    help="Model tier for commit (default: medium)",
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
def main(run_id: str, model: str, working_dir: str, cli: str):
    """Create a conventional commit from staged changes."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    state = resolve_state(run_id, working_dir, console, usage_hint=COMMIT_USAGE_HINT)

    console.print(
        Panel(
            f"[bold blue]Commit Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]Task Type:[/cyan] {state.task_type or '(auto-detect)'}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}",
            title="[bold blue]Commit Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Generate commit ──────────────────────────────────────────────
    console.print(Rule("[bold yellow]Creating Commit[/bold yellow]"))
    console.print()

    template = load_template(COMMIT_TEMPLATE, working_dir)
    commit_prompt = render_template(template, {"1": state.run_id, "2": state.task_type or ""})

    committer_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/committer")
    os.makedirs(committer_output_dir, exist_ok=True)

    request = AgentPromptRequest(
        prompt=commit_prompt,
        run_id=state.run_id,
        agent_name="committer",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(committer_output_dir, OUTPUT_JSONL),
        working_dir=working_dir,
    )

    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()
    info_table.add_row("Template", COMMIT_TEMPLATE)
    info_table.add_row("Task Type", state.task_type or "(auto-detect)")
    info_table.add_row("Model", model)

    console.print(Panel(info_table, title="[bold blue]Committer Inputs[/bold blue]", border_style="blue"))
    console.print()

    with console.status("[bold yellow]Creating commit...[/bold yellow]"):
        response = prompt_claude_code_with_retry(request, max_retries=2)

    if response.success:
        commit_message = response.output.strip()
        console.print(
            Panel(
                commit_message,
                title="[bold green]Commit Created[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        console.print(
            Panel(response.output, title="[bold red]Commit Failed[/bold red]", border_style="red", padding=(1, 2))
        )
        commit_message = None

    # ── Summary ──────────────────────────────────────────────────────
    console.print()

    # Update state
    if commit_message:
        state.update(commit_message=commit_message)
    state.save(working_dir, phase="commit")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    # Save summary
    with open(os.path.join(committer_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "commit",
                "run_id": state.run_id,
                "success": response.success,
                "session_id": response.session_id,
                "commit_message": commit_message,
            },
            f,
            indent=2,
        )

    if is_piped:
        state.to_stdout()

    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()
