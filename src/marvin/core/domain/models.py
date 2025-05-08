"""Domain models for Marvin."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

from pydantic import BaseModel, Field


class FeatureStatus(str, Enum):
    """Status of a feature."""
    
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    REJECTED = "rejected"


class Feature(BaseModel):
    """A feature from a PRD."""
    
    id: str
    name: str
    description: str
    requirements: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    status: FeatureStatus = FeatureStatus.PROPOSED
    priority: int = 0
    estimated_effort: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class PRD(BaseModel):
    """A Product Requirements Document."""
    
    id: str
    title: str
    description: str
    author: str
    created_at: datetime
    updated_at: datetime
    version: str
    features: List[Feature] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    
    def add_feature(self, feature: Feature) -> None:
        """Adds a feature to the PRD."""
        self.features.append(feature)
        self.updated_at = datetime.now()


class Component(BaseModel):
    """A component of a codebase."""
    
    name: str
    path: str
    type: str  # file, directory, module, class, etc.
    description: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Technology(BaseModel):
    """A technology used in a codebase."""
    
    name: str
    version: Optional[str] = None
    category: str  # language, framework, library, database, etc.
    description: Optional[str] = None


class Codebase(BaseModel):
    """An analyzed codebase."""
    
    id: str
    name: str
    root_path: str
    components: List[Component] = Field(default_factory=list)
    technologies: List[Technology] = Field(default_factory=list)
    scanned_at: datetime = Field(default_factory=datetime.now)
    architecture_patterns: List[str] = Field(default_factory=list)
    
    def add_component(self, component: Component) -> None:
        """Adds a component to the codebase."""
        self.components.append(component)


class TaskStatus(str, Enum):
    """Status of a task."""
    
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class Task(BaseModel):
    """An AI coding task."""
    
    task_id: str
    sequence_number: int
    name: str
    description: str
    feature_id: str
    depends_on: List[str] = Field(default_factory=list)
    template_path: Optional[str] = None
    status: TaskStatus = TaskStatus.PLANNED
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @property
    def is_blocked(self) -> bool:
        """Checks if the task is blocked."""
        return self.status == TaskStatus.BLOCKED


class Workflow(BaseModel):
    """A workflow with a sequence of tasks."""
    
    id: str
    name: str
    description: str
    prd_id: str
    codebase_id: Optional[str] = None
    tasks: List[Task] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_task(self, task: Task) -> None:
        """Adds a task to the workflow."""
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x.sequence_number)
        self.updated_at = datetime.now()
