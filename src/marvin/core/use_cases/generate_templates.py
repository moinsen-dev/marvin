"""Use Case: Generation of AI coding task templates from a PRD."""

import os
import time
from typing import Any, List, Optional, Tuple

from marvin.core.agents.codebase_analysis import CodebaseAnalysisAgent
from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.agents.sequence_planner import SequencePlannerAgent
from marvin.core.agents.template_generation import TemplateGenerationAgent
from marvin.logging import get_logger


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
        self.codebase_analysis_agent = (
            codebase_analysis_agent or CodebaseAnalysisAgent()
        )
        self.sequence_planner_agent = sequence_planner_agent or SequencePlannerAgent()
        self.template_generation_agent = (
            template_generation_agent or TemplateGenerationAgent()
        )
        self.logger = get_logger("use_case.generate_templates")
        self.logger.info("GenerateTemplatesUseCase initialized")

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
        start_time = time.time()
        self.logger.info(f"Starting template generation process for PRD: {prd_path}")

        # Validate paths
        if not os.path.exists(prd_path):
            self.logger.error(f"PRD not found: {prd_path}")
            raise FileNotFoundError(f"PRD not found: {prd_path}")

        if codebase_path and not os.path.exists(codebase_path):
            self.logger.error(f"Codebase not found: {codebase_path}")
            raise FileNotFoundError(f"Codebase not found: {codebase_path}")

        try:
            # 1. Analyze PRD
            self.logger.info("Step 1: Analyzing PRD document")
            analysis_start = time.time()
            prd, features = await self.document_analysis_agent._timed_execute(
                prd_path, **kwargs
            )
            analysis_time = time.time() - analysis_start
            self.logger.info(
                f"PRD analysis completed in {analysis_time:.2f}s. Found {len(features)} features"
            )

            # 2. Analyze codebase (if present)
            codebase = None
            if codebase_path:
                self.logger.info(f"Step 2: Analyzing codebase: {codebase_path}")
                codebase_start = time.time()
                codebase = await self.codebase_analysis_agent._timed_execute(
                    codebase_path, name=prd.title, **kwargs
                )
                codebase_time = time.time() - codebase_start
                self.logger.info(f"Codebase analysis completed in {codebase_time:.2f}s")
            else:
                self.logger.info(
                    "Step 2: No codebase provided, skipping codebase analysis"
                )

            # 3. Plan task sequence
            self.logger.info("Step 3: Planning task sequence")
            planning_start = time.time()
            workflow = await self.sequence_planner_agent._timed_execute(
                prd, codebase, **kwargs
            )
            planning_time = time.time() - planning_start
            self.logger.info(
                f"Task sequence planning completed in {planning_time:.2f}s. Planned {len(workflow.tasks)} tasks"
            )

            # 4. Generate templates for each task
            self.logger.info(
                f"Step 4: Generating templates for {len(workflow.tasks)} tasks"
            )
            template_paths = []
            template_start = time.time()

            for i, task in enumerate(workflow.tasks):
                self.logger.debug(
                    f"Generating template for task {i + 1}/{len(workflow.tasks)}: {task.title}"
                )
                feature = next((f for f in features if f.id == task.feature_id), None)
                if not feature:
                    self.logger.warning(
                        f"Feature with ID {task.feature_id} not found for task {task.id}"
                    )
                    continue

                task_start = time.time()
                template_path = await self.template_generation_agent._timed_execute(
                    task, feature, prd, output_dir, codebase, **kwargs
                )
                task_time = time.time() - task_start
                self.logger.debug(
                    f"Template for task {task.id} generated in {task_time:.2f}s: {template_path}"
                )

                template_paths.append(template_path)

                # Update task with template path
                task.template_path = template_path

            template_time = time.time() - template_start
            total_time = time.time() - start_time

            self.logger.info(
                f"Template generation completed in {template_time:.2f}s. Generated {len(template_paths)} templates"
            )
            self.logger.info(f"Total execution time: {total_time:.2f}s")
            self.logger.info(f"Output directory: {output_dir}")

            return workflow.id, template_paths

        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(
                f"Error in template generation process after {execution_time:.2f}s: {str(e)}"
            )
            raise
