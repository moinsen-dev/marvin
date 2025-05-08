"""Command Line Interface for Marvin."""

import os
import sys
from typing import Optional

import typer
from rich.console import Console

from marvin import __version__
from marvin.adapters.cli.commands import (
    analyze_prd_command,
    serve_api_command,
    serve_mcp_command,
)

app = typer.Typer(
    name="marvin",
    help="Marvin - The intelligent task generator for AI coding assistants",
    add_completion=False,
)

console = Console()


def _print_version(value: bool) -> None:
    """Displays the version and exits the program."""
    if value:
        console.print(f"Marvin version: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Displays the version and exits the program.",
        callback=_print_version,
        is_eager=True,
    ),
) -> None:
    """Marvin - The intelligent task generator for AI coding assistants."""
    pass


@app.command("analyze")
def analyze_prd(
    prd_path: str = typer.Argument(..., help="Path to the PRD document"),
    codebase_path: Optional[str] = typer.Option(
        None, "--codebase", "-c", help="Path to the existing codebase (optional)"
    ),
    output_dir: str = typer.Option(
        "./marvin-output", "--output", "-o", help="Output directory for tasks"
    ),
) -> None:
    """Analyzes a PRD and generates AI coding tasks."""
    analyze_prd_command(prd_path, codebase_path, output_dir)


@app.command("serve-api")
def serve_api(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address"),
    port: int = typer.Option(8000, "--port", "-p", help="Port"),
) -> None:
    """Starts the API server."""
    serve_api_command(host, port)


@app.command("serve-mcp")
def serve_mcp(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host address"),
    port: int = typer.Option(9000, "--port", "-p", help="Port"),
) -> None:
    """Starts the MCP server."""
    serve_mcp_command(host, port)


if __name__ == "__main__":
    app()
