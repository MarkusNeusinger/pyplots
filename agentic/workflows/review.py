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
Standalone review workflow with automatic blocker resolution.

Runs the review.md template against a spec file, parses results,
and for each blocker spawns an inline-prompt agent to fix the issue.
Retries up to 5 times.

Usage:
    # With run-id from a previous build
    uv run agentic/workflows/review.py --run-id abc12345

    # Piped from test.py
    uv run agentic/workflows/test.py --run-id abc12345 | uv run agentic/workflows/review.py
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

from agent import (
    OUTPUT_JSONL,
    SUMMARY_JSON,
    AgentPromptRequest,
    ReviewIssue,
    ReviewResult,
    parse_json,
    prompt_claude_code_with_retry,
)
from state import WorkflowState, resolve_state
from template import load_template, render_template


# Template paths
REVIEW_TEMPLATE = "agentic/commands/review.md"
IMPLEMENT_TEMPLATE = "agentic/commands/implement.md"

# Retry configuration
MAX_REVIEW_RETRY_ATTEMPTS = 5

# Usage hint for resolve_state error message
REVIEW_USAGE_HINT = (
    "  uv run agentic/workflows/review.py --run-id <id>\n"
    "  uv run agentic/workflows/test.py --run-id <id> | uv run agentic/workflows/review.py"
)


def run_review(
    state: WorkflowState, working_dir: str, model: str, cli: str, console: Console, attempt: int
) -> ReviewResult | None:
    """Run review.md template and parse results into ReviewResult."""
    template = load_template(REVIEW_TEMPLATE, working_dir)

    # Find spec file from state
    spec_file = state.plan_file or ""

    review_prompt = render_template(template, {"1": state.run_id, "2": spec_file, "3": "reviewer"})

    reviewer_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/reviewer")
    os.makedirs(reviewer_output_dir, exist_ok=True)

    output_file = os.path.join(
        reviewer_output_dir, f"cli_raw_output_attempt{attempt}.jsonl" if attempt > 0 else OUTPUT_JSONL
    )

    request = AgentPromptRequest(
        prompt=review_prompt,
        run_id=state.run_id,
        agent_name="reviewer",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=output_file,
        working_dir=working_dir,
    )

    with console.status(
        f"[bold yellow]Running review (attempt {attempt + 1}/{MAX_REVIEW_RETRY_ATTEMPTS})...[/bold yellow]"
    ):
        response = prompt_claude_code_with_retry(request)

    if not response.success:
        console.print(Panel(response.output, title="[bold red]Review Execution Failed[/bold red]", border_style="red"))
        return None

    try:
        result = parse_json(response.output, ReviewResult)
        if isinstance(result, list):
            result = result[0]
        return result
    except (json.JSONDecodeError, ValueError) as e:
        console.print(
            Panel(
                f"Failed to parse review output: {e}\n\nRaw output:\n{response.output[:500]}",
                title="[bold red]Parse Error[/bold red]",
                border_style="red",
            )
        )
        return None


def resolve_blocker(
    issue: ReviewIssue, state: WorkflowState, working_dir: str, model: str, cli: str, console: Console, fix_index: int
) -> bool:
    """Attempt to fix a blocker issue using implement.md template."""
    fix_prompt = (
        f"Fix this blocking review issue:\n\nIssue: {issue.issue_description}\nResolution: {issue.issue_resolution}\n"
    )

    # Use implement.md template with the fix as $ARGUMENTS
    try:
        implement_template = load_template(IMPLEMENT_TEMPLATE, working_dir)
        full_prompt = render_template(implement_template, {"ARGUMENTS": fix_prompt})
    except FileNotFoundError:
        # Fallback to inline prompt if implement.md not available
        full_prompt = fix_prompt

    fixer_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/reviewer/fixes")
    os.makedirs(fixer_output_dir, exist_ok=True)

    request = AgentPromptRequest(
        prompt=full_prompt,
        run_id=state.run_id,
        agent_name="reviewer",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(fixer_output_dir, f"fix_{fix_index}.jsonl"),
        working_dir=working_dir,
    )

    console.print(f"  Fixing blocker #{issue.review_issue_number}...")
    response = prompt_claude_code_with_retry(request, max_retries=1)
    return response.success


def display_review_result(result: ReviewResult, console: Console) -> int:
    """Display review results and return blocker count."""
    if result.success:
        console.print(
            Panel(result.review_summary, title="[bold green]Review Passed[/bold green]", border_style="green")
        )
    else:
        console.print(Panel(result.review_summary, title="[bold red]Review Failed[/bold red]", border_style="red"))

    blocker_count = 0
    if result.review_issues:
        table = Table(show_header=True, box=None)
        table.add_column("#", style="bold")
        table.add_column("Severity")
        table.add_column("Description")

        for issue in result.review_issues:
            severity_style = {
                "blocker": "[red]blocker[/red]",
                "tech_debt": "[yellow]tech_debt[/yellow]",
                "skippable": "[dim]skippable[/dim]",
            }.get(issue.issue_severity, issue.issue_severity)

            if issue.issue_severity == "blocker":
                blocker_count += 1

            table.add_row(str(issue.review_issue_number), severity_style, issue.issue_description[:80])

        console.print(table)

    console.print(f"\n  Blockers: [red]{blocker_count}[/red]")
    return blocker_count


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous plan/build/test execution")
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="large",
    help="Model tier for review (default: large)",
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
    """Review implementation against spec with blocker auto-fix."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    state = resolve_state(run_id, working_dir, console, usage_hint=REVIEW_USAGE_HINT)

    console.print(
        Panel(
            f"[bold blue]Review Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]Spec:[/cyan] {state.plan_file or '(auto-detect)'}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Max Retries:[/cyan] {MAX_REVIEW_RETRY_ATTEMPTS}",
            title="[bold blue]Review Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Review retry loop ──────────────────────────────────────────
    review_success = False
    final_result = None
    fix_index = 0

    for attempt in range(MAX_REVIEW_RETRY_ATTEMPTS):
        console.print(Rule(f"[bold yellow]Review {attempt + 1}/{MAX_REVIEW_RETRY_ATTEMPTS}[/bold yellow]"))
        console.print()

        result = run_review(state, working_dir, model, cli, console, attempt)
        final_result = result

        if result is None:
            console.print("[bold red]No review result returned.[/bold red]")
            break

        blocker_count = display_review_result(result, console)
        console.print()

        if result.success or blocker_count == 0:
            review_success = True
            break

        # Last attempt — don't try to fix
        if attempt == MAX_REVIEW_RETRY_ATTEMPTS - 1:
            break

        # Try to fix blockers
        console.print(Rule("[bold yellow]Resolving Blockers[/bold yellow]"))
        console.print()

        resolved_count = 0
        blockers = [i for i in result.review_issues if i.issue_severity == "blocker"]

        for issue in blockers:
            success = resolve_blocker(issue, state, working_dir, model, cli, console, fix_index)
            fix_index += 1
            if success:
                resolved_count += 1
                console.print(f"  [green]Resolved:[/green] #{issue.review_issue_number}")
            else:
                console.print(f"  [red]Could not resolve:[/red] #{issue.review_issue_number}")

        console.print(f"\n  Resolved {resolved_count}/{len(blockers)} blockers")

        if resolved_count == 0:
            console.print("[bold yellow]No blockers resolved, stopping retry loop.[/bold yellow]")
            break

    # ── Summary ────────────────────────────────────────────────────
    console.print()
    console.print(Rule("[bold blue]Review Summary[/bold blue]"))
    console.print()

    blocker_count = 0
    if final_result:
        blocker_count = sum(1 for i in final_result.review_issues if i.issue_severity == "blocker")

    if review_success:
        console.print("[bold green]Review passed.[/bold green]")
    else:
        console.print(f"[bold red]Review failed with {blocker_count} blocker(s).[/bold red]")

    # Update state
    state.update(review_success=review_success, review_blocker_count=blocker_count)
    state.save(working_dir, phase="review")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    # Save summary
    reviewer_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/reviewer")
    os.makedirs(reviewer_output_dir, exist_ok=True)

    summary = {
        "phase": "review",
        "run_id": state.run_id,
        "success": review_success,
        "blocker_count": blocker_count,
        "review_summary": final_result.review_summary if final_result else "",
        "issues": [i.model_dump() for i in final_result.review_issues] if final_result else [],
        "screenshots": final_result.screenshots if final_result else [],
    }
    with open(os.path.join(reviewer_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(summary, f, indent=2)

    if is_piped:
        state.to_stdout()

    sys.exit(0 if review_success else 1)


if __name__ == "__main__":
    main()
