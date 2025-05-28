"""
Codebase Scanning Agent.

This agent is responsible for scanning and understanding existing codebases,
identifying architecture patterns, components, and technologies used.
"""

import os
from typing import Any, Dict, List

from google.adk.agents import Agent
from google.genai.types import Content, Part

from marvin.agents.base import MODEL_GEMINI_2_0_PRO, create_runner


def scan_directory(
    directory_path: str, ignore_dirs: List[str] = None
) -> Dict[str, List[str]]:
    """
    Scan a directory and collect information about files.

    Args:
        directory_path: Path to the directory to scan
        ignore_dirs: List of directories to ignore (e.g., .git, node_modules)

    Returns:
        Dict with file types and their paths
    """
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"{directory_path} is not a directory")

    if ignore_dirs is None:
        ignore_dirs = [".git", ".venv", "node_modules", "__pycache__"]

    result = {}

    for root, dirs, files in os.walk(directory_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]

        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext not in result:
                result[ext] = []

            result[ext].append(file_path)

    return result


def analyze_codebase(directory_path: str, tool_context: Any = None) -> Dict:
    """
    Analyze a codebase directory and extract information about architecture, patterns, etc.

    Args:
        directory_path: Path to the codebase directory
        tool_context: Tool context provided by ADK (not used here)

    Returns:
        Dict containing analysis results
    """
    # Scan the directory to get file information
    try:
        files_by_type = scan_directory(directory_path)

        # Count files by type
        file_counts = {ext: len(files) for ext, files in files_by_type.items()}

        # Determine primary languages
        primary_languages = []
        if ".py" in file_counts and file_counts[".py"] > 0:
            primary_languages.append("Python")
        if ".js" in file_counts and file_counts[".js"] > 0:
            primary_languages.append("JavaScript")
        if ".ts" in file_counts and file_counts[".ts"] > 0:
            primary_languages.append("TypeScript")

        # For now, return basic information
        # In a real implementation, this would do much more analysis
        return {
            "status": "success",
            "file_count": sum(file_counts.values()),
            "file_types": file_counts,
            "primary_languages": primary_languages,
            "framework_hints": [],  # Would detect frameworks in real implementation
            "patterns": [],  # Would detect architectural patterns
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# Create the codebase scanning agent
codebase_scanner_agent = Agent(
    name="codebase_scanner_agent",
    model=MODEL_GEMINI_2_0_PRO,
    description="Scans and analyzes codebases to identify architecture, components, and technologies",
    instruction="""You are a codebase analysis specialist. Your job is to scan and understand existing codebases,
identifying architecture patterns, components, and technologies used. When a user provides a codebase location,
use the analyze_codebase tool to extract relevant information. Present the results clearly to the user, highlighting
key findings about the codebase structure, patterns, and technologies.""",
    tools=[analyze_codebase],
)

# Create a runner for the agent
codebase_scanner_runner = create_runner(codebase_scanner_agent)


async def scan_codebase_async(directory_path: str) -> Dict:
    """
    Scan a codebase asynchronously using the codebase scanner agent.

    Args:
        directory_path: Path to the codebase directory

    Returns:
        Dict containing the scanning results
    """
    # Create user message with directory path
    message = Content(
        role="user",
        parts=[Part(text=f"Please analyze the codebase at: {directory_path}")],
    )

    # Run the agent and collect the final response
    final_response = None
    async for event in codebase_scanner_runner.run_async(
        user_id="marvin_user",
        session_id="codebase_scanner_session",
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    # Return the analysis results
    return {"status": "success", "analysis": final_response or "No analysis produced"}
