"""Codebase analysis domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Set
from uuid import UUID, uuid4


class ComponentType(str, Enum):
    """Types of components in a codebase."""
    
    MODULE = "module"
    PACKAGE = "package"
    CLASS = "class"
    FUNCTION = "function"
    FILE = "file"
    DIRECTORY = "directory"
    SERVICE = "service"
    API_ENDPOINT = "api_endpoint"
    DATABASE_MODEL = "database_model"
    CONFIGURATION = "configuration"


class TechnologyCategory(str, Enum):
    """Categories of technologies."""
    
    LANGUAGE = "language"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    DATABASE = "database"
    TOOL = "tool"
    INFRASTRUCTURE = "infrastructure"


@dataclass
class Technology:
    """Represents a technology used in the codebase."""
    
    name: str
    version: Optional[str] = None
    category: TechnologyCategory = TechnologyCategory.LIBRARY
    purpose: Optional[str] = None
    dependencies: list[str] = field(default_factory=list)


@dataclass
class Component:
    """Represents a component in the codebase."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    path: Path = Path()
    type: ComponentType = ComponentType.FILE
    description: Optional[str] = None
    imports: Set[str] = field(default_factory=set)
    exports: Set[str] = field(default_factory=set)
    dependencies: list[UUID] = field(default_factory=list)
    
    @property
    def is_entry_point(self) -> bool:
        """Check if this component is an entry point."""
        return self.type in [ComponentType.SERVICE, ComponentType.API_ENDPOINT]


@dataclass
class ComponentGraph:
    """Represents the dependency graph of components."""
    
    components: dict[UUID, Component] = field(default_factory=dict)
    edges: dict[UUID, Set[UUID]] = field(default_factory=dict)
    
    def add_component(self, component: Component) -> None:
        """Add a component to the graph."""
        self.components[component.id] = component
        if component.id not in self.edges:
            self.edges[component.id] = set()
        
        # Add edges for dependencies
        for dep_id in component.dependencies:
            self.edges[component.id].add(dep_id)
    
    def get_dependencies(self, component_id: UUID) -> Set[Component]:
        """Get all dependencies of a component."""
        dep_ids = self.edges.get(component_id, set())
        return {self.components[dep_id] for dep_id in dep_ids if dep_id in self.components}
    
    def get_dependents(self, component_id: UUID) -> Set[Component]:
        """Get all components that depend on this component."""
        dependents = set()
        for comp_id, deps in self.edges.items():
            if component_id in deps:
                dependents.add(self.components[comp_id])
        return dependents


@dataclass
class TechnologyStack:
    """Represents the technology stack of a codebase."""
    
    primary_language: Optional[Technology] = None
    frameworks: list[Technology] = field(default_factory=list)
    libraries: list[Technology] = field(default_factory=list)
    databases: list[Technology] = field(default_factory=list)
    tools: list[Technology] = field(default_factory=list)
    
    def add_technology(self, tech: Technology) -> None:
        """Add a technology to the appropriate category."""
        if tech.category == TechnologyCategory.LANGUAGE and not self.primary_language:
            self.primary_language = tech
        elif tech.category == TechnologyCategory.FRAMEWORK:
            self.frameworks.append(tech)
        elif tech.category == TechnologyCategory.LIBRARY:
            self.libraries.append(tech)
        elif tech.category == TechnologyCategory.DATABASE:
            self.databases.append(tech)
        elif tech.category == TechnologyCategory.TOOL:
            self.tools.append(tech)


@dataclass
class CodebaseAnalysis:
    """Represents a complete codebase analysis."""
    
    id: UUID = field(default_factory=uuid4)
    root_path: Path = Path()
    analyzed_at: datetime = field(default_factory=datetime.now)
    component_graph: ComponentGraph = field(default_factory=ComponentGraph)
    technology_stack: TechnologyStack = field(default_factory=TechnologyStack)
    architecture_patterns: list[str] = field(default_factory=list)
    entry_points: list[Component] = field(default_factory=list)
    
    def add_component(self, component: Component) -> None:
        """Add a component to the analysis."""
        self.component_graph.add_component(component)
        if component.is_entry_point:
            self.entry_points.append(component)
