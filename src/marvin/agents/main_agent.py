"""
Main Marvin Agent.

This agent orchestrates the entire Marvin workflow, coordinating the PRD analysis,
codebase scanning, template generation, and sequence planning agents to convert
PRD documents into AI-Coding-Task templates.
"""

import asyncio
import os

from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.genai.types import Content, Part

from marvin.agents.base import MODEL_GEMINI_2_0_PRO, create_runner
from marvin.agents.codebase_scanner import codebase_scanner_agent
from marvin.agents.prd_analysis import prd_analysis_agent
from marvin.agents.sequence_planner import sequence_planner_agent
from marvin.agents.template_generator import template_generator_agent

# Create the main agent using AgentTool to delegate to specialized agents
main_agent = Agent(
    name="marvin_main_agent",
    model=MODEL_GEMINI_2_0_PRO,
    description="Orchestrates the conversion of PRD documents into AI-Coding-Task templates",
    instruction="""You are Marvin, an intelligent agent for converting Product Requirements Documents (PRDs)
into structured AI-Coding-Tasks. Named after the paranoid-depressive robot from "The Hitchhiker's Guide to the Galaxy,"
you help developers organize their projects and effectively use AI coding assistants.

Your capabilities include:
1. Analyzing PRD documents to extract features and requirements
2. Scanning codebases to understand project structure and technologies
3. Generating XML task templates for AI coding assistants
4. Planning optimal implementation sequences based on dependencies

When a user provides a PRD document and/or codebase location, coordinate the specialized agents
to process the inputs and generate useful task templates. Present the results clearly to the user.

Use the PRD Analysis Agent for extracting information from PRDs.
Use the Codebase Scanner Agent for understanding existing projects.
Use the Template Generator Agent for creating XML templates.
Use the Sequence Planner Agent for arranging tasks in optimal order.""",
    tools=[
        agent_tool.AgentTool(agent=prd_analysis_agent),
        agent_tool.AgentTool(agent=codebase_scanner_agent),
        agent_tool.AgentTool(agent=template_generator_agent),
        agent_tool.AgentTool(agent=sequence_planner_agent),
    ],
)

# Create a runner for the main agent
main_agent_runner = create_runner(main_agent)


async def process_prd_async(prd_path: str, codebase_path: str = None) -> dict:
    """
    Process a PRD file asynchronously using the main Marvin agent.

    Args:
        prd_path: Path to the PRD file
        codebase_path: Optional path to the codebase directory

    Returns:
        Dict containing the processing results
    """
    # Validate inputs
    if not os.path.exists(prd_path):
        return {"status": "error", "error_message": f"PRD file not found: {prd_path}"}

    if codebase_path and not os.path.isdir(codebase_path):
        return {
            "status": "error",
            "error_message": f"Codebase directory not found: {codebase_path}",
        }

    # Create the message for the agent
    message_text = f"Please analyze the PRD at {prd_path}"
    if codebase_path:
        message_text += f" and consider the codebase at {codebase_path}"
    message_text += " to generate AI coding task templates."

    message = Content(role="user", parts=[Part(text=message_text)])

    # Run the agent and collect the events
    results = []
    async for event in main_agent_runner.run_async(
        user_id="marvin_user", session_id="main_agent_session", new_message=message
    ):
        # Store all event information for analysis
        if event.content and event.content.parts:
            results.append(event.content.parts[0].text)

    # Return the final results
    return {"status": "success", "results": results}


def process_prd(prd_path: str, codebase_path: str = None) -> dict:
    """
    Synchronous wrapper for process_prd_async.

    Args:
        prd_path: Path to the PRD file
        codebase_path: Optional path to the codebase directory

    Returns:
        Dict containing the processing results
    """
    return asyncio.run(process_prd_async(prd_path, codebase_path))
