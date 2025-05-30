"""Task sequencer domain service."""

from typing import Any
from uuid import UUID

from ..entities.analysis import AnalysisContext
from ..entities.task import (
    TaskComplexity,
    TaskContext,
    TaskDefinition,
    TaskSequence,
    TaskType,
)


class TaskSequencer:
    """Service for creating and optimizing task sequences."""
    
    def create_from_ai_result(self, ai_tasks: list[dict[str, Any]], context: AnalysisContext) -> TaskSequence:
        """Create a task sequence from AI-generated tasks."""
        sequence = TaskSequence(
            name="AI Coding Tasks",
            description=f"Tasks for implementing {len(context.prd_document.features)} features",
        )
        
        # Create task definitions
        task_map = {}
        for i, ai_task in enumerate(ai_tasks):
            task = self._create_task_from_ai(ai_task, i + 1, context)
            task_map[ai_task.get("task_id", str(task.id))] = task
            sequence.add_task(task)
        
        # Set up dependencies
        for ai_task, task in zip(ai_tasks, sequence.tasks):
            dep_ids = ai_task.get("dependencies", [])
            for dep_id in dep_ids:
                if dep_task := task_map.get(dep_id):
                    task.prerequisites.append(dep_task.id)
        
        return sequence
    
    def _create_task_from_ai(self, ai_task: dict[str, Any], sequence_num: int, context: AnalysisContext) -> TaskDefinition:
        """Create a TaskDefinition from AI task data."""
        # Map task type
        task_type_map = {
            "implementation": TaskType.IMPLEMENTATION,
            "refactoring": TaskType.REFACTORING,
            "testing": TaskType.TESTING,
            "documentation": TaskType.DOCUMENTATION,
            "debugging": TaskType.DEBUGGING,
            "configuration": TaskType.CONFIGURATION,
        }
        task_type = task_type_map.get(ai_task.get("type", ""), TaskType.IMPLEMENTATION)
        
        # Create task context
        task_context = TaskContext(
            feature_id=UUID(ai_task.get("feature_id", "00000000-0000-0000-0000-000000000000")),
            files_to_modify=ai_task.get("files_to_modify", []),
            files_to_create=ai_task.get("files_to_create", []),
        )
        
        # Create task definition
        return TaskDefinition(
            name=ai_task.get("name", f"Task {sequence_num}"),
            description=ai_task.get("description", ""),
            type=task_type,
            complexity=self._estimate_complexity(ai_task),
            context=task_context,
            estimated_time=ai_task.get("estimated_time"),
            acceptance_criteria=ai_task.get("acceptance_criteria", []),
        )
    
    def _estimate_complexity(self, ai_task: dict[str, Any]) -> TaskComplexity:
        """Estimate task complexity based on various factors."""
        # Simple heuristic based on file counts and estimated time
        files_count = len(ai_task.get("files_to_modify", [])) + len(ai_task.get("files_to_create", []))
        time_str = ai_task.get("estimated_time", "").lower()
        
        if "day" in time_str or "week" in time_str:
            return TaskComplexity.COMPLEX
        elif files_count > 5:
            return TaskComplexity.COMPLEX
        elif files_count > 2:
            return TaskComplexity.MODERATE
        elif "hour" in time_str:
            return TaskComplexity.SIMPLE
        else:
            return TaskComplexity.TRIVIAL
