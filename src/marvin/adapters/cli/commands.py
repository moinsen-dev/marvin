"""CLI-Befehle für Marvin."""

import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from marvin import __version__
from marvin.core.agents.codebase_analysis import CodebaseAnalysisAgent
from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.agents.sequence_planner import SequencePlannerAgent
from marvin.core.agents.template_generation import TemplateGenerationAgent
from marvin.core.use_cases.generate_templates import GenerateTemplatesUseCase


console = Console()


def analyze_prd_command(
    prd_path: str,
    codebase_path: Optional[str] = None,
    output_dir: str = "./marvin-output",
) -> None:
    """Analysiert ein PRD und generiert AI-Coding-Tasks.
    
    Args:
        prd_path: Pfad zum PRD-Dokument
        codebase_path: (Optional) Pfad zur bestehenden Codebase
        output_dir: Ausgabeverzeichnis für die Tasks
    """
    console.print(Panel(f"Marvin - Der intelligente Task-Generator", subtitle=f"v{__version__}"))
    console.print("\n[bold]Analysiere PRD...[/bold]")
    console.print(f"PRD-Pfad: {prd_path}")
    
    if not os.path.exists(prd_path):
        console.print(f"[bold red]Fehler:[/bold red] PRD-Datei nicht gefunden: {prd_path}")
        return
    
    if codebase_path:
        console.print(f"Codebase-Pfad: {codebase_path}")
        if not os.path.exists(codebase_path):
            console.print(f"[bold red]Fehler:[/bold red] Codebase-Pfad nicht gefunden: {codebase_path}")
            return
    
    # Ausgabeverzeichnis erstellen
    os.makedirs(output_dir, exist_ok=True)
    console.print(f"Ausgabeverzeichnis: {output_dir}")
    
    # Agenten erstellen
    document_analysis_agent = DocumentAnalysisAgent()
    codebase_analysis_agent = CodebaseAnalysisAgent()
    sequence_planner_agent = SequencePlannerAgent()
    template_generation_agent = TemplateGenerationAgent()
    
    # Use Case erstellen
    use_case = GenerateTemplatesUseCase(
        document_analysis_agent,
        codebase_analysis_agent,
        sequence_planner_agent,
        template_generation_agent,
    )
    
    # Fortschrittsanzeige mit Spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Analysiere PRD und generiere Templates...", total=None)
        
        # Asynchrone Ausführung in einem synchronen Kontext
        try:
            workflow_id, template_paths = asyncio.run(
                use_case.execute(
                    prd_path=prd_path,
                    output_dir=output_dir,
                    codebase_path=codebase_path,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
            progress.update(task, completed=True)
            
            # Ergebnis anzeigen
            console.print("\n[bold green]Analyse abgeschlossen![/bold green]")
            console.print(f"Workflow-ID: {workflow_id}")
            console.print(f"Generierte Templates: {len(template_paths)}")
            
            for i, path in enumerate(template_paths, 1):
                rel_path = os.path.relpath(path, os.getcwd())
                console.print(f"  {i}. [blue]{rel_path}[/blue]")
            
            console.print(
                f"\nDu kannst diese Templates jetzt mit deinem bevorzugten AI-Coding-Assistenten verwenden."
            )
        
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"\n[bold red]Fehler bei der Analyse:[/bold red] {str(e)}")


def serve_api_command(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Startet den API-Server.
    
    Args:
        host: Host-Adresse
        port: Port-Nummer
    """
    console.print(Panel(f"Marvin API-Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starte API-Server auf {host}:{port}...[/bold]")
    
    try:
        from marvin.adapters.api.server import start_server
        
        start_server(host=host, port=port)
    except ImportError:
        console.print("[bold red]Fehler:[/bold red] API-Server-Modul nicht gefunden.")
    except Exception as e:
        console.print(f"[bold red]Fehler beim Starten des API-Servers:[/bold red] {str(e)}")


def serve_mcp_command(host: str = "127.0.0.1", port: int = 9000) -> None:
    """Startet den MCP-Server.
    
    Args:
        host: Host-Adresse
        port: Port-Nummer
    """
    console.print(Panel(f"Marvin MCP-Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starte MCP-Server auf {host}:{port}...[/bold]")
    
    try:
        from marvin.adapters.mcp.server import start_server
        
        start_server(host=host, port=port)
    except ImportError:
        console.print("[bold red]Fehler:[/bold red] MCP-Server-Modul nicht gefunden.")
    except Exception as e:
        console.print(f"[bold red]Fehler beim Starten des MCP-Servers:[/bold red] {str(e)}")
