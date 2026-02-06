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
Run an adhoc Claude Code prompt from the command line.

Usage:
    uv run agentic/workflows/prompt.py "Write a hello world Python script"

Examples:
    # Run with specific model
    uv run agentic/workflows/prompt.py "Explain this code" --model large

    # Run with custom output file
    uv run agentic/workflows/prompt.py "Create a FastAPI app" --output my_result.jsonl

    # Run from a different working directory
    uv run agentic/workflows/prompt.py "List files here" --working-dir /path/to/project

    # Disable retry on failure
    uv run agentic/workflows/prompt.py "Quick test" --no-retry

    # Use custom agent name
    uv run agentic/workflows/prompt.py "Debug this" --agent-name debugger
"""

import os
import sys
import json
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text

# Add the modules directory to the path so we can import agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agent import (
    prompt_claude_code,
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


@click.command()
@click.argument("prompt", required=True)
@click.option(
    "--model",
    type=click.Choice(["small", "medium", "large"]),
    default="large",
    help="Model tier (maps to CLI-specific models)",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output file path (default: ./output/oneoff_<id>_output.jsonl)",
)
@click.option(
    "--working-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Working directory for the prompt execution (default: current directory)",
)
@click.option("--no-retry", is_flag=True, help="Disable automatic retry on failure")
@click.option(
    "--agent-name", default="oneoff", help="Agent name for tracking (default: oneoff)"
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
    output: str,
    working_dir: str,
    no_retry: bool,
    agent_name: str,
    cli: str,
):
    """Run an adhoc Claude Code prompt from the command line."""
    console = Console()

    # Generate a unique ID for this execution
    run_id = generate_short_id()

    # Set up output file path
    if not output:
        # Default: write to agentic/runs/<run_id>/<agent_name>/
        output_dir = Path(working_dir or os.getcwd()) / f"agentic/runs/{run_id}/{agent_name}"
        output_dir.mkdir(parents=True, exist_ok=True)
        output = str(output_dir / OUTPUT_JSONL)

    # Use current directory if no working directory specified
    if not working_dir:
        working_dir = os.getcwd()

    # Create the prompt request
    request = AgentPromptRequest(
        prompt=prompt,
        run_id=run_id,
        agent_name=agent_name,
        model=model,
        cli=cli,
        dangerously_skip_permissions=True,
        output_file=output,
        working_dir=working_dir,
    )

    # Create execution info table
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()

    info_table.add_row("Run ID", run_id)
    info_table.add_row("Workflow", "prompt")
    info_table.add_row("Prompt", prompt)
    info_table.add_row("Model", model)
    info_table.add_row("CLI", cli)
    info_table.add_row("Working Dir", working_dir)
    info_table.add_row("Output", output)

    console.print(
        Panel(
            info_table,
            title="[bold blue]🚀 Inputs[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    response: AgentPromptResponse | None = None

    try:
        # Execute the prompt
        with console.status("[bold yellow]Executing prompt...[/bold yellow]"):
            if no_retry:
                # Direct execution without retry

                response = prompt_claude_code(request)
            else:
                # Execute with retry logic
                response = prompt_claude_code_with_retry(request)

        # Display the result
        if response.success:
            # Success panel
            result_panel = Panel(
                response.output,
                title="[bold green]✅ Success[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
            console.print(result_panel)

            if response.session_id:
                console.print(
                    f"\n[bold cyan]Session ID:[/bold cyan] {response.session_id}"
                )
        else:
            # Error panel
            error_panel = Panel(
                response.output,
                title="[bold red]❌ Failed[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)

            if response.retry_code != "none":
                console.print(
                    f"\n[bold yellow]Retry code:[/bold yellow] {response.retry_code}"
                )

        # Show output file info
        console.print()

        # Also create a JSON summary file
        if output.endswith(f"/{OUTPUT_JSONL}"):
            # Default path: save as custom_summary_output.json in same directory
            simple_json_output = output.replace(f"/{OUTPUT_JSONL}", f"/{SUMMARY_JSON}")
        else:
            # Custom path: replace .jsonl with _summary.json
            simple_json_output = output.replace(".jsonl", "_summary.json")

        with open(simple_json_output, "w") as f:
            json.dump(
                {
                    "run_id": run_id,
                    "prompt": prompt,
                    "model": model,
                    "cli": cli,
                    "working_dir": working_dir,
                    "success": response.success,
                    "session_id": response.session_id,
                    "retry_code": response.retry_code,
                    "output": response.output,
                },
                f,
                indent=2,
            )

        # Files saved panel with descriptions
        files_table = Table(show_header=True, box=None)
        files_table.add_column("File Type", style="bold cyan")
        files_table.add_column("Path", style="dim")
        files_table.add_column("Description", style="italic")

        # Determine paths for all files
        output_dir = os.path.dirname(output)

        if cli == "claude":
            # Claude outputs JSONL with additional parsed files
            json_array_path = os.path.join(output_dir, OUTPUT_JSON)
            final_object_path = os.path.join(output_dir, FINAL_OBJECT_JSON)

            files_table.add_row(
                "JSONL Stream", output, "Raw streaming output from CLI"
            )
            files_table.add_row(
                "JSON Array", json_array_path, "All messages as a JSON array"
            )
            files_table.add_row(
                "Final Object", final_object_path, "Last message entry (final result)"
            )
        else:
            # Copilot/Gemini output plain text
            files_table.add_row(
                "Text Output", output, "Raw text output from CLI"
            )

        files_table.add_row(
            "Summary", simple_json_output, "High-level execution summary with metadata"
        )

        console.print(
            Panel(
                files_table,
                title="[bold blue]📄 Output Files[/bold blue]",
                border_style="blue",
            )
        )

        # Exit with appropriate code
        sys.exit(0 if response.success else 1)

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
