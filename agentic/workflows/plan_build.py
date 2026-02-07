#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "click",
#   "rich",
# ]
# ///
"""
Plan + Build orchestrator — chains plan.py and build.py.

Chains plan.py and build.py in a composable two-phase workflow.

Usage:
    uv run agentic/workflows/plan_build.py "Add error handling to API endpoints"
    uv run agentic/workflows/plan_build.py "Fix the 404 bug" --model small
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
    """Plan and build in sequence."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    console.print(
        Panel(
            f"[bold blue]Plan + Build Orchestrator[/bold blue]\n\n"
            f"[cyan]Prompt:[/cyan] {prompt}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]CLI:[/cyan] {cli}",
            title="[bold blue]Orchestrator[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Phase 1: Plan ──────────────────────────────────────────────
    console.print(Rule("[bold yellow]Phase 1: Plan[/bold yellow]"))
    console.print()

    plan_args = [prompt, "--model", model, "--cli", cli]
    if task_type:
        plan_args.extend(["--type", task_type])
    if working_dir:
        plan_args.extend(["--working-dir", working_dir])

    # Capture stdout to get the state JSON with run_id
    plan_rc, plan_stdout = run_phase("plan.py", plan_args, console, "Plan", capture_stdout=True)

    if plan_rc != 0:
        console.print("[bold red]Plan phase failed. Aborting.[/bold red]")
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

    build_args = ["--run-id", run_id, "--model", model, "--cli", cli]
    if working_dir:
        build_args.extend(["--working-dir", working_dir])

    build_rc, build_stdout = run_phase("build.py", build_args, console, "Build", capture_stdout=is_piped)

    # ── Done ───────────────────────────────────────────────────────
    console.print()
    if build_rc == 0:
        console.print("[bold green]Plan + Build completed successfully.[/bold green]")
    else:
        console.print("[bold red]Build phase failed.[/bold red]")

    # Forward state for further piping
    if is_piped and build_stdout:
        print(build_stdout, end="")

    sys.exit(build_rc)


if __name__ == "__main__":
    main()
