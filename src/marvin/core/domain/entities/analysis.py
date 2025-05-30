"""Analysis-related domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from .codebase import CodebaseAnalysis
from .prd import PRDDocument
from .task import TaskSequence


@dataclass
class AnalysisContext:
    """Context for the analysis process."""
    
    id: UUID = field(default_factory=uuid4)
    prd_document: Optional[PRDDocument] = None
    codebase_analysis: Optional[CodebaseAnalysis] = None
    user_preferences: dict[str, Any] = field(default_factory=dict)
    constraints: dict[str, Any] = field(default_factory=dict)
    
    @property
    def has_codebase(self) -> bool:
        """Check if codebase analysis is available."""
        return self.codebase_analysis is not None
    
    @property
    def is_greenfield(self) -> bool:
        """Check if this is a greenfield project."""
        return not self.has_codebase


@dataclass
class AnalysisResult:
    """Result of the complete analysis process."""
    
    id: UUID = field(default_factory=uuid4)
    context: AnalysisContext = field(default_factory=AnalysisContext)
    task_sequence: TaskSequence = field(default_factory=TaskSequence)
    generated_templates: dict[UUID, str] = field(default_factory=dict)
    insights: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    processing_time_seconds: float = 0.0
    
    def add_template(self, task_id: UUID, template: str) -> None:
        """Add a generated template for a task."""
        self.generated_templates[task_id] = template
    
    def add_insight(self, insight: str) -> None:
        """Add an insight from the analysis."""
        self.insights.append(insight)
    
    def add_warning(self, warning: str) -> None:
        """Add a warning from the analysis."""
        self.warnings.append(warning)
