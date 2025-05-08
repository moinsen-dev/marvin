"""Agent zur Planung von Aufgabensequenzen."""

import itertools
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Codebase, Feature, PRD, Task, TaskStatus, Workflow


class DependencyGraph:
    """Graph zur Darstellung von Abhängigkeiten zwischen Aufgaben."""
    
    def __init__(self):
        """Initialisiert einen neuen Abhängigkeitsgraphen."""
        self.nodes: Dict[str, Set[str]] = {}  # Feature-ID -> abhängige Features
    
    def add_node(self, feature_id: str) -> None:
        """Fügt einen Knoten zum Graphen hinzu.
        
        Args:
            feature_id: ID des Features
        """
        if feature_id not in self.nodes:
            self.nodes[feature_id] = set()
    
    def add_edge(self, from_id: str, to_id: str) -> None:
        """Fügt eine Kante zum Graphen hinzu (from_id hängt von to_id ab).
        
        Args:
            from_id: ID des abhängigen Features
            to_id: ID des Features, von dem abhängig ist
        """
        self.add_node(from_id)
        self.add_node(to_id)
        self.nodes[from_id].add(to_id)
    
    def has_cycle(self) -> bool:
        """Prüft, ob der Graph Zyklen enthält.
        
        Returns:
            True, wenn Zyklen vorhanden sind, sonst False
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
    
    def topological_sort(self) -> List[str]:
        """Führt eine topologische Sortierung des Graphen durch.
        
        Returns:
            Liste der Feature-IDs in topologischer Reihenfolge
            
        Raises:
            ValueError: Wenn der Graph Zyklen enthält
        """
        if self.has_cycle():
            raise ValueError("Graph enthält Zyklen und kann nicht topologisch sortiert werden")
        
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
    """Agent zur Planung von Aufgabensequenzen basierend auf Feature-Abhängigkeiten."""
    
    def __init__(self, name: str = "sequence_planner", config: Optional[Dict[str, Any]] = None):
        """Initialisiert den SequencePlannerAgent.
        
        Args:
            name: Name des Agenten
            config: Konfiguration des Agenten
        """
        super().__init__(name, config)
    
    async def execute(
        self, prd: PRD, codebase: Optional[Codebase] = None, **kwargs: Any
    ) -> Workflow:
        """Plant eine Sequenz von Aufgaben basierend auf Feature-Abhängigkeiten.
        
        Args:
            prd: Das PRD mit den Features
            codebase: (Optional) Die analysierte Codebase
            **kwargs: Weitere Parameter
            
        Returns:
            Workflow mit geplanten Aufgaben
        """
        # Abhängigkeitsgraphen erstellen
        dependency_graph = await self._build_dependency_graph(prd.features)
        
        # Topologische Sortierung durchführen
        try:
            feature_sequence = dependency_graph.topological_sort()
        except ValueError:
            # Bei Zyklen eine andere Strategie anwenden
            feature_sequence = await self._resolve_cyclic_dependencies(prd.features, dependency_graph)
        
        # Workflow erstellen
        workflow = Workflow(
            id=f"workflow_{prd.id}",
            name=f"Workflow für {prd.title}",
            description=f"Automatisch generierter Workflow für {prd.title}",
            prd_id=prd.id,
            codebase_id=codebase.id if codebase else None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        # Aufgaben für jedes Feature erstellen
        sequence_number = 1
        for feature_id in feature_sequence:
            feature = next((f for f in prd.features if f.id == feature_id), None)
            if not feature:
                continue
            
            # Abhängigkeiten für die Task ermitteln
            depends_on = []
            for dep_id in feature.dependencies:
                dep_feature = next((f for f in prd.features if f.id == dep_id), None)
                if dep_feature:
                    depends_on.append(f"task_{dep_feature.id}")
            
            # Task erstellen
            task = Task(
                task_id=f"task_{feature.id}",
                sequence_number=sequence_number,
                name=f"Implementiere {feature.name}",
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
    
    async def _build_dependency_graph(self, features: List[Feature]) -> DependencyGraph:
        """Erstellt einen Abhängigkeitsgraphen aus Features.
        
        Args:
            features: Liste der Features
            
        Returns:
            Abhängigkeitsgraph
        """
        graph = DependencyGraph()
        
        # Knoten für alle Features hinzufügen
        for feature in features:
            graph.add_node(feature.id)
        
        # Kanten für Abhängigkeiten hinzufügen
        for feature in features:
            for dep_id in feature.dependencies:
                graph.add_edge(feature.id, dep_id)
        
        return graph
    
    async def _resolve_cyclic_dependencies(
        self, features: List[Feature], graph: DependencyGraph
    ) -> List[str]:
        """Löst zyklische Abhängigkeiten auf, indem die am wenigsten störenden Kanten entfernt werden.
        
        Args:
            features: Liste der Features
            graph: Abhängigkeitsgraph mit Zyklen
            
        Returns:
            Sequenz von Feature-IDs
        """
        # Tiefe Kopie des Graphen erstellen
        import copy
        working_graph = copy.deepcopy(graph)
        
        # Prioritäten der Features berücksichtigen
        feature_priorities = {f.id: f.priority for f in features}
        
        # Kanten entfernen, bis keine Zyklen mehr vorhanden sind
        removed_edges = []
        while working_graph.has_cycle():
            # Kante mit niedrigster Priorität finden
            min_priority = float("inf")
            edge_to_remove = None
            
            for from_id, to_ids in working_graph.nodes.items():
                for to_id in to_ids:
                    # Priorität der Kante berechnen
                    edge_priority = feature_priorities.get(from_id, 0) + feature_priorities.get(to_id, 0)
                    if edge_priority < min_priority:
                        min_priority = edge_priority
                        edge_to_remove = (from_id, to_id)
            
            if edge_to_remove:
                from_id, to_id = edge_to_remove
                working_graph.nodes[from_id].remove(to_id)
                removed_edges.append(edge_to_remove)
            else:
                # Keine Kanten mehr zum Entfernen
                break
        
        # Topologische Sortierung des bereinigten Graphen
        feature_sequence = working_graph.topological_sort()
        
        return feature_sequence
