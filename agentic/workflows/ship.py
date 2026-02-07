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
Ship workflow — commits changes and creates a pull request.

Combines the commit and pull-request steps into a single phase.
Reads state from a previous workflow run, stages + commits, then
pushes the branch and opens a PR.

Usage:
    # With run-id from a previous build/review
    uv run agentic/workflows/ship.py --run-id abc12345

    # Piped from document.py
    uv run agentic/workflows/document.py --run-id abc12345 | uv run agentic/workflows/ship.py
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


# Template paths
COMMIT_TEMPLATE = "agentic/commands/commit.md"
PR_TEMPLATE = "agentic/commands/pull_request.md"

# Usage hint for resolve_state error message
SHIP_USAGE_HINT = (
    "  uv run agentic/workflows/ship.py --run-id <id>\n"
    "  uv run agentic/workflows/document.py --run-id <id> | uv run agentic/workflows/ship.py"
)


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous workflow execution")
@click.option(
    "--model", type=click.Choice(["small", "medium", "large"]), default="large", help="Model tier (default: large)"
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
    """Commit changes and create a pull request."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    state = resolve_state(run_id, working_dir, console, usage_hint=SHIP_USAGE_HINT)

    console.print(
        Panel(
            f"[bold blue]Ship Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]Task Type:[/cyan] {state.task_type or '(auto-detect)'}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}",
            title="[bold blue]Ship Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Step 1: Commit ────────────────────────────────────────────────
    console.print(Rule("[bold yellow]Step 1: Creating Commit[/bold yellow]"))
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
        commit_response = prompt_claude_code_with_retry(request, max_retries=2)

    if commit_response.success:
        commit_message = commit_response.output.strip()
        console.print(
            Panel(commit_message, title="[bold green]Commit Created[/bold green]", border_style="green", padding=(1, 2))
        )
    else:
        console.print(
            Panel(
                commit_response.output, title="[bold red]Commit Failed[/bold red]", border_style="red", padding=(1, 2)
            )
        )
        commit_message = None

    # Save commit summary
    with open(os.path.join(committer_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "commit",
                "run_id": state.run_id,
                "success": commit_response.success,
                "session_id": commit_response.session_id,
                "commit_message": commit_message,
            },
            f,
            indent=2,
        )

    if commit_message:
        state.update(commit_message=commit_message)

    if not commit_response.success:
        console.print()
        console.print("[bold red]Commit failed. Aborting ship.[/bold red]")
        state.save(working_dir, phase="ship")
        sys.exit(1)

    console.print()

    # ── Step 2: Pull Request ──────────────────────────────────────────
    console.print(Rule("[bold yellow]Step 2: Creating Pull Request[/bold yellow]"))
    console.print()

    pr_template = load_template(PR_TEMPLATE, working_dir)
    pr_prompt = render_template(pr_template, {"1": state.run_id, "2": state.plan_file or ""})

    pr_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/pr_creator")
    os.makedirs(pr_output_dir, exist_ok=True)

    pr_request = AgentPromptRequest(
        prompt=pr_prompt,
        run_id=state.run_id,
        agent_name="pr_creator",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(pr_output_dir, OUTPUT_JSONL),
        working_dir=working_dir,
    )

    pr_info_table = Table(show_header=False, box=None, padding=(0, 1))
    pr_info_table.add_column(style="bold cyan")
    pr_info_table.add_column()
    pr_info_table.add_row("Template", PR_TEMPLATE)
    pr_info_table.add_row("Plan File", state.plan_file or "(none)")
    pr_info_table.add_row("Model", model)

    console.print(Panel(pr_info_table, title="[bold blue]PR Creator Inputs[/bold blue]", border_style="blue"))
    console.print()

    with console.status("[bold yellow]Creating pull request...[/bold yellow]"):
        pr_response = prompt_claude_code_with_retry(pr_request, max_retries=2)

    if pr_response.success:
        pr_url = pr_response.output.strip()
        console.print(
            Panel(pr_url, title="[bold green]Pull Request Created[/bold green]", border_style="green", padding=(1, 2))
        )
    else:
        console.print(
            Panel(
                pr_response.output, title="[bold red]PR Creation Failed[/bold red]", border_style="red", padding=(1, 2)
            )
        )
        pr_url = None

    # Save PR summary
    with open(os.path.join(pr_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "pull_request",
                "run_id": state.run_id,
                "success": pr_response.success,
                "session_id": pr_response.session_id,
                "pr_url": pr_url,
            },
            f,
            indent=2,
        )

    if pr_url:
        state.update(pr_url=pr_url)

    # ── Final state ───────────────────────────────────────────────────
    console.print()
    state.save(working_dir, phase="ship")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    if is_piped:
        state.to_stdout()

    sys.exit(0 if pr_response.success else 1)


if __name__ == "__main__":
    main()
