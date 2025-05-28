"""ADK Orchestrator Agent for coordinating the complete Marvin workflow."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import Session
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from marvin.adapters.adk_agents.document_analyzer_adk import DocumentAnalyzerADKAgent
from marvin.adapters.adk_agents.sequence_planner_adk import SequencePlannerADKAgent
from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.domain.models import Task
from marvin.infrastructure.template_generator.xml_generator import XMLTemplateGenerator


def analyze_prd_document(
    document_path: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Analyze a PRD document to extract features and metadata.

    Args:
        document_path: Path to the PRD document
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with analysis results including PRD and features
    """
    try:
        # Use our core DocumentAnalysisAgent for robust parsing
        analyzer = DocumentAnalysisAgent()

        # Perform analysis
        import asyncio

        prd, features = asyncio.run(analyzer.execute(document_path))

        # Convert to serializable format
        result = {
            "success": True,
            "prd": {
                "id": prd.id,
                "title": prd.title,
                "description": prd.description,
                "author": prd.author,
                "version": prd.version,
                "created_at": prd.created_at.isoformat(),
                "updated_at": prd.updated_at.isoformat(),
            },
            "features": [
                {
                    "id": feature.id,
                    "name": feature.name,
                    "description": feature.description,
                    "requirements": feature.requirements,
                    "dependencies": feature.dependencies,
                    "priority": feature.priority,
                    "status": feature.status.value,
                    "estimated_effort": feature.estimated_effort,
                    "tags": feature.tags,
                }
                for feature in features
            ],
            "analysis_timestamp": datetime.now().isoformat(),
            "document_path": document_path,
        }

        # Store in session state
        tool_context.state["last_prd_analysis"] = result
        tool_context.state["current_prd"] = result["prd"]
        tool_context.state["current_features"] = result["features"]

        return result

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "document_path": document_path,
            "analysis_timestamp": datetime.now().isoformat(),
        }
        tool_context.state["last_analysis_error"] = error_result
        return error_result


def generate_xml_templates(
    features_data: str, prd_data: str, output_directory: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Generate XML templates for all features.

    Args:
        features_data: JSON string containing features data
        prd_data: JSON string containing PRD data
        output_directory: Directory to save XML templates
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with generation results
    """
    try:
        features = json.loads(features_data)
        prd = json.loads(prd_data)

        # Initialize XML generator
        xml_generator = XMLTemplateGenerator()

        # Ensure output directory exists
        output_path = Path(output_directory)
        output_path.mkdir(parents=True, exist_ok=True)

        generated_templates = []

        # Generate template for each feature
        for i, feature_data in enumerate(features):
            # Create Task and Feature objects
            task = Task(
                task_id=f"task-{i + 1:03d}",
                sequence_number=i + 1,
                name=f"Implement {feature_data['name']}",
                description=f"Implement the {feature_data['name'].lower()} feature with all requirements",
                feature_id=feature_data["id"],
                depends_on=[],  # Will be determined by sequence planner
            )

            from marvin.core.domain.models import Feature, FeatureStatus

            feature = Feature(
                id=feature_data["id"],
                name=feature_data["name"],
                description=feature_data["description"],
                requirements=feature_data["requirements"],
                dependencies=feature_data["dependencies"],
                priority=feature_data["priority"],
                status=FeatureStatus(feature_data["status"]),
            )

            # Reconstruct PRD object
            from marvin.core.domain.models import PRD

            prd_obj = PRD(
                id=prd["id"],
                title=prd["title"],
                description=prd["description"],
                author=prd["author"],
                version=prd["version"],
                created_at=datetime.fromisoformat(prd["created_at"]),
                updated_at=datetime.fromisoformat(prd["updated_at"]),
            )

            # Generate XML template
            xml_content = xml_generator.generate_task_template(
                task=task,
                feature=feature,
                prd=prd_obj,
            )

            # Save to file
            template_filename = f"{task.task_id}_{feature.id}.xml"
            template_path = output_path / template_filename

            xml_generator.save_to_file(xml_content, str(template_path))

            # Validate generated XML
            is_valid, error = xml_generator.validate_xml(xml_content)

            generated_templates.append(
                {
                    "task_id": task.task_id,
                    "feature_id": feature.id,
                    "feature_name": feature.name,
                    "template_path": str(template_path),
                    "is_valid": is_valid,
                    "validation_error": error,
                    "file_size": len(xml_content),
                }
            )

        result = {
            "success": True,
            "templates_generated": len(generated_templates),
            "output_directory": str(output_path),
            "templates": generated_templates,
            "generation_timestamp": datetime.now().isoformat(),
        }

        # Store in session state
        tool_context.state["last_template_generation"] = result
        tool_context.state["generated_templates"] = generated_templates

        return result

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "output_directory": output_directory,
            "generation_timestamp": datetime.now().isoformat(),
        }
        tool_context.state["last_generation_error"] = error_result
        return error_result


def create_project_workflow(
    features_data: str, prd_data: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Create a comprehensive project workflow from analyzed features.

    Args:
        features_data: JSON string containing features data
        prd_data: JSON string containing PRD data
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with workflow creation results
    """
    try:
        features = json.loads(features_data)
        prd = json.loads(prd_data)

        # Create workflow structure
        workflow_id = str(uuid.uuid4())
        workflow = {
            "id": workflow_id,
            "name": f"Implementation Workflow for {prd['title']}",
            "description": f"Comprehensive workflow for implementing {prd['title']} with {len(features)} features",
            "prd_id": prd["id"],
            "created_at": datetime.now().isoformat(),
            "phases": [],
            "estimated_timeline": "",
            "risk_assessment": "",
        }

        # Organize features into phases based on dependencies and complexity
        phases = _organize_features_into_phases(features)

        for phase_num, phase_features in enumerate(phases, 1):
            phase = {
                "phase_number": phase_num,
                "name": f"Phase {phase_num}",
                "description": f"Implementation phase {phase_num} with {len(phase_features)} features",
                "features": phase_features,
                "estimated_duration": _estimate_phase_duration(phase_features),
                "deliverables": [
                    f"Complete {feature['name']}" for feature in phase_features
                ],
            }
            workflow["phases"].append(phase)

        # Calculate overall timeline
        total_duration = sum(
            _parse_duration(phase["estimated_duration"]) for phase in workflow["phases"]
        )
        workflow["estimated_timeline"] = f"{total_duration} weeks"

        # Assess risks
        workflow["risk_assessment"] = _assess_project_risks(features, phases)

        result = {
            "success": True,
            "workflow": workflow,
            "phases_count": len(phases),
            "total_features": len(features),
            "creation_timestamp": datetime.now().isoformat(),
        }

        # Store in session state
        tool_context.state["project_workflow"] = result
        tool_context.state["current_workflow_id"] = workflow_id

        return result

    except Exception as e:
        error_result = {
            "success": False,
            "error": str(e),
            "creation_timestamp": datetime.now().isoformat(),
        }
        tool_context.state["last_workflow_error"] = error_result
        return error_result


def generate_project_summary(tool_context: ToolContext) -> dict[str, Any]:
    """Generate a comprehensive project summary from session state.

    Args:
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with project summary
    """
    try:
        state = tool_context.state

        # Extract data from session state
        prd_analysis = state.get("last_prd_analysis", {})
        template_generation = state.get("last_template_generation", {})
        workflow = state.get("project_workflow", {})

        # Build comprehensive summary
        summary = {
            "project_overview": {
                "name": prd_analysis.get("prd", {}).get("title", "Unknown Project"),
                "author": prd_analysis.get("prd", {}).get("author", "Unknown"),
                "version": prd_analysis.get("prd", {}).get("version", "1.0.0"),
                "features_count": len(prd_analysis.get("features", [])),
                "analysis_date": prd_analysis.get("analysis_timestamp", ""),
            },
            "implementation_plan": {
                "phases_count": workflow.get("phases_count", 0),
                "estimated_timeline": workflow.get("workflow", {}).get(
                    "estimated_timeline", ""
                ),
                "risk_level": workflow.get("workflow", {}).get("risk_assessment", ""),
            },
            "deliverables": {
                "templates_generated": template_generation.get(
                    "templates_generated", 0
                ),
                "output_directory": template_generation.get("output_directory", ""),
                "all_templates_valid": all(
                    t.get("is_valid", False)
                    for t in template_generation.get("templates", [])
                ),
            },
            "next_steps": _generate_next_steps(state),
            "summary_timestamp": datetime.now().isoformat(),
        }

        # Store summary in session state
        tool_context.state["project_summary"] = summary

        return {
            "success": True,
            "summary": summary,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "summary_timestamp": datetime.now().isoformat(),
        }


def _organize_features_into_phases(
    features: list[dict[str, Any]],
) -> list[list[dict[str, Any]]]:
    """Organize features into implementation phases based on dependencies."""
    phases = []
    remaining_features = features.copy()
    implemented_features: set[str] = set()

    while remaining_features:
        current_phase = []

        # Find features with no unresolved dependencies
        for feature in remaining_features.copy():
            dependencies = set(feature.get("dependencies", []))
            if dependencies.issubset(implemented_features) or not dependencies:
                current_phase.append(feature)
                remaining_features.remove(feature)
                implemented_features.add(feature["name"])

        # If no features can be added, force add the simplest one to break deadlock
        if not current_phase and remaining_features:
            simplest = min(
                remaining_features, key=lambda f: len(f.get("requirements", []))
            )
            current_phase.append(simplest)
            remaining_features.remove(simplest)
            implemented_features.add(simplest["name"])

        if current_phase:
            phases.append(current_phase)

    return phases


def _estimate_phase_duration(features: list[dict[str, Any]]) -> str:
    """Estimate duration for a phase based on feature complexity."""
    total_complexity = sum(len(f.get("requirements", [])) for f in features)

    if total_complexity <= 5:
        return "1-2 weeks"
    elif total_complexity <= 10:
        return "2-3 weeks"
    elif total_complexity <= 15:
        return "3-4 weeks"
    else:
        return "4-6 weeks"


def _parse_duration(duration_str: str) -> int:
    """Parse duration string to weeks (simplified)."""
    if "1-2 weeks" in duration_str:
        return 2
    elif "2-3 weeks" in duration_str:
        return 3
    elif "3-4 weeks" in duration_str:
        return 4
    elif "4-6 weeks" in duration_str:
        return 5
    else:
        return 2


def _assess_project_risks(
    features: list[dict[str, Any]], phases: list[list[dict[str, Any]]]
) -> str:
    """Assess overall project risk level."""
    risk_factors = 0

    # Complex features
    complex_features = sum(1 for f in features if len(f.get("requirements", [])) > 5)
    if complex_features > len(features) * 0.3:
        risk_factors += 1

    # Many dependencies
    total_deps = sum(len(f.get("dependencies", [])) for f in features)
    if total_deps > len(features):
        risk_factors += 1

    # Many phases
    if len(phases) > 4:
        risk_factors += 1

    # Large number of features
    if len(features) > 8:
        risk_factors += 1

    if risk_factors >= 3:
        return "High Risk - Complex project requiring careful management"
    elif risk_factors >= 2:
        return "Medium Risk - Some complexity factors present"
    else:
        return "Low Risk - Well-structured project"


def _generate_next_steps(state: dict[str, Any]) -> list[str]:
    """Generate recommended next steps based on current state."""
    next_steps = []

    if state.get("generated_templates"):
        next_steps.append("Review generated XML templates for accuracy")
        next_steps.append(
            "Validate templates with your AI coding assistant (Cursor, Windsurf, etc.)"
        )

    if state.get("project_workflow"):
        next_steps.append("Review the proposed implementation phases")
        next_steps.append("Adjust timeline based on team capacity")
        next_steps.append("Set up project tracking and milestones")

    if state.get("last_prd_analysis"):
        next_steps.append("Begin implementation with Phase 1 features")
        next_steps.append("Set up development environment and repository")
        next_steps.append("Schedule regular check-ins and reviews")

    return next_steps


# Security and validation callback
def orchestrator_security_callback(
    _context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """Security callback for the orchestrator agent."""
    # Extract user input
    user_input = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                if content.parts[0].text:
                    user_input = content.parts[0].text
                    break

    # Security checks
    dangerous_patterns = [
        "rm -rf",
        "delete all",
        "../",
        "system(",
        "exec(",
        "eval(",
        "__import__",
    ]

    for pattern in dangerous_patterns:
        if pattern in user_input.lower():
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="I cannot process requests that contain potentially dangerous operations. Please provide a safe request for PRD analysis and template generation."
                        )
                    ],
                )
            )

    return None


class MarvinOrchestratorADKAgent(LlmAgent):
    """
    Master orchestrator agent for the complete Marvin workflow.

    Coordinates PRD analysis, sequence planning, and XML template generation
    using a team of specialized sub-agents and tools.
    """

    def __init__(
        self,
        name: str = "marvin_orchestrator_adk",
        model: str = "gemini-1.5-pro",
        _config: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Initialize the MarvinOrchestratorADKAgent.

        Args:
            name: Name of the orchestrator agent
            model: The LLM model to use
            config: Optional configuration dictionary
            **kwargs: Additional arguments for LlmAgent
        """
        # Comprehensive orchestrator instruction
        instruction = """You are Marvin, the master orchestrator for intelligent PRD-to-Template conversion workflows. You coordinate a team of specialized agents to transform Product Requirements Documents into structured AI coding tasks.

**YOUR MISSION:**
Transform PRDs into actionable, well-sequenced development workflows with XML templates that AI coding assistants (Cursor, Windsurf, Claude Code) can execute.

**WORKFLOW STEPS:**

1. **PRD Analysis**: Use `analyze_prd_document` to extract features, requirements, and metadata
2. **Workflow Planning**: Use `create_project_workflow` to organize features into logical phases
3. **Template Generation**: Use `generate_xml_templates` to create AI-ready task templates
4. **Summary Creation**: Use `generate_project_summary` to provide comprehensive project overview

**CRITICAL GUIDELINES:**

- ALWAYS use tools in the correct sequence: analyze → plan → generate → summarize
- Validate all outputs and check for errors at each step
- Provide clear status updates throughout the process
- If any step fails, analyze the error and provide solutions
- Store all results in session state for continuity
- Be proactive in identifying potential issues

**OUTPUT PHILOSOPHY:**
- Actionable over theoretical
- Specific over general
- Validated over assumed
- User-friendly over technical

**RESPONSE STRUCTURE:**
Always provide:
1. **Status Update**: Current step and progress
2. **Action Taken**: What tool was used and why
3. **Results Summary**: Key findings and outputs
4. **Next Steps**: What's happening next
5. **Issues/Recommendations**: Any problems or suggestions

**PERSONALITY:**
Be professional, thorough, and solution-oriented. Think like a senior project manager who deeply understands both product requirements and development workflows.

Remember: You're not just processing documents - you're enabling teams to build amazing products efficiently."""

        # Initialize sub-agents
        document_analyzer = DocumentAnalyzerADKAgent(
            name="document_analyzer_sub",
            model="gemini-1.5-flash",  # Faster model for sub-agent
        )

        sequence_planner = SequencePlannerADKAgent(
            name="sequence_planner_sub",
            model="gemini-1.5-pro",  # More sophisticated model for planning
        )

        super().__init__(
            name=name,
            model=model,
            instruction=instruction,
            description="Master orchestrator that coordinates PRD analysis, sequence planning, and XML template generation through specialized sub-agents and tools.",
            tools=[
                analyze_prd_document,
                generate_xml_templates,
                create_project_workflow,
                generate_project_summary,
            ],
            sub_agents=[document_analyzer, sequence_planner],
            before_model_callback=orchestrator_security_callback,
            output_key="marvin_workflow_result",  # Store complete workflow results
            **kwargs,
        )

    def get_orchestrator_capabilities(self) -> dict[str, Any]:
        """Get comprehensive information about orchestrator capabilities."""
        return {
            "workflow_steps": [
                "PRD document analysis and feature extraction",
                "Intelligent sequence planning with dependency analysis",
                "XML template generation for AI coding assistants",
                "Comprehensive project workflow creation",
                "Risk assessment and timeline estimation",
                "Project summary and next steps generation",
            ],
            "supported_formats": {
                "input": [
                    "Markdown PRDs",
                    "Word documents (future)",
                    "PDF documents (future)",
                ],
                "output": ["XML templates", "JSON workflows", "Project summaries"],
            },
            "ai_assistants_supported": [
                "Cursor AI",
                "Windsurf",
                "Claude Code",
                "GitHub Copilot",
                "Any XML-compatible AI coding assistant",
            ],
            "sub_agents": [
                {
                    "name": "DocumentAnalyzer",
                    "purpose": "Extract features and requirements from PRDs",
                    "capabilities": [
                        "Markdown parsing",
                        "Feature extraction",
                        "Dependency analysis",
                    ],
                },
                {
                    "name": "SequencePlanner",
                    "purpose": "Create optimal task sequences",
                    "capabilities": [
                        "Dependency resolution",
                        "Timeline estimation",
                        "Risk assessment",
                    ],
                },
            ],
            "tools": [
                "analyze_prd_document",
                "create_project_workflow",
                "generate_xml_templates",
                "generate_project_summary",
            ],
            "safety_features": [
                "Content filtering for sensitive data",
                "Path traversal protection",
                "Command injection prevention",
                "Workflow validation",
            ],
        }

    def process_prd_complete(
        self,
        document_path: str,
        output_directory: str,
        session: Session,
        custom_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Process a PRD through the complete Marvin workflow.

        This is a convenience method that can be called directly
        for programmatic workflow execution.

        Args:
            document_path: Path to PRD document
            output_directory: Directory for generated templates
            session: ADK session for state management
            custom_config: Optional custom configuration

        Returns:
            Complete workflow results
        """
        try:
            # Starting complete PRD processing

            # Store initial parameters in session
            session.state.update(
                {
                    "input_document": document_path,
                    "output_directory": output_directory,
                    "custom_config": custom_config or {},
                    "workflow_start_time": datetime.now().isoformat(),
                }
            )

            # This method sets up the context for the agent to work with
            # The actual processing will be done through agent interactions

            return {
                "status": "initialized",
                "document_path": document_path,
                "output_directory": output_directory,
                "session_id": session.id if hasattr(session, "id") else "unknown",
                "message": "Workflow initialized. Interact with the agent to begin processing.",
            }

        except Exception as e:
            # Failed to initialize workflow
            return {
                "status": "error",
                "error": str(e),
                "document_path": document_path,
            }
