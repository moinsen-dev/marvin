"""PRD-related domain entities."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4


class RequirementType(str, Enum):
    """Types of requirements in a PRD."""
    
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    TECHNICAL = "technical"
    BUSINESS = "business"
    USER_EXPERIENCE = "user_experience"


class PriorityLevel(str, Enum):
    """Priority levels for features."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NICE_TO_HAVE = "nice_to_have"


@dataclass
class UserStory:
    """Represents a user story in the PRD."""
    
    id: UUID = field(default_factory=uuid4)
    persona: str = ""
    goal: str = ""
    benefit: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    
    @property
    def formatted_story(self) -> str:
        """Returns the user story in standard format."""
        return f"As a {self.persona}, I want to {self.goal} so that {self.benefit}"


@dataclass
class Requirement:
    """Represents a requirement in the PRD."""
    
    id: UUID = field(default_factory=uuid4)
    description: str = ""
    type: RequirementType = RequirementType.FUNCTIONAL
    priority: PriorityLevel = PriorityLevel.MEDIUM
    rationale: Optional[str] = None
    constraints: list[str] = field(default_factory=list)
    dependencies: list[UUID] = field(default_factory=list)


@dataclass
class FeatureSpecification:
    """Represents a feature specification in the PRD."""
    
    id: UUID = field(default_factory=uuid4)
    name: str = ""
    description: str = ""
    requirements: list[Requirement] = field(default_factory=list)
    user_stories: list[UserStory] = field(default_factory=list)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    estimated_effort: Optional[str] = None
    dependencies: list[UUID] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    
    def add_requirement(self, requirement: Requirement) -> None:
        """Add a requirement to the feature."""
        self.requirements.append(requirement)
    
    def add_user_story(self, story: UserStory) -> None:
        """Add a user story to the feature."""
        self.user_stories.append(story)


@dataclass
class PRDDocument:
    """Represents a Product Requirements Document."""
    
    id: UUID = field(default_factory=uuid4)
    title: str = ""
    description: str = ""
    author: str = ""
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    features: list[FeatureSpecification] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    
    def add_feature(self, feature: FeatureSpecification) -> None:
        """Add a feature to the PRD."""
        self.features.append(feature)
        self.updated_at = datetime.now()
    
    def get_features_by_priority(self, priority: PriorityLevel) -> list[FeatureSpecification]:
        """Get all features with a specific priority."""
        return [f for f in self.features if f.priority == priority]
    
    def get_dependency_graph(self) -> dict[UUID, list[UUID]]:
        """Build a dependency graph of all features."""
        graph = {}
        for feature in self.features:
            graph[feature.id] = feature.dependencies
        return graph
