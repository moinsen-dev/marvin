"""Agent for planning task sequences."""

from datetime import datetime
from typing import Any

from marvin.core.agents.base import Agent
from marvin.core.domain.models import PRD, Codebase, Feature, Task, TaskStatus, Workflow


class DependencyGraph:
    """Graph for representing dependencies between tasks."""

    def __init__(self):
        """Initializes a new dependency graph."""
        self.nodes: dict[str, set[str]] = {}  # Feature ID -> dependent features

    def add_node(self, feature_id: str) -> None:
        """Adds a node to the graph.

        Args:
            feature_id: ID of the feature
        """
        if feature_id not in self.nodes:
            self.nodes[feature_id] = set()

    def add_edge(self, from_id: str, to_id: str) -> None:
        """Adds an edge to the graph (from_id depends on to_id).

        Args:
            from_id: ID of the dependent feature
            to_id: ID of the feature that is depended on
        """
        self.add_node(from_id)
        self.add_node(to_id)
        self.nodes[from_id].add(to_id)

    def has_cycle(self) -> bool:
        """Checks if the graph contains cycles.

        Returns:
            True if cycles are present, False otherwise
        """
        visited = set()
        rec_stack = set()

        def is_cyclic(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.nodes[node]:
                if neighbor not in visited:
                    if is_cyclic(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node in self.nodes:
            if node not in visited:
                if is_cyclic(node):
                    return True

        return False

    def topological_sort(self) -> list[str]:
        """Performs a topological sort of the graph.

        Returns:
            List of feature IDs in topological order

        Raises:
            ValueError: If the graph contains cycles
        """
        if self.has_cycle():
            raise ValueError("Graph contains cycles and cannot be topologically sorted")

        visited = set()
        result = []

        def dfs(node: str) -> None:
            visited.add(node)

            for neighbor in self.nodes[node]:
                if neighbor not in visited:
                    dfs(neighbor)

            result.append(node)

        for node in self.nodes:
            if node not in visited:
                dfs(node)

        return list(reversed(result))


class SequencePlannerAgent(Agent):
    """Agent for planning task sequences based on feature dependencies."""

    def __init__(
        self, name: str = "sequence_planner", config: dict[str, Any] | None = None
    ):
        """Initializes the SequencePlannerAgent.

        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        super().__init__(name, config)

    async def execute(
        self, prd: PRD, codebase: Codebase | None = None, **kwargs: Any
    ) -> Workflow:
        """Plans a sequence of tasks based on feature dependencies.

        Args:
            prd: The PRD with the features
            codebase: (Optional) The analyzed codebase
            **kwargs: Additional parameters

        Returns:
            Workflow with planned tasks
        """
        # Create dependency graph
        dependency_graph = await self._build_dependency_graph(prd.features)

        # Perform topological sort
        try:
            feature_sequence = dependency_graph.topological_sort()
        except ValueError:
            # Apply a different strategy for cycles
            feature_sequence = await self._resolve_cyclic_dependencies(
                prd.features, dependency_graph
            )

        # Create workflow
        workflow = Workflow(
            id=f"workflow_{prd.id}",
            name=f"Workflow for {prd.title}",
            description=f"Automatically generated workflow for {prd.title}",
            prd_id=prd.id,
            codebase_id=codebase.id if codebase else None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Create tasks for each feature
        sequence_number = 1
        for feature_id in feature_sequence:
            feature = next((f for f in prd.features if f.id == feature_id), None)
            if not feature:
                continue

            # Determine dependencies for the task
            depends_on = []
            for dep_id in feature.dependencies:
                dep_feature = next((f for f in prd.features if f.id == dep_id), None)
                if dep_feature:
                    depends_on.append(f"task_{dep_feature.id}")

            # Create task
            task = Task(
                task_id=f"task_{feature.id}",
                sequence_number=sequence_number,
                name=f"Implement {feature.name}",
                description=feature.description,
                feature_id=feature.id,
                depends_on=depends_on,
                status=TaskStatus.PLANNED,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

            workflow.add_task(task)
            sequence_number += 1

        return workflow

    async def _build_dependency_graph(self, features: list[Feature]) -> DependencyGraph:
        """Creates a dependency graph from features.

        Args:
            features: List of features

        Returns:
            Dependency graph
        """
        graph = DependencyGraph()

        # Add nodes for all features
        for feature in features:
            graph.add_node(feature.id)

        # Add edges for dependencies
        for feature in features:
            for dep_id in feature.dependencies:
                graph.add_edge(feature.id, dep_id)

        return graph

    async def _resolve_cyclic_dependencies(
        self, features: list[Feature], graph: DependencyGraph
    ) -> list[str]:
        """Resolves cyclic dependencies by removing the least disruptive edges.

        Args:
            features: List of features
            graph: Dependency graph with cycles

        Returns:
            Sequence of feature IDs
        """
        # Create a deep copy of the graph
        import copy

        working_graph = copy.deepcopy(graph)

        # Consider feature priorities
        feature_priorities = {f.id: f.priority for f in features}

        # Remove edges until no cycles remain
        removed_edges = []
        while working_graph.has_cycle():
            # Find edge with lowest priority
            min_priority = float("inf")
            edge_to_remove = None

            for from_id, to_ids in working_graph.nodes.items():
                for to_id in to_ids:
                    # Calculate edge priority
                    edge_priority = feature_priorities.get(
                        from_id, 0
                    ) + feature_priorities.get(to_id, 0)
                    if edge_priority < min_priority:
                        min_priority = edge_priority
                        edge_to_remove = (from_id, to_id)

            if edge_to_remove:
                from_id, to_id = edge_to_remove
                working_graph.nodes[from_id].remove(to_id)
                removed_edges.append(edge_to_remove)
            else:
                # No more edges to remove
                break

        # Topological sort of the cleaned graph
        feature_sequence = working_graph.topological_sort()

        return feature_sequence
