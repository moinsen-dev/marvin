"""
PRD Analysis Agent.

This agent is responsible for analyzing Product Requirements Documents (PRDs)
and extracting features, requirements, and dependencies.
"""

import os
from typing import Any

from google.adk.agents import Agent
from google.genai.types import Content, Part

from marvin.agents.base import MODEL_GEMINI_2_0_PRO, create_runner


def extract_prd_content(prd_path: str) -> str:
    """
    Extract the content of a PRD file.

    Args:
        prd_path: Path to the PRD file

    Returns:
        Content of the PRD file as string
    """
    if not os.path.exists(prd_path):
        raise FileNotFoundError(f"PRD file not found at {prd_path}")

    with open(prd_path) as f:
        return f.read()


def analyze_prd(prd_content: str, tool_context: Any = None) -> dict:
    """
    Analyze a PRD and extract features, requirements, and dependencies.

    Args:
        prd_content: Content of the PRD to analyze
        tool_context: Tool context provided by ADK (not used here)

    Returns:
        Dict containing extracted information
    """
    # This would typically call an external API or perform complex analysis
    # For now, we'll return a simple placeholder
    return {
        "status": "success",
        "features": ["Feature 1", "Feature 2"],
        "requirements": ["Req 1", "Req 2"],
        "dependencies": {"Feature 1": ["Req 1"], "Feature 2": ["Req 2"]},
    }


# Create the PRD analysis agent
prd_analysis_agent = Agent(
    name="prd_analysis_agent",
    model=MODEL_GEMINI_2_0_PRO,
    description="Analyzes Product Requirements Documents (PRDs) to extract features, requirements, and dependencies",
    instruction="""You are a PRD analysis specialist. Your job is to analyze Product Requirements Documents (PRDs)
and extract features, requirements, and dependencies. When a user provides a PRD, use the analyze_prd tool
to extract the relevant information. Present the results clearly to the user, highlighting key features and requirements.""",
    tools=[analyze_prd],
)

# Create a runner for the agent
prd_analysis_runner = create_runner(prd_analysis_agent)


async def analyze_prd_async(prd_path: str) -> dict:
    """
    Analyze a PRD file asynchronously using the PRD analysis agent.

    Args:
        prd_path: Path to the PRD file

    Returns:
        Dict containing the analysis results
    """
    # Extract PRD content
    prd_content = extract_prd_content(prd_path)

    # Create user message with PRD content
    message = Content(
        role="user", parts=[Part(text=f"Please analyze this PRD:\n\n{prd_content}")]
    )

    # Run the agent and collect the final response
    final_response = None
    async for event in prd_analysis_runner.run_async(
        user_id="marvin_user", session_id="prd_analysis_session", new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    # Return the analysis results
    return {"status": "success", "analysis": final_response or "No analysis produced"}
