"""CLI commands for Marvin."""

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
    """Analyzes a PRD and generates AI coding tasks.
    
    Args:
        prd_path: Path to the PRD document
        codebase_path: (Optional) Path to the existing codebase
        output_dir: Output directory for the tasks
    """
    console.print(Panel(f"Marvin - The Intelligent Task Generator", subtitle=f"v{__version__}"))
    console.print("\n[bold]Analyzing PRD...[/bold]")
    console.print(f"PRD Path: {prd_path}")
    
    if not os.path.exists(prd_path):
        console.print(f"[bold red]Error:[/bold red] PRD file not found: {prd_path}")
        return
    
    if codebase_path:
        console.print(f"Codebase Path: {codebase_path}")
        if not os.path.exists(codebase_path):
            console.print(f"[bold red]Error:[/bold red] Codebase path not found: {codebase_path}")
            return
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    console.print(f"Output Directory: {output_dir}")
    
    # Create agents
    document_analysis_agent = DocumentAnalysisAgent()
    codebase_analysis_agent = CodebaseAnalysisAgent()
    sequence_planner_agent = SequencePlannerAgent()
    template_generation_agent = TemplateGenerationAgent()
    
    # Create use case
    use_case = GenerateTemplatesUseCase(
        document_analysis_agent,
        codebase_analysis_agent,
        sequence_planner_agent,
        template_generation_agent,
    )
    
    # Progress display with spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing PRD and generating templates...", total=None)
        
        # Asynchronous execution in a synchronous context
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
            
            # Show results
            console.print("\n[bold green]Analysis completed![/bold green]")
            console.print(f"Workflow ID: {workflow_id}")
            console.print(f"Generated Templates: {len(template_paths)}")
            
            for i, path in enumerate(template_paths, 1):
                rel_path = os.path.relpath(path, os.getcwd())
                console.print(f"  {i}. [blue]{rel_path}[/blue]")
            
            console.print(
                f"\nYou can now use these templates with your preferred AI coding assistant."
            )
        
        except Exception as e:
            progress.update(task, completed=True)
            console.print(f"\n[bold red]Error during analysis:[/bold red] {str(e)}")


def serve_api_command(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Starts the API server.
    
    Args:
        host: Host address
        port: Port number
    """
    console.print(Panel(f"Marvin API Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starting API server on {host}:{port}...[/bold]")
    
    try:
        from marvin.adapters.api.server import start_server
        
        start_server(host=host, port=port)
    except ImportError:
        console.print("[bold red]Error:[/bold red] API server module not found.")
    except Exception as e:
        console.print(f"[bold red]Error starting API server:[/bold red] {str(e)}")


def serve_mcp_command(host: str = "127.0.0.1", port: int = 9000) -> None:
    """Starts the MCP server.
    
    Args:
        host: Host address
        port: Port number
    """
    console.print(Panel(f"Marvin MCP Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starting MCP server on {host}:{port}...[/bold]")
    
    try:
        from marvin.adapters.mcp.server import start_server
        
        start_server(host=host, port=port)
    except ImportError:
        console.print("[bold red]Error:[/bold red] MCP server module not found.")
    except Exception as e:
        console.print(f"[bold red]Error starting MCP server:[/bold red] {str(e)}")
