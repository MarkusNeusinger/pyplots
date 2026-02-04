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
Run chore planning and implementation workflow.

This script runs two prompts in sequence:
1. chore.md - Creates a plan based on the prompt
2. implement.md - Implements the plan created by chore

Usage:
    # Method 1: Direct execution (requires uv)
    ./agentic/workflows/chore_implement.py "Add error handling to all API endpoints"

    # Method 2: Using uv run
    uv run agentic/workflows/chore_implement.py "Refactor database connection logic"

Examples:
    # Run with specific model
    ./agentic/workflows/chore_implement.py "Add logging to agent.py" --model medium

    # Run from a different working directory
    ./agentic/workflows/chore_implement.py "Update documentation" --working-dir /path/to/project

    # Use a different CLI tool
    ./agentic/workflows/chore_implement.py "Refactor code" --cli copilot
"""

import os
import sys
import json
import re
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule

# Add the modules directory to the path so we can import agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agent import (
    AgentPromptRequest,
    AgentPromptResponse,
    prompt_claude_code_with_retry,
    generate_short_id,
)

# Output file name constants
OUTPUT_JSONL = "cli_raw_output.jsonl"
OUTPUT_JSON = "cli_raw_output.json"
FINAL_OBJECT_JSON = "cli_final_object.json"
SUMMARY_JSON = "cli_summary_output.json"

# Command template paths (relative to project root)
CHORE_TEMPLATE = "agentic/commands/chore.md"
IMPLEMENT_TEMPLATE = "agentic/commands/implement.md"


def load_template(template_path: str, working_dir: str) -> str:
    """Load a template file from the working directory."""
    full_path = os.path.join(working_dir, template_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Template not found: {full_path}")
    with open(full_path, "r") as f:
        return f.read()


def render_template(template: str, variables: dict) -> str:
    """Render a template by replacing variables.

    Supports:
    - $1, $2, etc. for positional arguments
    - $ARGUMENTS for all arguments joined
    - {variable_name} for named variables
    """
    result = template

    # Replace positional variables ($1, $2, etc.)
    for key, value in variables.items():
        if key.isdigit():
            result = result.replace(f"${key}", str(value))

    # Replace $ARGUMENTS with all positional args joined
    if "ARGUMENTS" in variables:
        result = result.replace("$ARGUMENTS", str(variables["ARGUMENTS"]))

    return result


def extract_plan_path(output: str) -> str:
    """Extract the plan file path from the chore command output.

    Looks for patterns like:
    - agentic/specs/chore-12345678-update-readme.md
    - specs/chore-12345678-update-readme.md
    - Created plan at: specs/chore-...
    - Plan file: specs/chore-...
    """
    # Try multiple patterns to find the plan path
    patterns = [
        r"agentic/specs/chore-[a-zA-Z0-9\-]+\.md",
        r"specs/chore-[a-zA-Z0-9\-]+\.md",
        r"Created plan at:\s*(agentic/specs/chore-[a-zA-Z0-9\-]+\.md)",
        r"Created plan at:\s*(specs/chore-[a-zA-Z0-9\-]+\.md)",
        r"Plan file:\s*(agentic/specs/chore-[a-zA-Z0-9\-]+\.md)",
        r"Plan file:\s*(specs/chore-[a-zA-Z0-9\-]+\.md)",
        r"path.*?:\s*(agentic/specs/chore-[a-zA-Z0-9\-]+\.md)",
        r"path.*?:\s*(specs/chore-[a-zA-Z0-9\-]+\.md)",
    ]

    for pattern in patterns:
        match = re.search(pattern, output, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1) if match.groups() else match.group(0)

    # If no match found, raise an error
    raise ValueError("Could not find plan file path in chore output")


@click.command()
@click.argument("prompt", required=True)
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="large",
    help="Model tier (maps to CLI-specific models)",
)
@click.option(
    "--working-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Working directory for command execution (default: current directory)",
)
@click.option(
    "--cli",
    type=click.Choice(["claude", "copilot", "gemini"]),
    default="claude",
    help="CLI tool to use (default: claude)",
)
def main(
    prompt: str,
    model: str,
    working_dir: str,
    cli: str,
):
    """Run chore planning and implementation workflow."""
    console = Console()

    # Generate a unique ID for this workflow
    run_id = generate_short_id()

    # Use current directory if no working directory specified
    if not working_dir:
        working_dir = os.getcwd()

    # Set default agent names
    planner_name = "planner"
    builder_name = "builder"

    console.print(
        Panel(
            f"[bold blue]Chore & Implement Workflow[/bold blue]\n\n"
            f"[cyan]Run ID:[/cyan] {run_id}\n"
            f"[cyan]CLI:[/cyan] {cli}\n"
            f"[cyan]Model:[/cyan] {model}\n"
            f"[cyan]Working Dir:[/cyan] {working_dir}",
            title="[bold blue]🚀 Workflow Configuration[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    # Phase 1: Run chore planning
    console.print(Rule("[bold yellow]Phase 1: Planning (chore.md)[/bold yellow]"))
    console.print()

    # Load and render the chore template
    try:
        chore_template = load_template(CHORE_TEMPLATE, working_dir)
        chore_prompt = render_template(chore_template, {"1": run_id, "2": prompt})
    except FileNotFoundError as e:
        console.print(
            Panel(
                f"[bold red]{str(e)}[/bold red]",
                title="[bold red]❌ Template Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(2)

    # Create output directory
    chore_output_dir = os.path.join(working_dir, f"agentic/runs/{run_id}/{planner_name}")
    os.makedirs(chore_output_dir, exist_ok=True)
    chore_output_file = os.path.join(chore_output_dir, OUTPUT_JSONL)

    # Create the chore request
    chore_request = AgentPromptRequest(
        prompt=chore_prompt,
        run_id=run_id,
        agent_name=planner_name,
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=chore_output_file,
        working_dir=working_dir,
    )

    # Display chore execution info
    chore_info_table = Table(show_header=False, box=None, padding=(0, 1))
    chore_info_table.add_column(style="bold cyan")
    chore_info_table.add_column()

    chore_info_table.add_row("Run ID", run_id)
    chore_info_table.add_row("Workflow", "chore_implement (planning)")
    chore_info_table.add_row("Template", CHORE_TEMPLATE)
    chore_info_table.add_row("Args", f'{run_id} "{prompt}"')
    chore_info_table.add_row("CLI", cli)
    chore_info_table.add_row("Model", model)
    chore_info_table.add_row("Agent", planner_name)

    console.print(
        Panel(
            chore_info_table,
            title="[bold blue]🚀 Chore Inputs[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    plan_path = None

    try:
        # Execute the chore command
        with console.status("[bold yellow]Creating plan...[/bold yellow]"):
            chore_response = prompt_claude_code_with_retry(chore_request)

        # Display the chore result
        if chore_response.success:
            # Success panel
            console.print(
                Panel(
                    chore_response.output,
                    title="[bold green]✅ Planning Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                )
            )

            # Extract the plan path from the output
            try:
                plan_path = extract_plan_path(chore_response.output)
                console.print(f"\n[bold cyan]Plan created at:[/bold cyan] {plan_path}")
            except ValueError as e:
                console.print(
                    Panel(
                        f"[bold red]Could not extract plan path: {str(e)}[/bold red]\n\n"
                        "The chore command succeeded but the plan file path could not be found in the output.",
                        title="[bold red]❌ Parse Error[/bold red]",
                        border_style="red",
                    )
                )
                sys.exit(3)

        else:
            # Error panel
            console.print(
                Panel(
                    chore_response.output,
                    title="[bold red]❌ Planning Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                )
            )
            console.print(
                "\n[bold red]Workflow aborted: Planning phase failed[/bold red]"
            )
            sys.exit(1)

        # Save chore phase summary
        chore_summary_path = os.path.join(chore_output_dir, SUMMARY_JSON)

        with open(chore_summary_path, "w") as f:
            json.dump(
                {
                    "phase": "planning",
                    "run_id": run_id,
                    "template": CHORE_TEMPLATE,
                    "args": [run_id, prompt],
                    "cli": cli,
                    "model": model,
                    "working_dir": working_dir,
                    "success": chore_response.success,
                    "session_id": chore_response.session_id,
                    "retry_code": str(chore_response.retry_code),
                    "output": chore_response.output,
                    "plan_path": plan_path,
                },
                f,
                indent=2,
            )

        # Show chore output files
        console.print()

        # Files saved panel for chore phase
        chore_files_table = Table(show_header=True, box=None)
        chore_files_table.add_column("File Type", style="bold cyan")
        chore_files_table.add_column("Path", style="dim")
        chore_files_table.add_column("Description", style="italic")

        if cli == "claude":
            # Claude outputs JSONL with additional parsed files
            chore_files_table.add_row(
                "JSONL Stream",
                chore_output_file,
                "Raw streaming output from CLI",
            )
            chore_files_table.add_row(
                "JSON Array",
                os.path.join(chore_output_dir, OUTPUT_JSON),
                "All messages as a JSON array",
            )
            chore_files_table.add_row(
                "Final Object",
                os.path.join(chore_output_dir, FINAL_OBJECT_JSON),
                "Last message entry (final result)",
            )
        else:
            # Copilot/Gemini output plain text
            chore_files_table.add_row(
                "Text Output",
                chore_output_file,
                "Raw text output from CLI",
            )
        chore_files_table.add_row(
            "Summary",
            chore_summary_path,
            "High-level execution summary with metadata",
        )

        console.print(
            Panel(
                chore_files_table,
                title="[bold blue]📄 Planning Output Files[/bold blue]",
                border_style="blue",
            )
        )

        console.print()

        # Phase 2: Run implementation
        console.print(
            Rule("[bold yellow]Phase 2: Implementation (implement.md)[/bold yellow]")
        )
        console.print()

        # Load and render the implement template
        # Read the plan file content to pass as $ARGUMENTS
        plan_full_path = os.path.join(working_dir, plan_path)
        with open(plan_full_path, "r") as f:
            plan_content = f.read()

        implement_template = load_template(IMPLEMENT_TEMPLATE, working_dir)
        implement_prompt = render_template(implement_template, {"ARGUMENTS": plan_content})

        # Create output directory for implementation
        implement_output_dir = os.path.join(working_dir, f"agentic/runs/{run_id}/{builder_name}")
        os.makedirs(implement_output_dir, exist_ok=True)
        implement_output_file = os.path.join(implement_output_dir, OUTPUT_JSONL)

        # Create the implement request
        implement_request = AgentPromptRequest(
            prompt=implement_prompt,
            run_id=run_id,
            agent_name=builder_name,
            model=model,
            cli=cli,
            dangerously_skip_permissions=True,
            output_file=implement_output_file,
            working_dir=working_dir,
        )

        # Display implement execution info
        implement_info_table = Table(show_header=False, box=None, padding=(0, 1))
        implement_info_table.add_column(style="bold cyan")
        implement_info_table.add_column()

        implement_info_table.add_row("Run ID", run_id)
        implement_info_table.add_row("Workflow", "chore_implement (building)")
        implement_info_table.add_row("Template", IMPLEMENT_TEMPLATE)
        implement_info_table.add_row("Plan", plan_path)
        implement_info_table.add_row("CLI", cli)
        implement_info_table.add_row("Model", model)
        implement_info_table.add_row("Agent", builder_name)

        console.print(
            Panel(
                implement_info_table,
                title="[bold blue]🚀 Implement Inputs[/bold blue]",
                border_style="blue",
            )
        )
        console.print()

        # Execute the implement command
        with console.status("[bold yellow]Implementing plan...[/bold yellow]"):
            implement_response = prompt_claude_code_with_retry(implement_request)

        # Display the implement result
        if implement_response.success:
            # Success panel
            console.print(
                Panel(
                    implement_response.output,
                    title="[bold green]✅ Implementation Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                )
            )

            if implement_response.session_id:
                console.print(
                    f"\n[bold cyan]Session ID:[/bold cyan] {implement_response.session_id}"
                )
        else:
            # Error panel
            console.print(
                Panel(
                    implement_response.output,
                    title="[bold red]❌ Implementation Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                )
            )

        # Save implement phase summary
        implement_summary_path = os.path.join(implement_output_dir, SUMMARY_JSON)

        with open(implement_summary_path, "w") as f:
            json.dump(
                {
                    "phase": "implementation",
                    "run_id": run_id,
                    "template": IMPLEMENT_TEMPLATE,
                    "plan_path": plan_path,
                    "cli": cli,
                    "model": model,
                    "working_dir": working_dir,
                    "success": implement_response.success,
                    "session_id": implement_response.session_id,
                    "retry_code": str(implement_response.retry_code),
                    "output": implement_response.output,
                },
                f,
                indent=2,
            )

        # Show implement output files
        console.print()

        # Files saved panel for implement phase
        implement_files_table = Table(show_header=True, box=None)
        implement_files_table.add_column("File Type", style="bold cyan")
        implement_files_table.add_column("Path", style="dim")
        implement_files_table.add_column("Description", style="italic")

        if cli == "claude":
            # Claude outputs JSONL with additional parsed files
            implement_files_table.add_row(
                "JSONL Stream",
                implement_output_file,
                "Raw streaming output from CLI",
            )
            implement_files_table.add_row(
                "JSON Array",
                os.path.join(implement_output_dir, OUTPUT_JSON),
                "All messages as a JSON array",
            )
            implement_files_table.add_row(
                "Final Object",
                os.path.join(implement_output_dir, FINAL_OBJECT_JSON),
                "Last message entry (final result)",
            )
        else:
            # Copilot/Gemini output plain text
            implement_files_table.add_row(
                "Text Output",
                implement_output_file,
                "Raw text output from CLI",
            )
        implement_files_table.add_row(
            "Summary",
            implement_summary_path,
            "High-level execution summary with metadata",
        )

        console.print(
            Panel(
                implement_files_table,
                title="[bold blue]📄 Implementation Output Files[/bold blue]",
                border_style="blue",
            )
        )

        # Show workflow summary
        console.print()
        console.print(Rule("[bold blue]Workflow Summary[/bold blue]"))
        console.print()

        summary_table = Table(show_header=True, box=None)
        summary_table.add_column("Phase", style="bold cyan")
        summary_table.add_column("Status", style="bold")
        summary_table.add_column("Output Directory", style="dim")

        # Planning phase row
        planning_status = "✅ Success" if chore_response.success else "❌ Failed"
        summary_table.add_row(
            "Planning (chore.md)",
            planning_status,
            chore_output_dir,
        )

        # Implementation phase row
        implement_status = "✅ Success" if implement_response.success else "❌ Failed"
        summary_table.add_row(
            "Implementation (implement.md)",
            implement_status,
            implement_output_dir,
        )

        console.print(summary_table)

        # Create overall workflow summary
        workflow_output_dir = os.path.join(working_dir, f"agentic/runs/{run_id}")
        workflow_summary_path = os.path.join(workflow_output_dir, "workflow_summary.json")

        with open(workflow_summary_path, "w") as f:
            json.dump(
                {
                    "workflow": "chore_implement",
                    "run_id": run_id,
                    "prompt": prompt,
                    "cli": cli,
                    "model": model,
                    "working_dir": working_dir,
                    "plan_path": plan_path,
                    "phases": {
                        "planning": {
                            "success": chore_response.success,
                            "session_id": chore_response.session_id,
                            "agent": planner_name,
                            "output_dir": chore_output_dir,
                        },
                        "implementation": {
                            "success": implement_response.success,
                            "session_id": implement_response.session_id,
                            "agent": builder_name,
                            "output_dir": implement_output_dir,
                        },
                    },
                    "overall_success": chore_response.success
                                       and implement_response.success,
                },
                f,
                indent=2,
            )

        console.print(
            f"\n[bold cyan]Workflow summary:[/bold cyan] {workflow_summary_path}"
        )
        console.print()

        # Exit with appropriate code
        if chore_response.success and implement_response.success:
            console.print(
                "[bold green]✅ Workflow completed successfully![/bold green]"
            )
            sys.exit(0)
        else:
            console.print(
                "[bold yellow]⚠️  Workflow completed with errors[/bold yellow]"
            )
            sys.exit(1)

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]{str(e)}[/bold red]",
                title="[bold red]❌ Unexpected Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
