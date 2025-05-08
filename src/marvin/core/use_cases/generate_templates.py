"""Use Case: Generation of AI coding task templates from a PRD."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from marvin.core.agents.codebase_analysis import CodebaseAnalysisAgent
from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.agents.sequence_planner import SequencePlannerAgent
from marvin.core.agents.template_generation import TemplateGenerationAgent
from marvin.core.domain.models import Codebase, Feature, PRD, Task, Workflow


class GenerateTemplatesUseCase:
    """Use Case: Generation of AI coding task templates from a PRD."""
    
    def __init__(
        self,
        document_analysis_agent: DocumentAnalysisAgent,
        codebase_analysis_agent: Optional[CodebaseAnalysisAgent] = None,
        sequence_planner_agent: Optional[SequencePlannerAgent] = None,
        template_generation_agent: Optional[TemplateGenerationAgent] = None,
    ):
        """Initializes the GenerateTemplatesUseCase.
        
        Args:
            document_analysis_agent: Agent for analyzing PRDs
            codebase_analysis_agent: (Optional) Agent for analyzing codebases
            sequence_planner_agent: (Optional) Agent for planning task sequences
            template_generation_agent: (Optional) Agent for generating templates
        """
        self.document_analysis_agent = document_analysis_agent
        self.codebase_analysis_agent = codebase_analysis_agent or CodebaseAnalysisAgent()
        self.sequence_planner_agent = sequence_planner_agent or SequencePlannerAgent()
        self.template_generation_agent = template_generation_agent or TemplateGenerationAgent()
    
    async def execute(
        self,
        prd_path: str,
        output_dir: str,
        codebase_path: Optional[str] = None,
        **kwargs: Any,
    ) -> Tuple[str, List[str]]:
        """Executes the use case.
        
        Args:
            prd_path: Path to the PRD document
            output_dir: Output directory for the templates
            codebase_path: (Optional) Path to the codebase
            **kwargs: Additional parameters
            
        Returns:
            Tuple of workflow ID and list of paths to the generated templates
            
        Raises:
            FileNotFoundError: If the PRD or codebase was not found
            ValueError: If the PRD does not have a supported format
        """
        # 1. Analyze PRD
        prd, features = await self.document_analysis_agent.execute(
            prd_path, **kwargs
        )
        
        # 2. Analyze codebase (if present)
        codebase = None
        if codebase_path:
            codebase = await self.codebase_analysis_agent.execute(
                codebase_path, name=prd.title, **kwargs
            )
        
        # 3. Plan task sequence
        workflow = await self.sequence_planner_agent.execute(
            prd, codebase, **kwargs
        )
        
        # 4. Generate templates for each task
        template_paths = []
        for task in workflow.tasks:
            feature = next((f for f in features if f.id == task.feature_id), None)
            if not feature:
                continue
            
            template_path = await self.template_generation_agent.execute(
                task, feature, prd, output_dir, codebase, **kwargs
            )
            template_paths.append(template_path)
            
            # Update task with template path
            task.template_path = template_path
        
        return workflow.id, template_paths
