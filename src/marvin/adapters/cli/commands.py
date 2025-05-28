"""CLI commands for Marvin."""

import asyncio
import os
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from marvin import __version__
from marvin.core.agents.codebase_analysis import CodebaseAnalysisAgent
from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.agents.sequence_planner import SequencePlannerAgent
from marvin.core.agents.template_generation import TemplateGenerationAgent
from marvin.core.use_cases.generate_templates import GenerateTemplatesUseCase
from marvin.logging import get_logger

console = Console()
logger = get_logger("cli.commands")


def analyze_prd_command(
    prd_path: str,
    codebase_path: str | None = None,
    output_dir: str = "./marvin-output",
) -> None:
    """Analyzes a PRD and generates AI coding tasks.

    Args:
        prd_path: Path to the PRD document
        codebase_path: (Optional) Path to the existing codebase
        output_dir: Output directory for the tasks
    """
    start_time = time.time()
    logger.info(
        f"Executing analyze_prd_command with prd_path={prd_path}, codebase_path={codebase_path}, output_dir={output_dir}"
    )

    console.print(
        Panel("Marvin - The Intelligent Task Generator", subtitle=f"v{__version__}")
    )
    console.print("\n[bold]Analyzing PRD...[/bold]")
    console.print(f"PRD Path: {prd_path}")

    if not os.path.exists(prd_path):
        logger.error(f"PRD file not found: {prd_path}")
        console.print(f"[bold red]Error:[/bold red] PRD file not found: {prd_path}")
        return

    if codebase_path:
        console.print(f"Codebase Path: {codebase_path}")
        if not os.path.exists(codebase_path):
            logger.error(f"Codebase path not found: {codebase_path}")
            console.print(
                f"[bold red]Error:[/bold red] Codebase path not found: {codebase_path}"
            )
            return

    # Create output directory
    try:
        os.makedirs(output_dir, exist_ok=True)
        logger.debug(f"Created or verified output directory: {output_dir}")
        console.print(f"Output Directory: {output_dir}")
    except Exception as e:
        logger.error(f"Error creating output directory: {str(e)}")
        console.print(
            f"[bold red]Error:[/bold red] Could not create output directory: {str(e)}"
        )
        return

    # Create agents
    logger.debug("Initializing agents")
    document_analysis_agent = DocumentAnalysisAgent()
    codebase_analysis_agent = CodebaseAnalysisAgent()
    sequence_planner_agent = SequencePlannerAgent()
    template_generation_agent = TemplateGenerationAgent()

    # Create use case
    logger.debug("Initializing use case")
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
        task = progress.add_task(
            "Analyzing PRD and generating templates...", total=None
        )

        # Asynchronous execution in a synchronous context
        try:
            logger.info("Starting use case execution")
            start_exec_time = time.time()
            workflow_id, template_paths = asyncio.run(
                use_case.execute(
                    prd_path=prd_path,
                    output_dir=output_dir,
                    codebase_path=codebase_path,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
            )
            exec_time = time.time() - start_exec_time
            logger.info(f"Use case execution completed in {exec_time:.2f}s")
            progress.update(task, completed=True)

            # Show results
            console.print("\n[bold green]Analysis completed![/bold green]")
            console.print(f"Workflow ID: {workflow_id}")
            console.print(f"Generated Templates: {len(template_paths)}")

            for i, path in enumerate(template_paths, 1):
                rel_path = os.path.relpath(path, os.getcwd())
                console.print(f"  {i}. [blue]{rel_path}[/blue]")
                logger.debug(f"Generated template {i}: {rel_path}")

            console.print(
                "\nYou can now use these templates with your preferred AI coding assistant."
            )
            logger.info(
                f"Analysis successful. Generated {len(template_paths)} templates"
            )

        except Exception as e:
            logger.error(f"Error during analysis: {str(e)}", exc_info=True)
            progress.update(task, completed=True)
            console.print(f"\n[bold red]Error during analysis:[/bold red] {str(e)}")

    total_time = time.time() - start_time
    logger.info(f"analyze_prd_command completed in {total_time:.2f}s")


def serve_api_command(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Starts the API server.

    Args:
        host: Host address
        port: Port number
    """
    logger.info(f"Starting API server on {host}:{port}")
    console.print(Panel("Marvin API Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starting API server on {host}:{port}...[/bold]")

    try:
        from marvin.adapters.api.server import start_server

        logger.debug("API server module imported")
        start_server(host=host, port=port)
    except ImportError:
        error_msg = "API server module not found"
        logger.error(error_msg)
        console.print(f"[bold red]Error:[/bold red] {error_msg}")
    except Exception as e:
        error_msg = f"Error starting API server: {str(e)}"
        logger.error(error_msg, exc_info=True)
        console.print(f"[bold red]Error starting API server:[/bold red] {str(e)}")


def serve_mcp_command(host: str = "127.0.0.1", port: int = 9000) -> None:
    """Starts the MCP server.

    Args:
        host: Host address
        port: Port number
    """
    logger.info(f"Starting MCP server on {host}:{port}")
    console.print(Panel("Marvin MCP Server", subtitle=f"v{__version__}"))
    console.print(f"[bold]Starting MCP server on {host}:{port}...[/bold]")

    try:
        from marvin.adapters.mcp.server import start_server

        logger.debug("MCP server module imported")
        start_server(host=host, port=port)
    except ImportError:
        error_msg = "MCP server module not found"
        logger.error(error_msg)
        console.print(f"[bold red]Error:[/bold red] {error_msg}")
    except Exception as e:
        error_msg = f"Error starting MCP server: {str(e)}"
        logger.error(error_msg, exc_info=True)
        console.print(f"[bold red]Error starting MCP server:[/bold red] {str(e)}")
