"""Domänenmodelle für Marvin."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

from pydantic import BaseModel, Field


class FeatureStatus(str, Enum):
    """Status eines Features."""
    
    PROPOSED = "proposed"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"
    REJECTED = "rejected"


class Feature(BaseModel):
    """Ein Feature aus einem PRD."""
    
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
    """Ein Produktanforderungsdokument."""
    
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
        """Fügt ein Feature zum PRD hinzu."""
        self.features.append(feature)
        self.updated_at = datetime.now()


class Component(BaseModel):
    """Eine Komponente einer Codebase."""
    
    name: str
    path: str
    type: str  # file, directory, module, class, etc.
    description: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)


class Technology(BaseModel):
    """Eine Technologie, die in einer Codebase verwendet wird."""
    
    name: str
    version: Optional[str] = None
    category: str  # language, framework, library, database, etc.
    description: Optional[str] = None


class Codebase(BaseModel):
    """Eine analysierte Codebase."""
    
    id: str
    name: str
    root_path: str
    components: List[Component] = Field(default_factory=list)
    technologies: List[Technology] = Field(default_factory=list)
    scanned_at: datetime = Field(default_factory=datetime.now)
    architecture_patterns: List[str] = Field(default_factory=list)
    
    def add_component(self, component: Component) -> None:
        """Fügt eine Komponente zur Codebase hinzu."""
        self.components.append(component)


class TaskStatus(str, Enum):
    """Status einer Task."""
    
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"


class Task(BaseModel):
    """Eine AI-Coding-Task."""
    
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
        """Prüft, ob die Task blockiert ist."""
        return self.status == TaskStatus.BLOCKED


class Workflow(BaseModel):
    """Ein Workflow mit einer Sequenz von Tasks."""
    
    id: str
    name: str
    description: str
    prd_id: str
    codebase_id: Optional[str] = None
    tasks: List[Task] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    def add_task(self, task: Task) -> None:
        """Fügt eine Task zum Workflow hinzu."""
        self.tasks.append(task)
        self.tasks.sort(key=lambda x: x.sequence_number)
        self.updated_at = datetime.now()
