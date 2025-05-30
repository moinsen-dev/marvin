"""
Main Marvin orchestrator using the new domain-driven architecture.

This replaces the ADK-based agent with a proper domain service orchestration.
"""

import asyncio
import os
from pathlib import Path
from typing import Optional

from marvin.core.application import ProcessPRDUseCase
from marvin.core.domain.services import (
    CodebaseScanner,
    PRDAnalyzer,
    TaskSequencer,
    TemplateGenerator,
)
from marvin.infrastructure.ai import GeminiClient


async def process_prd_async(
    prd_path: str,
    codebase_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> dict:
    """
    Process a PRD file asynchronously using the new architecture.

    Args:
        prd_path: Path to the PRD file
        codebase_path: Optional path to the codebase directory
        output_dir: Optional output directory for results

    Returns:
        Dict containing the processing results
    """
    # Validate inputs
    prd_file = Path(prd_path)
    if not prd_file.exists():
        return {"status": "error", "error_message": f"PRD file not found: {prd_path}"}

    codebase_dir = None
    if codebase_path:
        codebase_dir = Path(codebase_path)
        if not codebase_dir.is_dir():
            return {
                "status": "error",
                "error_message": f"Codebase directory not found: {codebase_path}",
            }

    output_path = Path(output_dir) if output_dir else None

    try:
        # Initialize infrastructure
        ai_client = GeminiClient()
        
        # Initialize domain services
        prd_analyzer = PRDAnalyzer()
        codebase_scanner = CodebaseScanner()
        task_sequencer = TaskSequencer()
        template_generator = TemplateGenerator()
        
        # Create use case
        use_case = ProcessPRDUseCase(
            prd_analyzer=prd_analyzer,
            codebase_scanner=codebase_scanner,
            task_sequencer=task_sequencer,
            template_generator=template_generator,
            ai_service=ai_client,
        )
        
        # Execute the use case
        result = await use_case.execute(
            prd_path=prd_file,
            codebase_path=codebase_dir,
            output_dir=output_path,
        )
        
        # Format results
        return {
            "status": "success",
            "features_analyzed": len(result.context.prd_document.features),
            "tasks_generated": len(result.task_sequence.tasks),
            "templates_created": len(result.generated_templates),
            "insights": result.insights,
            "warnings": result.warnings,
            "processing_time": result.processing_time_seconds,
            "output_directory": str(output_path) if output_path else None,
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Processing failed: {str(e)}",
        }


def process_prd(
    prd_path: str,
    codebase_path: Optional[str] = None,
    output_dir: Optional[str] = None,
) -> dict:
    """
    Synchronous wrapper for process_prd_async.

    Args:
        prd_path: Path to the PRD file
        codebase_path: Optional path to the codebase directory
        output_dir: Optional output directory for results

    Returns:
        Dict containing the processing results
    """
    return asyncio.run(process_prd_async(prd_path, codebase_path, output_dir))


# For backward compatibility
main_agent = None  # No longer using ADK agents
main_agent_runner = None  # No longer using ADK runners
