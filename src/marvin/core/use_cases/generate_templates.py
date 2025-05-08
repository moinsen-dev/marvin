"""Use Case: Generierung von AI-Coding-Task-Templates aus einem PRD."""

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
    """Use Case: Generierung von AI-Coding-Task-Templates aus einem PRD."""
    
    def __init__(
        self,
        document_analysis_agent: DocumentAnalysisAgent,
        codebase_analysis_agent: Optional[CodebaseAnalysisAgent] = None,
        sequence_planner_agent: Optional[SequencePlannerAgent] = None,
        template_generation_agent: Optional[TemplateGenerationAgent] = None,
    ):
        """Initialisiert den GenerateTemplatesUseCase.
        
        Args:
            document_analysis_agent: Agent zur Analyse von PRDs
            codebase_analysis_agent: (Optional) Agent zur Analyse von Codebases
            sequence_planner_agent: (Optional) Agent zur Planung von Aufgabensequenzen
            template_generation_agent: (Optional) Agent zur Generierung von Templates
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
        """Führt den Use Case aus.
        
        Args:
            prd_path: Pfad zum PRD-Dokument
            output_dir: Ausgabeverzeichnis für die Templates
            codebase_path: (Optional) Pfad zur Codebase
            **kwargs: Weitere Parameter
            
        Returns:
            Tupel aus Workflow-ID und Liste der Pfade zu den generierten Templates
            
        Raises:
            FileNotFoundError: Wenn das PRD oder die Codebase nicht gefunden wurde
            ValueError: Wenn das PRD kein unterstütztes Format hat
        """
        # 1. PRD analysieren
        prd, features = await self.document_analysis_agent.execute(
            prd_path, **kwargs
        )
        
        # 2. Codebase analysieren (falls vorhanden)
        codebase = None
        if codebase_path:
            codebase = await self.codebase_analysis_agent.execute(
                codebase_path, name=prd.title, **kwargs
            )
        
        # 3. Aufgabensequenz planen
        workflow = await self.sequence_planner_agent.execute(
            prd, codebase, **kwargs
        )
        
        # 4. Templates für jede Aufgabe generieren
        template_paths = []
        for task in workflow.tasks:
            feature = next((f for f in features if f.id == task.feature_id), None)
            if not feature:
                continue
            
            template_path = await self.template_generation_agent.execute(
                task, feature, prd, output_dir, codebase, **kwargs
            )
            template_paths.append(template_path)
            
            # Task mit Template-Pfad aktualisieren
            task.template_path = template_path
        
        return workflow.id, template_paths
