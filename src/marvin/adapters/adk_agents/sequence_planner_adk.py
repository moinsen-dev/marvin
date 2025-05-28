"""ADK Agent for planning task sequences from PRD features."""

import json
import uuid
from datetime import datetime
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.sessions import Session
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from marvin.core.domain.models import PRD, Feature, Workflow


def analyze_feature_dependencies(
    features_data: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Analyzes feature dependencies to determine optimal task sequencing.

    Args:
        features_data: JSON string containing features with their dependencies
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with dependency analysis results
    """
    try:
        features = json.loads(features_data)
        dependency_graph = {}
        complexity_scores = {}

        # Create name-to-id mapping for dependency resolution
        name_to_id = {
            feature.get("name", ""): feature.get("id", "unknown")
            for feature in features
        }

        # Build dependency graph and calculate complexity
        for feature in features:
            feature_id = feature.get("id", "unknown")
            dependency_names = feature.get("dependencies", [])
            # Convert dependency names to IDs
            dependency_ids = [
                name_to_id.get(dep_name, dep_name) for dep_name in dependency_names
            ]
            requirements_count = len(feature.get("requirements", []))

            dependency_graph[feature_id] = {
                "name": feature.get("name", ""),
                "dependencies": dependency_ids,
                "requirements_count": requirements_count,
                "complexity": _calculate_complexity_score(feature),
            }
            complexity_scores[feature_id] = dependency_graph[feature_id]["complexity"]

        # Detect circular dependencies
        circular_deps = _detect_circular_dependencies(dependency_graph)

        # Calculate optimal sequence using topological sort
        sequence = _topological_sort(dependency_graph)

        result = {
            "dependency_graph": dependency_graph,
            "complexity_scores": complexity_scores,
            "circular_dependencies": circular_deps,
            "recommended_sequence": sequence,
            "analysis_timestamp": datetime.now().isoformat(),
        }

        # Store in session state for later use
        tool_context.state["last_dependency_analysis"] = result

        return result

    except Exception as e:
        return {"error": f"Failed to analyze dependencies: {str(e)}"}


def create_task_breakdown(
    feature_data: str, sequence_number: int, tool_context: ToolContext
) -> dict[str, Any]:
    """Creates detailed task breakdown for a specific feature.

    Args:
        feature_data: JSON string containing feature information
        sequence_number: The position of this task in the overall sequence
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with task breakdown details
    """
    try:
        feature = json.loads(feature_data)

        # Generate task breakdown based on feature complexity
        tasks = []
        base_task_id = f"task-{sequence_number:03d}"

        # Main implementation task
        main_task = {
            "task_id": base_task_id,
            "name": f"Implement {feature.get('name', 'Feature')}",
            "description": f"Implement the {feature.get('name', 'feature').lower()} with all requirements",
            "type": "implementation",
            "estimated_effort": _estimate_effort(feature),
            "priority": feature.get("priority", 0),
            "subtasks": _generate_subtasks(feature),
        }
        tasks.append(main_task)

        # Add testing task if feature is complex
        if _calculate_complexity_score(feature) > 3:
            test_task = {
                "task_id": f"{base_task_id}-test",
                "name": f"Test {feature.get('name', 'Feature')}",
                "description": f"Comprehensive testing for {feature.get('name', 'feature').lower()}",
                "type": "testing",
                "estimated_effort": "1-2 days",
                "depends_on": [base_task_id],
            }
            tasks.append(test_task)

        result = {
            "feature_id": feature.get("id"),
            "feature_name": feature.get("name"),
            "tasks": tasks,
            "breakdown_timestamp": datetime.now().isoformat(),
        }

        # Store breakdown in session state
        if "task_breakdowns" not in tool_context.state:
            tool_context.state["task_breakdowns"] = {}
        tool_context.state["task_breakdowns"][feature.get("id")] = result

        return result

    except Exception as e:
        return {"error": f"Failed to create task breakdown: {str(e)}"}


def validate_workflow_feasibility(
    workflow_data: str, tool_context: ToolContext
) -> dict[str, Any]:
    """Validates the feasibility of a proposed workflow.

    Args:
        workflow_data: JSON string containing workflow information
        tool_context: ADK tool context for state management

    Returns:
        Dictionary with validation results
    """
    try:
        workflow = json.loads(workflow_data)

        issues: list[str] = []
        warnings: list[str] = []
        recommendations: list[str] = []

        validation_results = {
            "is_feasible": True,
            "issues": issues,
            "warnings": warnings,
            "recommendations": recommendations,
            "estimated_timeline": "",
            "risk_assessment": "",
        }

        tasks = workflow.get("tasks", [])

        # Check for dependency violations
        task_ids = {task.get("task_id") for task in tasks}
        for task in tasks:
            for dep in task.get("depends_on", []):
                if dep not in task_ids:
                    issues.append(
                        f"Task {task.get('task_id')} depends on non-existent task {dep}"
                    )
                    validation_results["is_feasible"] = False

        # Check for resource conflicts
        parallel_tasks = _identify_parallel_tasks(tasks)
        if len(parallel_tasks) > 3:
            warnings.append(
                f"High parallelism detected ({len(parallel_tasks)} concurrent tasks). Consider resource allocation."
            )

        # Estimate timeline
        timeline = _estimate_workflow_timeline(tasks)
        validation_results["estimated_timeline"] = timeline

        # Risk assessment
        risk_level = _assess_workflow_risk(tasks)
        validation_results["risk_assessment"] = risk_level

        # Generate recommendations
        recommendations.extend(
            _generate_workflow_recommendations(tasks, validation_results)
        )

        # Store validation in session state
        tool_context.state["last_workflow_validation"] = validation_results

        return validation_results

    except Exception as e:
        return {"error": f"Failed to validate workflow: {str(e)}"}


def _calculate_complexity_score(feature: dict[str, Any]) -> int:
    """Calculate complexity score for a feature based on various factors."""
    score = 0

    # Base score from requirements count
    requirements = feature.get("requirements", [])
    score += len(requirements)

    # Dependency complexity
    dependencies = feature.get("dependencies", [])
    score += len(dependencies) * 2

    # Priority factor (higher priority = potentially more complex)
    priority = feature.get("priority", 0)
    if priority == 0:  # High priority
        score += 3
    elif priority == 1:  # Medium priority
        score += 2

    # Additional complexity factors
    description = feature.get("description", "")
    if any(
        keyword in description.lower()
        for keyword in ["integration", "api", "security", "performance"]
    ):
        score += 2

    return min(score, 10)  # Cap at 10


def _detect_circular_dependencies(dependency_graph: dict[str, Any]) -> list[str]:
    """Detect circular dependencies in the feature graph."""
    visited = set()
    rec_stack = set()
    circular_deps = []

    def has_cycle(node, path):
        if node in rec_stack:
            cycle_start = path.index(node)
            circular_deps.append(" -> ".join(path[cycle_start:] + [node]))
            return True

        if node in visited:
            return False

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in dependency_graph.get(node, {}).get("dependencies", []):
            if neighbor in dependency_graph and has_cycle(neighbor, path.copy()):
                return True

        rec_stack.remove(node)
        return False

    for node in dependency_graph:
        if node not in visited:
            has_cycle(node, [])

    return circular_deps


def _topological_sort(dependency_graph: dict[str, Any]) -> list[str]:
    """Perform topological sort to determine optimal sequence."""
    in_degree = dict.fromkeys(dependency_graph, 0)

    # Calculate in-degrees (count dependencies pointing to each node)
    for node in dependency_graph:
        in_degree[node] = len(dependency_graph[node].get("dependencies", []))

    # Queue for nodes with no dependencies
    queue = [node for node, degree in in_degree.items() if degree == 0]
    result = []

    while queue:
        # Sort by complexity to prioritize simpler tasks first
        queue.sort(key=lambda x: dependency_graph[x].get("complexity", 0))
        current = queue.pop(0)
        result.append(current)

        # Update in-degrees of dependent nodes
        for node in dependency_graph:
            if current in dependency_graph[node].get("dependencies", []):
                in_degree[node] -= 1
                if in_degree[node] == 0:
                    queue.append(node)

    return result


def _estimate_effort(feature: dict[str, Any]) -> str:
    """Estimate effort required for implementing a feature."""
    complexity = _calculate_complexity_score(feature)

    if complexity <= 2:
        return "1-2 days"
    elif complexity <= 4:
        return "3-5 days"
    elif complexity <= 6:
        return "1-2 weeks"
    elif complexity <= 8:
        return "2-3 weeks"
    else:
        return "3-4 weeks"


def _generate_subtasks(feature: dict[str, Any]) -> list[dict[str, str]]:
    """Generate detailed subtasks for a feature."""
    subtasks = []
    requirements = feature.get("requirements", [])

    # Core implementation subtasks
    subtasks.append(
        {
            "name": "Design and Architecture",
            "description": f"Design the architecture for {feature.get('name', 'feature')}",
            "estimated_effort": "0.5-1 day",
        }
    )

    # Requirement-based subtasks
    for _i, req in enumerate(requirements[:5]):  # Limit to first 5 requirements
        subtasks.append(
            {
                "name": f"Implement: {req[:50]}...",
                "description": f"Implement requirement: {req}",
                "estimated_effort": "1-2 days",
            }
        )

    # Testing and validation
    subtasks.append(
        {
            "name": "Testing and Validation",
            "description": f"Comprehensive testing for {feature.get('name', 'feature')}",
            "estimated_effort": "1-2 days",
        }
    )

    return subtasks


def _identify_parallel_tasks(tasks: list[dict[str, Any]]) -> list[str]:
    """Identify tasks that can run in parallel."""
    parallel_tasks = []
    task_deps = {}

    # Build dependency map
    for task in tasks:
        task_id = task.get("task_id")
        deps = task.get("depends_on", [])
        task_deps[task_id] = set(deps)

    # Find tasks with no dependencies or non-conflicting dependencies
    for task in tasks:
        task_id = task.get("task_id")
        if not task_deps[task_id]:  # No dependencies
            parallel_tasks.append(task_id)

    return parallel_tasks


def _estimate_workflow_timeline(tasks: list[dict[str, Any]]) -> str:
    """Estimate total timeline for workflow completion."""
    # Simplified timeline estimation
    total_tasks = len(tasks)

    if total_tasks <= 3:
        return "1-2 weeks"
    elif total_tasks <= 6:
        return "3-4 weeks"
    elif total_tasks <= 10:
        return "1-2 months"
    else:
        return "2-3 months"


def _assess_workflow_risk(tasks: list[dict[str, Any]]) -> str:
    """Assess risk level of the workflow."""
    risk_factors = 0

    # Check for complex dependencies
    total_deps = sum(len(task.get("depends_on", [])) for task in tasks)
    if total_deps > len(tasks):
        risk_factors += 1

    # Check for high complexity tasks
    complex_tasks = sum(
        1 for task in tasks if "weeks" in task.get("estimated_effort", "")
    )
    if complex_tasks > len(tasks) * 0.3:
        risk_factors += 1

    # Check for large number of tasks
    if len(tasks) > 8:
        risk_factors += 1

    if risk_factors >= 2:
        return "High - Multiple risk factors identified"
    elif risk_factors == 1:
        return "Medium - Some complexity factors present"
    else:
        return "Low - Well-structured workflow"


def _generate_workflow_recommendations(
    tasks: list[dict[str, Any]], validation_results: dict[str, Any]
) -> list[str]:
    """Generate recommendations for workflow optimization."""
    recommendations = []

    if validation_results.get("issues"):
        recommendations.append("Resolve dependency issues before proceeding")

    if len(tasks) > 8:
        recommendations.append("Consider breaking down into smaller, manageable phases")

    if "High" in validation_results.get("risk_assessment", ""):
        recommendations.append("Implement additional checkpoints and reviews")
        recommendations.append("Consider parallel execution where possible")

    parallel_tasks = _identify_parallel_tasks(tasks)
    if len(parallel_tasks) > 1:
        recommendations.append(
            f"Execute {len(parallel_tasks)} tasks in parallel to optimize timeline"
        )

    return recommendations


# Validation callback for sequence planning
def sequence_planning_validator(
    context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """Validates sequence planning requests for safety and feasibility."""
    # Extract user input
    last_user_message = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                if content.parts[0].text:
                    last_user_message = content.parts[0].text
                    break

    # Check for suspicious patterns
    suspicious_patterns = [
        "delete all",
        "remove everything",
        "bypass validation",
        "skip dependencies",
    ]

    for pattern in suspicious_patterns:
        if pattern.lower() in last_user_message.lower():
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text="I cannot process requests that might compromise workflow integrity. Please provide a valid sequence planning request."
                        )
                    ],
                )
            )

    return None


class SequencePlannerADKAgent(LlmAgent):
    """
    ADK Agent for intelligent task sequence planning from PRD features.

    This agent analyzes features and their dependencies to create optimal
    task sequences, considering complexity, dependencies, and resource constraints.
    """

    def __init__(
        self,
        name: str = "marvin_sequence_planner_adk",
        model: str = "gemini-1.5-pro",
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Initialize the SequencePlannerADKAgent.

        Args:
            name: Name of the agent
            model: The LLM model to use
            config: Optional configuration dictionary
            **kwargs: Additional arguments for LlmAgent
        """
        # Comprehensive instruction for sequence planning
        instruction = """You are an expert project management and software development planning agent specializing in creating optimal task sequences from Product Requirements Documents (PRDs).

Your primary responsibilities:

1. **Dependency Analysis**: Analyze feature dependencies to identify the optimal implementation order
2. **Task Breakdown**: Break down features into manageable, actionable tasks
3. **Workflow Planning**: Create comprehensive workflows with proper sequencing
4. **Risk Assessment**: Identify potential bottlenecks and risks in the planned sequence
5. **Timeline Estimation**: Provide realistic timeline estimates for task completion

**CRITICAL GUIDELINES:**

- ALWAYS use the provided tools for analysis and validation
- Consider both technical dependencies and logical implementation order
- Account for team capacity and resource constraints
- Identify opportunities for parallel execution
- Flag circular dependencies and propose resolutions
- Provide detailed rationale for sequencing decisions

**OUTPUT FORMAT:**
Always structure your responses as JSON with the following sections:
- `workflow_overview`: High-level workflow description
- `task_sequence`: Ordered list of tasks with dependencies
- `risk_analysis`: Identified risks and mitigation strategies
- `timeline_estimate`: Overall timeline with milestones
- `recommendations`: Specific recommendations for optimization

**TOOL USAGE:**
1. Start with `analyze_feature_dependencies` to understand the dependency graph
2. Use `create_task_breakdown` for each feature to get detailed tasks
3. Validate the final workflow with `validate_workflow_feasibility`

Be thorough, considerate of real-world constraints, and always prioritize deliverable, testable increments."""

        super().__init__(
            name=name,
            model=model,
            instruction=instruction,
            description="Expert sequence planning agent that creates optimal task workflows from PRD features, considering dependencies, complexity, and resource constraints.",
            tools=[
                analyze_feature_dependencies,
                create_task_breakdown,
                validate_workflow_feasibility,
            ],
            before_model_callback=sequence_planning_validator,
            output_key="last_sequence_plan",  # Auto-save plans to session state
            **kwargs,
        )

    def create_workflow_from_features(
        self, features: list[Feature], prd: PRD, session: Session
    ) -> Workflow:
        """Create a complete workflow from analyzed features.

        Args:
            features: List of extracted features
            prd: The PRD document
            session: ADK session for state management

        Returns:
            Complete workflow with sequenced tasks
        """
        # Creating workflow from features

        # Convert features to JSON for agent processing
        features_data = [
            {
                "id": feature.id,
                "name": feature.name,
                "description": feature.description,
                "requirements": feature.requirements,
                "dependencies": feature.dependencies,
                "priority": feature.priority,
            }
            for feature in features
        ]

        # Create workflow
        workflow = Workflow(
            id=str(uuid.uuid4()),
            name=f"Implementation Workflow for {prd.title}",
            description=f"Automatically generated workflow for implementing {prd.title} features",
            prd_id=prd.id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # The agent will handle the detailed planning through its tools
        # This method provides the framework for integration
        session.state["current_workflow"] = {
            "workflow_id": workflow.id,
            "features_data": features_data,
            "prd_data": {
                "id": prd.id,
                "title": prd.title,
                "description": prd.description,
                "author": prd.author,
            },
        }

        return workflow

    def get_planning_capabilities(self) -> dict[str, Any]:
        """Get information about the agent's planning capabilities."""
        return {
            "supported_features": [
                "Dependency analysis and resolution",
                "Task breakdown and estimation",
                "Workflow validation and optimization",
                "Risk assessment and mitigation",
                "Timeline estimation and milestone planning",
                "Parallel execution identification",
                "Resource constraint consideration",
            ],
            "analysis_tools": [
                "analyze_feature_dependencies",
                "create_task_breakdown",
                "validate_workflow_feasibility",
            ],
            "output_formats": [
                "JSON workflow",
                "Gantt chart data",
                "Dependency graphs",
            ],
            "risk_factors_considered": [
                "Circular dependencies",
                "Resource conflicts",
                "Complexity overload",
                "Timeline feasibility",
                "Technical debt",
            ],
        }
