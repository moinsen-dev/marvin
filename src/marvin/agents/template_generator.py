"""
Template Generation Agent.

This agent is responsible for creating XML-based task templates
for AI coding assistants based on PRD analysis and codebase scanning results.
"""

import uuid
import xml.dom.minidom
import xml.etree.ElementTree as ET
from typing import Any

from google.adk.agents import Agent
from google.genai.types import Content, Part

from marvin.agents.base import MODEL_GEMINI_2_0_PRO, create_runner


def generate_task_id(feature_name: str) -> str:
    """
    Generate a task ID from a feature name.

    Args:
        feature_name: Name of the feature

    Returns:
        Task ID in the format FEATURE-UUID
    """
    # Normalize feature name (remove spaces, lowercase)
    normalized = feature_name.replace(" ", "_").lower()

    # Generate a short UUID
    short_uuid = str(uuid.uuid4())[:8]

    return f"{normalized}-{short_uuid}"


def create_task_template(
    feature: str,
    requirements: list[str],
    dependencies: list[str] = None,
    tool_context: Any = None,
) -> dict:
    """
    Create an XML task template for an AI coding assistant.

    Args:
        feature: Feature name
        requirements: List of requirements for the feature
        dependencies: List of dependencies (optional)
        tool_context: Tool context provided by ADK (not used here)

    Returns:
        Dict containing the task template
    """
    try:
        # Generate task ID
        task_id = generate_task_id(feature)

        # Create XML structure
        root = ET.Element("task")
        root.set("id", task_id)

        # Add feature information
        feature_elem = ET.SubElement(root, "feature")
        feature_elem.text = feature

        # Add requirements
        reqs_elem = ET.SubElement(root, "requirements")
        for req in requirements:
            req_elem = ET.SubElement(reqs_elem, "requirement")
            req_elem.text = req

        # Add dependencies if provided
        if dependencies:
            deps_elem = ET.SubElement(root, "dependencies")
            for dep in dependencies:
                dep_elem = ET.SubElement(deps_elem, "dependency")
                dep_elem.text = dep

        # Convert to pretty-printed XML string
        xml_str = ET.tostring(root, encoding="unicode")
        pretty_xml = xml.dom.minidom.parseString(xml_str).toprettyxml(indent="  ")

        return {"status": "success", "task_id": task_id, "template": pretty_xml}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# Create the template generation agent
template_generator_agent = Agent(
    name="template_generator_agent",
    model=MODEL_GEMINI_2_0_PRO,
    description="Creates XML-based task templates for AI coding assistants based on PRD analysis",
    instruction="""You are a template generation specialist. Your job is to create XML-based task templates
for AI coding assistants based on PRD analysis results. When given feature information, requirements,
and dependencies, use the create_task_template tool to generate appropriate XML templates.
Present the results clearly to the user, explaining how the template can be used with AI coding assistants.""",
    tools=[create_task_template],
)

# Create a runner for the agent
template_generator_runner = create_runner(template_generator_agent)


async def generate_templates_async(analysis_results: dict) -> dict:
    """
    Generate task templates asynchronously using the template generator agent.

    Args:
        analysis_results: Results from PRD analysis

    Returns:
        Dict containing the generated templates
    """
    # Extract data from analysis results
    features = analysis_results.get("features", [])
    requirements = analysis_results.get("requirements", [])
    dependencies = analysis_results.get("dependencies", {})

    # Create a message for the agent
    message_text = f"""Please generate XML task templates for the following features:

Features: {", ".join(features)}
Requirements: {", ".join(requirements)}
Dependencies: {dependencies}

Please create an XML template for each feature."""

    message = Content(role="user", parts=[Part(text=message_text)])

    # Run the agent and collect the final response
    final_response = None
    async for event in template_generator_runner.run_async(
        user_id="marvin_user",
        session_id="template_generator_session",
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    # Return the templates
    return {"status": "success", "templates": final_response or "No templates produced"}
