#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "click",
#   "rich",
# ]
# ///
"""
Complete SDLC orchestrator: Plan + Build + Test + Review + Document + Commit + PR.

Chains all workflow phases into a single end-to-end pipeline.
Test, document, and PR failures are non-fatal. Build, commit, and review
failures abort the pipeline.

Usage:
    uv run agentic/workflows/sdlc.py "Add CSV export to API endpoints"
    uv run agentic/workflows/sdlc.py "Fix the 404 bug" --type bug --model large
"""

import os
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule


# Add the modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from orchestrator import extract_run_id, run_phase


@click.command()
@click.argument("prompt", required=True)
@click.option(
    "--type",
    "task_type",
    type=click.Choice(["bug", "feature", "chore", "refactor"]),
    default=None,
    help="Skip classifier, use this type directly",
)
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
def main(prompt: str, task_type: str, model: str, working_dir: str, cli: str):
    """Full SDLC: plan, build, test, review, document, commit, and PR."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    console.print(
        Panel(
            f"[bold blue]SDLC Orchestrator[/bold blue]\n\n"
            f"[cyan]Pipeline:[/cyan] Plan → Build → Test → Review → Document → Commit → PR\n"
            f"[cyan]Prompt:[/cyan] {prompt}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]CLI:[/cyan] {cli}",
            title="[bold blue]Full SDLC Pipeline[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    common_args = ["--model", model, "--cli", cli]
    if working_dir:
        common_args.extend(["--working-dir", working_dir])

    # Track results for summary
    phase_results = {}

    # ── Phase 1: Plan ──────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 1: Plan[/bold yellow]"))
    console.print()

    plan_args = [prompt] + common_args[:]
    if task_type:
        plan_args.extend(["--type", task_type])

    plan_rc, plan_stdout = run_phase("plan.py", plan_args, console, "Plan", capture_stdout=True)
    phase_results["Plan"] = plan_rc

    if plan_rc != 0:
        console.print("[bold red]Plan phase failed. Aborting.[/bold red]")
        _print_summary(console, phase_results)
        sys.exit(plan_rc)

    run_id = extract_run_id(plan_stdout)
    if not run_id:
        console.print("[bold red]Could not extract run_id from plan output.[/bold red]")
        sys.exit(1)

    console.print(f"\n[bold cyan]Run ID:[/bold cyan] {run_id}")
    console.print()

    # ── Phase 2: Build ─────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 2: Build[/bold yellow]"))
    console.print()

    build_args = ["--run-id", run_id] + common_args
    build_rc, _ = run_phase("build.py", build_args, console, "Build")
    phase_results["Build"] = build_rc

    if build_rc != 0:
        console.print("[bold red]Build phase failed. Aborting.[/bold red]")
        _print_summary(console, phase_results)
        sys.exit(build_rc)

    console.print()

    # ── Phase 3: Test ──────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 3: Test (with auto-fix)[/bold yellow]"))
    console.print()

    test_args = ["--run-id", run_id] + common_args
    test_rc, _ = run_phase("test.py", test_args, console, "Test")
    phase_results["Test"] = test_rc

    if test_rc != 0:
        console.print("[bold red]Test phase failed after retries. Aborting.[/bold red]")
        _print_summary(console, phase_results)
        sys.exit(test_rc)

    console.print()

    # ── Phase 4: Review ────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 4: Review (with blocker resolution)[/bold yellow]"))
    console.print()

    review_args = ["--run-id", run_id] + common_args
    review_rc, _ = run_phase("review.py", review_args, console, "Review")
    phase_results["Review"] = review_rc

    if review_rc != 0:
        console.print("[bold red]Review phase failed after retries. Aborting.[/bold red]")
        _print_summary(console, phase_results)
        sys.exit(review_rc)

    console.print()

    # ── Phase 5: Document ──────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 5: Document[/bold yellow]"))
    console.print()

    doc_args = ["--run-id", run_id] + common_args
    doc_rc, _ = run_phase("document.py", doc_args, console, "Document")
    phase_results["Document"] = doc_rc

    if doc_rc != 0:
        console.print("[bold yellow]Documentation failed, continuing.[/bold yellow]")

    console.print()

    # ── Phase 6: Commit ────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 6: Commit[/bold yellow]"))
    console.print()

    commit_args = ["--run-id", run_id] + common_args
    commit_rc, _ = run_phase("commit.py", commit_args, console, "Commit")
    phase_results["Commit"] = commit_rc

    if commit_rc != 0:
        console.print("[bold red]Commit failed. Skipping PR.[/bold red]")
        _print_summary(console, phase_results)
        sys.exit(commit_rc)

    console.print()

    # ── Phase 7: Pull Request ──────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 7: Pull Request[/bold yellow]"))
    console.print()

    pr_args = ["--run-id", run_id] + common_args
    pr_rc, pr_stdout = run_phase("pull_request.py", pr_args, console, "Pull Request", capture_stdout=is_piped)
    phase_results["PR"] = pr_rc

    # ── Summary ────────────────────────────────────────────────────
    _print_summary(console, phase_results)

    if is_piped and pr_stdout:
        print(pr_stdout, end="")

    final_rc = commit_rc or pr_rc
    sys.exit(final_rc)


def _print_summary(console: Console, phase_results: dict):
    """Print pipeline summary with phase statuses."""
    console.print()
    console.print(Rule("[bold blue]SDLC Pipeline Summary[/bold blue]"))
    console.print()

    all_passed = all(rc == 0 for rc in phase_results.values())

    for name, rc in phase_results.items():
        status = "[green]PASS[/green]" if rc == 0 else "[red]FAIL[/red]"
        console.print(f"  {name}: {status}")

    console.print()
    if all_passed:
        console.print("[bold green]Full SDLC pipeline completed successfully.[/bold green]")
    else:
        console.print("[bold red]SDLC pipeline completed with failures.[/bold red]")


if __name__ == "__main__":
    main()
