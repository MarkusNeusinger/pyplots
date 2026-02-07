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
Standalone pull request workflow — pushes branch and creates a PR.

Reads state from a previous workflow run and uses pull_request.md to
generate a structured PR with summary, plan reference, and test plan.

Usage:
    # With run-id from a previous commit
    uv run agentic/workflows/pull_request.py --run-id abc12345

    # Piped from commit.py
    uv run agentic/workflows/commit.py --run-id abc12345 | uv run agentic/workflows/pull_request.py
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
PR_TEMPLATE = "agentic/commands/pull_request.md"

# Usage hint for resolve_state error message
PR_USAGE_HINT = (
    "  uv run agentic/workflows/pull_request.py --run-id <id>\n"
    "  uv run agentic/workflows/commit.py --run-id <id> | uv run agentic/workflows/pull_request.py"
)


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous workflow execution")
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="medium",
    help="Model tier for PR creation (default: medium)",
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
    """Push branch and create a pull request."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    state = resolve_state(run_id, working_dir, console, usage_hint=PR_USAGE_HINT)

    console.print(
        Panel(
            f"[bold blue]Pull Request Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]Plan:[/cyan] {state.plan_file or '(none)'}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}",
            title="[bold blue]PR Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Create PR ────────────────────────────────────────────────────
    console.print(Rule("[bold yellow]Creating Pull Request[/bold yellow]"))
    console.print()

    template = load_template(PR_TEMPLATE, working_dir)
    pr_prompt = render_template(template, {"1": state.run_id, "2": state.plan_file or ""})

    pr_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/pr_creator")
    os.makedirs(pr_output_dir, exist_ok=True)

    request = AgentPromptRequest(
        prompt=pr_prompt,
        run_id=state.run_id,
        agent_name="pr_creator",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(pr_output_dir, OUTPUT_JSONL),
        working_dir=working_dir,
    )

    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()
    info_table.add_row("Template", PR_TEMPLATE)
    info_table.add_row("Plan File", state.plan_file or "(none)")
    info_table.add_row("Model", model)

    console.print(Panel(info_table, title="[bold blue]PR Creator Inputs[/bold blue]", border_style="blue"))
    console.print()

    with console.status("[bold yellow]Creating pull request...[/bold yellow]"):
        response = prompt_claude_code_with_retry(request, max_retries=2)

    if response.success:
        pr_url = response.output.strip()
        console.print(
            Panel(
                pr_url,
                title="[bold green]Pull Request Created[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
        )
    else:
        console.print(
            Panel(response.output, title="[bold red]PR Creation Failed[/bold red]", border_style="red", padding=(1, 2))
        )
        pr_url = None

    # ── Summary ──────────────────────────────────────────────────────
    console.print()

    # Update state
    if pr_url:
        state.update(pr_url=pr_url)
    state.save(working_dir, phase="pull_request")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    # Save summary
    with open(os.path.join(pr_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(
            {
                "phase": "pull_request",
                "run_id": state.run_id,
                "success": response.success,
                "session_id": response.session_id,
                "pr_url": pr_url,
            },
            f,
            indent=2,
        )

    if is_piped:
        state.to_stdout()

    sys.exit(0 if response.success else 1)


if __name__ == "__main__":
    main()
