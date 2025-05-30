"""Task-related domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional, Set
from uuid import UUID, uuid4


class TaskType(str, Enum):
    """Types of AI coding tasks."""
    
    IMPLEMENTATION = "implementation"
    REFACTORING = "refactoring"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEBUGGING = "debugging"
    REVIEW = "review"
    RESEARCH = "research"
    CONFIGURATION = "configuration"


class TaskComplexity(str, Enum):
    """Complexity levels for tasks."""
    
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"


@dataclass
class TaskContext:
    """Context information for a task."""
    
    feature_id: UUID
    component_ids: list[UUID] = field(default_factory=list)
    technologies: list[str] = field(default_factory=list)
    files_to_modify: list[str] = field(default_factory=list)
    files_to_create: list[str] = field(default_factory=list)
    reference_examples: list[str] = field(default_factory=list)


@dataclass
class TaskDefinition:
    """Represents an AI coding task."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    type: TaskType = TaskType.IMPLEMENTATION
    complexity: TaskComplexity = TaskComplexity.MODERATE
    context: TaskContext = field(default_factory=TaskContext)
    prerequisites: list[UUID] = field(default_factory=list)
    estimated_time: Optional[str] = None
    acceptance_criteria: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class TaskTemplate:
    """Represents an XML template for an AI coding task."""
    
    task_id: UUID
    template_content: str = ""
    format_version: str = "1.0"
    ai_assistant_hints: list[str] = field(default_factory=list)
    
    def to_xml(self) -> str:
        """Convert the template to XML format."""
        # This will be implemented with proper XML generation
        return self.template_content


@dataclass
class TaskSequence:
    """Represents a sequence of tasks with dependencies."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    tasks: list[TaskDefinition] = field(default_factory=list)
    execution_order: list[UUID] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_task(self, task: TaskDefinition) -> None:
        """Add a task to the sequence."""
        self.tasks.append(task)
        self._update_execution_order()
    
    def _update_execution_order(self) -> None:
        """Update the execution order based on dependencies."""
        # Topological sort implementation
        visited = set()
        order = []
        
        def visit(task_id: UUID) -> None:
            if task_id in visited:
                return
            visited.add(task_id)
            
            task = next((t for t in self.tasks if t.id == task_id), None)
            if task:
                for prereq in task.prerequisites:
                    visit(prereq)
                order.append(task_id)
        
        for task in self.tasks:
            visit(task.id)
        
        self.execution_order = order
    
    def get_next_tasks(self, completed_task_ids: Set[UUID]) -> list[TaskDefinition]:
        """Get the next tasks that can be executed."""
        available_tasks = []
        
        for task in self.tasks:
            if task.id in completed_task_ids:
                continue
            
            # Check if all prerequisites are completed
            if all(prereq in completed_task_ids for prereq in task.prerequisites):
                available_tasks.append(task)
        
        return available_tasks
