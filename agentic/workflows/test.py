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
Standalone test workflow with automatic failure resolution.

Runs the test.md template, parses results, and for each failing test
spawns an inline-prompt agent to fix the issue. Retries up to 4 times.

Usage:
    # With run-id from a previous build
    uv run agentic/workflows/test.py --run-id abc12345

    # Piped from build.py
    uv run agentic/workflows/build.py --run-id abc12345 | uv run agentic/workflows/test.py
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

from agent import AgentPromptRequest, prompt_claude_code_with_retry, generate_short_id, parse_json, TestResult
from state import WorkflowState

# Output file names
OUTPUT_JSONL = "cli_raw_output.jsonl"
SUMMARY_JSON = "cli_summary_output.json"

# Template path
TEST_TEMPLATE = "agentic/commands/test.md"

# Retry configuration
MAX_TEST_RETRY_ATTEMPTS = 4


def load_template(template_path: str, working_dir: str) -> str:
    """Load a template file from the working directory."""
    full_path = os.path.join(working_dir, template_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Template not found: {full_path}")
    with open(full_path, "r") as f:
        return f.read()


def resolve_state(run_id: str, working_dir: str, console: Console) -> WorkflowState:
    """Resolve state from --run-id or stdin pipe."""
    # Priority 1: explicit run-id
    if run_id:
        state = WorkflowState.load(run_id, working_dir)
        if not state:
            console.print(f"[bold red]No state found for run-id: {run_id}[/bold red]")
            console.print(f"Expected: agentic/runs/{run_id}/state.json")
            sys.exit(1)
        return state

    # Priority 2: piped stdin from build.py
    state = WorkflowState.from_stdin()
    if state:
        return state

    # No state source
    console.print("[bold red]No state source provided.[/bold red]")
    console.print("\nUsage:")
    console.print("  uv run agentic/workflows/test.py --run-id <id>")
    console.print("  uv run agentic/workflows/build.py --run-id <id> | uv run agentic/workflows/test.py")
    sys.exit(1)


def run_tests(
    state: WorkflowState, working_dir: str, model: str, cli: str, console: Console, attempt: int
) -> list[TestResult]:
    """Run test.md template and parse results into TestResult objects."""
    template = load_template(TEST_TEMPLATE, working_dir)

    tester_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/tester")
    os.makedirs(tester_output_dir, exist_ok=True)

    # Use attempt-suffixed output file to preserve history
    output_file = os.path.join(
        tester_output_dir, f"cli_raw_output_attempt{attempt}.jsonl" if attempt > 0 else OUTPUT_JSONL
    )

    request = AgentPromptRequest(
        prompt=template,
        run_id=state.run_id,
        agent_name="tester",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=output_file,
        working_dir=working_dir,
    )

    with console.status(
        f"[bold yellow]Running tests (attempt {attempt + 1}/{MAX_TEST_RETRY_ATTEMPTS})...[/bold yellow]"
    ):
        response = prompt_claude_code_with_retry(request)

    if not response.success:
        console.print(Panel(response.output, title="[bold red]Test Execution Failed[/bold red]", border_style="red"))
        return []

    try:
        results = parse_json(response.output, TestResult)
        if not isinstance(results, list):
            results = [results]
        return results
    except (json.JSONDecodeError, ValueError) as e:
        console.print(
            Panel(
                f"Failed to parse test output: {e}\n\nRaw output:\n{response.output[:500]}",
                title="[bold red]Parse Error[/bold red]",
                border_style="red",
            )
        )
        return []


def resolve_failing_test(
    test: TestResult, state: WorkflowState, working_dir: str, model: str, cli: str, console: Console, fix_index: int
) -> bool:
    """Attempt to fix a single failing test via inline prompt."""
    resolve_prompt = (
        f"A test is failing. Fix the code so the test passes.\n\n"
        f"Test: {test.test_name}\n"
        f"Command: {test.execution_command}\n"
        f"Purpose: {test.test_purpose}\n"
        f"Error:\n{test.error}\n\n"
        f"Fix the issue and verify by running: {test.execution_command}"
    )

    fixer_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/tester/fixes")
    os.makedirs(fixer_output_dir, exist_ok=True)

    request = AgentPromptRequest(
        prompt=resolve_prompt,
        run_id=state.run_id,
        agent_name="tester",
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=os.path.join(fixer_output_dir, f"fix_{fix_index}_{test.test_name}.jsonl"),
        working_dir=working_dir,
    )

    console.print(f"  Fixing [cyan]{test.test_name}[/cyan]...")
    response = prompt_claude_code_with_retry(request, max_retries=1)
    return response.success


def display_test_results(results: list[TestResult], console: Console) -> tuple[int, int]:
    """Display test results table and return (passed, failed) counts."""
    table = Table(show_header=True, box=None)
    table.add_column("Test", style="bold")
    table.add_column("Status")
    table.add_column("Command", style="dim")

    passed = 0
    failed = 0
    for r in results:
        if r.passed:
            passed += 1
            table.add_row(r.test_name, "[green]PASS[/green]", r.execution_command)
        else:
            failed += 1
            error_snippet = (r.error or "")[:80]
            table.add_row(r.test_name, f"[red]FAIL[/red] {error_snippet}", r.execution_command)

    console.print(table)
    console.print(f"\n  [green]{passed} passed[/green], [red]{failed} failed[/red]")
    return passed, failed


@click.command()
@click.option("--run-id", default=None, help="Run ID from a previous plan/build execution")
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="large",
    help="Model tier for testing (default: large)",
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
    """Run tests with automatic failure resolution."""
    is_piped = not sys.stdout.isatty()
    console = Console(file=sys.stderr if is_piped else None)

    if not working_dir:
        working_dir = os.getcwd()

    state = resolve_state(run_id, working_dir, console)

    console.print(
        Panel(
            f"[bold blue]Test Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {state.run_id}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Max Retries:[/cyan] {MAX_TEST_RETRY_ATTEMPTS}",
            title="[bold blue]Test Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # ── Test retry loop ────────────────────────────────────────────
    all_passed = False
    final_results = []
    fix_index = 0

    for attempt in range(MAX_TEST_RETRY_ATTEMPTS):
        console.print(Rule(f"[bold yellow]Test Run {attempt + 1}/{MAX_TEST_RETRY_ATTEMPTS}[/bold yellow]"))
        console.print()

        results = run_tests(state, working_dir, model, cli, console, attempt)
        final_results = results

        if not results:
            console.print("[bold red]No test results returned.[/bold red]")
            break

        passed, failed = display_test_results(results, console)
        console.print()

        if failed == 0:
            all_passed = True
            break

        # Last attempt — don't try to fix
        if attempt == MAX_TEST_RETRY_ATTEMPTS - 1:
            break

        # Try to fix each failing test
        console.print(Rule("[bold yellow]Resolving Failures[/bold yellow]"))
        console.print()

        resolved_count = 0
        failing_tests = [r for r in results if not r.passed]

        for test in failing_tests:
            success = resolve_failing_test(test, state, working_dir, model, cli, console, fix_index)
            fix_index += 1
            if success:
                resolved_count += 1
                console.print(f"  [green]Resolved:[/green] {test.test_name}")
            else:
                console.print(f"  [red]Could not resolve:[/red] {test.test_name}")

        console.print(f"\n  Resolved {resolved_count}/{len(failing_tests)} failures")

        if resolved_count == 0:
            console.print("[bold yellow]No tests resolved, stopping retry loop.[/bold yellow]")
            break

    # ── Summary ────────────────────────────────────────────────────
    console.print()
    console.print(Rule("[bold blue]Test Summary[/bold blue]"))
    console.print()

    failed_count = sum(1 for r in final_results if not r.passed)

    if all_passed:
        console.print("[bold green]All tests passed.[/bold green]")
    else:
        console.print(f"[bold red]{failed_count} test(s) still failing.[/bold red]")

    # Update state
    state.update(test_passed=all_passed, test_failed_count=failed_count)
    state.save(working_dir, phase="test")
    console.print(f"[bold cyan]State saved:[/bold cyan] agentic/runs/{state.run_id}/state.json")

    # Save summary
    tester_output_dir = os.path.join(working_dir, f"agentic/runs/{state.run_id}/tester")
    os.makedirs(tester_output_dir, exist_ok=True)

    summary = {
        "phase": "testing",
        "run_id": state.run_id,
        "all_passed": all_passed,
        "failed_count": failed_count,
        "total_tests": len(final_results),
        "results": [r.model_dump() for r in final_results],
    }
    with open(os.path.join(tester_output_dir, SUMMARY_JSON), "w") as f:
        json.dump(summary, f, indent=2)

    if is_piped:
        state.to_stdout()

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
