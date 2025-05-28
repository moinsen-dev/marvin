"""
Sequence Planning Agent.

This agent is responsible for planning optimal implementation sequences
based on task dependencies, resolving conflicts, and arranging tasks
in the most efficient order.
"""

from typing import Any, Dict, List

import networkx as nx
from google.adk.agents import Agent
from google.genai.types import Content, Part

from marvin.agents.base import MODEL_GEMINI_2_0_PRO, create_runner


def topological_sort(
    tasks: List[Dict], dependencies: Dict[str, List[str]]
) -> List[Dict]:
    """
    Perform a topological sort on tasks based on dependencies.

    Args:
        tasks: List of task dictionaries
        dependencies: Dictionary mapping task IDs to lists of dependency task IDs

    Returns:
        Sorted list of tasks
    """
    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes for all tasks
    for task in tasks:
        task_id = task["id"]
        G.add_node(task_id)

    # Add edges for dependencies
    for task_id, deps in dependencies.items():
        for dep in deps:
            G.add_edge(dep, task_id)  # Edge from dependency to task

    try:
        # Perform topological sort
        sorted_ids = list(nx.topological_sort(G))

        # Map back to the original task objects
        id_to_task = {task["id"]: task for task in tasks}
        sorted_tasks = [
            id_to_task[task_id] for task_id in sorted_ids if task_id in id_to_task
        ]

        return sorted_tasks
    except nx.NetworkXUnfeasible:
        # Cycle detected, cannot perform topological sort
        # In a real implementation, we would handle this better
        return tasks


def plan_sequence(tasks: List[Dict], tool_context: Any = None) -> Dict:
    """
    Plan an optimal implementation sequence for tasks.

    Args:
        tasks: List of task dictionaries with ID and dependencies
        tool_context: Tool context provided by ADK (not used here)

    Returns:
        Dict containing the planned sequence
    """
    try:
        # Extract dependencies from tasks
        dependencies = {}
        for i, task in enumerate(tasks):
            task_id = task.get("id", f"task_{i}")
            task["id"] = task_id  # Ensure ID exists

            # Extract dependencies for this task
            task_deps = task.get("dependencies", [])
            if task_deps:
                dependencies[task_id] = task_deps

        # Perform topological sort
        sorted_tasks = topological_sort(tasks, dependencies)

        # Add sequence numbers
        for i, task in enumerate(sorted_tasks):
            task["sequence_number"] = i + 1

        return {"status": "success", "sequence": sorted_tasks}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# Create the sequence planning agent
sequence_planner_agent = Agent(
    name="sequence_planner_agent",
    model=MODEL_GEMINI_2_0_PRO,
    description="Plans optimal implementation sequences based on task dependencies",
    instruction="""You are a sequence planning specialist. Your job is to arrange tasks in an optimal
order based on their dependencies. When presented with a list of tasks and their dependencies,
use the plan_sequence tool to create an optimal implementation sequence. Present the sequence
clearly to the user, explaining the reasoning behind the ordering.""",
    tools=[plan_sequence],
)

# Create a runner for the agent
sequence_planner_runner = create_runner(sequence_planner_agent)


async def plan_sequence_async(tasks: List[Dict]) -> Dict:
    """
    Plan an implementation sequence asynchronously using the sequence planner agent.

    Args:
        tasks: List of task dictionaries

    Returns:
        Dict containing the planned sequence
    """
    # Create a message for the agent
    task_descriptions = "\n".join(
        [f"Task {i + 1}: {task}" for i, task in enumerate(tasks)]
    )

    message_text = f"""Please plan an optimal implementation sequence for these tasks:

{task_descriptions}

Consider the dependencies and arrange them in the most efficient order."""

    message = Content(role="user", parts=[Part(text=message_text)])

    # Run the agent and collect the final response
    final_response = None
    async for event in sequence_planner_runner.run_async(
        user_id="marvin_user",
        session_id="sequence_planner_session",
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_response = event.content.parts[0].text
            break

    # Return the planned sequence
    return {
        "status": "success",
        "planned_sequence": final_response or "No sequence planned",
    }
