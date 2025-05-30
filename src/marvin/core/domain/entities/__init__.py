"""Domain entities for Marvin."""

from .analysis import AnalysisContext, AnalysisResult
from .codebase import CodebaseAnalysis, ComponentGraph, TechnologyStack
from .prd import PRDDocument, FeatureSpecification, RequirementType
from .task import TaskDefinition, TaskSequence, TaskTemplate

__all__ = [
    "AnalysisContext",
    "AnalysisResult",
    "CodebaseAnalysis",
    "ComponentGraph",
    "TechnologyStack",
    "PRDDocument",
    "FeatureSpecification",
    "RequirementType",
    "TaskDefinition",
    "TaskSequence",
    "TaskTemplate",
]
