"""Abstract AI service interface."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class AIService(ABC):
    """Abstract interface for AI services."""
    
    @abstractmethod
    async def extract_features(self, prd_content: str) -> list[dict[str, Any]]:
        """Extract features from PRD content."""
        pass
    
    @abstractmethod
    async def analyze_codebase(self, file_contents: dict[str, str]) -> dict[str, Any]:
        """Analyze codebase structure."""
        pass
    
    @abstractmethod
    async def generate_task_sequence(self, features: list[dict], codebase_info: Optional[dict] = None) -> list[dict]:
        """Generate task sequence from features."""
        pass
    
    @abstractmethod
    async def generate_xml_template(self, task: dict, context: dict) -> str:
        """Generate XML template for a task."""
        pass
