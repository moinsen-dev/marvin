"""Command Line Interface für Marvin."""

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
    help="Marvin - Der intelligente Task-Generator für AI-Coding-Assistenten",
    add_completion=False,
)

console = Console()


def _print_version(value: bool) -> None:
    """Zeigt die Version an und beendet das Programm."""
    if value:
        console.print(f"Marvin version: {__version__}")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Zeigt die Version an und beendet das Programm.",
        callback=_print_version,
        is_eager=True,
    ),
) -> None:
    """Marvin - Der intelligente Task-Generator für AI-Coding-Assistenten."""
    pass


@app.command("analyze")
def analyze_prd(
    prd_path: str = typer.Argument(..., help="Pfad zum PRD-Dokument"),
    codebase_path: Optional[str] = typer.Option(
        None, "--codebase", "-c", help="Pfad zur bestehenden Codebase (optional)"
    ),
    output_dir: str = typer.Option(
        "./marvin-output", "--output", "-o", help="Ausgabeverzeichnis für die Tasks"
    ),
) -> None:
    """Analysiert ein PRD und generiert AI-Coding-Tasks."""
    analyze_prd_command(prd_path, codebase_path, output_dir)


@app.command("serve-api")
def serve_api(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host-Adresse"),
    port: int = typer.Option(8000, "--port", "-p", help="Port"),
) -> None:
    """Startet den API-Server."""
    serve_api_command(host, port)


@app.command("serve-mcp")
def serve_mcp(
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host-Adresse"),
    port: int = typer.Option(9000, "--port", "-p", help="Port"),
) -> None:
    """Startet den MCP-Server."""
    serve_mcp_command(host, port)


if __name__ == "__main__":
    app()
