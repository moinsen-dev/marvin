"""Process PRD use case - main orchestration."""

import time
from pathlib import Path
from typing import Optional

from ..domain.entities.analysis import AnalysisContext, AnalysisResult
from ..domain.entities.codebase import CodebaseAnalysis
from ..domain.entities.prd import PRDDocument
from ..domain.entities.task import TaskSequence
from ..domain.services import (
    CodebaseScanner,
    PRDAnalyzer,
    TaskSequencer,
    TemplateGenerator,
)
from ...infrastructure.ai import AIService


class ProcessPRDUseCase:
    """Main use case for processing PRD documents."""
    
    def __init__(
        self,
        prd_analyzer: PRDAnalyzer,
        codebase_scanner: CodebaseScanner,
        task_sequencer: TaskSequencer,
        template_generator: TemplateGenerator,
        ai_service: AIService,
    ) -> None:
        """Initialize the use case with required services."""
        self.prd_analyzer = prd_analyzer
        self.codebase_scanner = codebase_scanner
        self.task_sequencer = task_sequencer
        self.template_generator = template_generator
        self.ai_service = ai_service
    
    async def execute(
        self,
        prd_path: Path,
        codebase_path: Optional[Path] = None,
        output_dir: Optional[Path] = None,
    ) -> AnalysisResult:
        """Execute the complete PRD processing workflow."""
        start_time = time.time()
        
        # Create analysis context
        context = AnalysisContext()
        
        # Step 1: Analyze PRD
        prd_document = await self._analyze_prd(prd_path)
        context.prd_document = prd_document
        
        # Step 2: Scan codebase if provided
        if codebase_path:
            codebase_analysis = await self._scan_codebase(codebase_path)
            context.codebase_analysis = codebase_analysis
        
        # Step 3: Generate task sequence
        task_sequence = await self._generate_task_sequence(context)
        
        # Step 4: Generate templates
        templates = await self._generate_templates(task_sequence, context)
        
        # Step 5: Save results if output directory provided
        if output_dir:
            await self._save_results(output_dir, task_sequence, templates)
        
        # Create result
        result = AnalysisResult(
            context=context,
            task_sequence=task_sequence,
            generated_templates=templates,
            processing_time_seconds=time.time() - start_time,
        )
        
        # Add insights
        result.add_insight(f"Analyzed {len(prd_document.features)} features")
        result.add_insight(f"Generated {len(task_sequence.tasks)} tasks")
        
        if context.is_greenfield:
            result.add_insight("Greenfield project - no existing codebase constraints")
        else:
            result.add_insight(f"Existing codebase with {len(context.codebase_analysis.component_graph.components)} components")
        
        return result
    
    async def _analyze_prd(self, prd_path: Path) -> PRDDocument:
        """Analyze the PRD document."""
        content = prd_path.read_text()
        
        # Use AI to extract features
        ai_features = await self.ai_service.extract_features(content)
        
        # Use domain service to build PRD document
        prd_document = self.prd_analyzer.analyze_document(content, {"author": "AI Analysis"})
        
        # Enhance with AI-extracted features
        # (This would merge AI insights with pattern-based extraction)
        
        return prd_document
    
    async def _scan_codebase(self, codebase_path: Path) -> CodebaseAnalysis:
        """Scan and analyze the codebase."""
        # Collect relevant files
        file_contents = self.codebase_scanner.collect_files(codebase_path)
        
        # Use AI to analyze structure
        ai_analysis = await self.ai_service.analyze_codebase(file_contents)
        
        # Build codebase analysis
        return self.codebase_scanner.analyze_from_ai_result(codebase_path, ai_analysis)
    
    async def _generate_task_sequence(self, context: AnalysisContext) -> TaskSequence:
        """Generate the task sequence."""
        features = [
            {
                "id": str(f.id),
                "name": f.name,
                "description": f.description,
                "priority": str(f.priority),
                "dependencies": [str(d) for d in f.dependencies],
            }
            for f in context.prd_document.features
        ]
        
        codebase_info = None
        if context.has_codebase:
            codebase_info = {
                "primary_language": {
                    "name": context.codebase_analysis.technology_stack.primary_language.name
                    if context.codebase_analysis.technology_stack.primary_language
                    else "Unknown"
                }
            }
        
        # Generate tasks using AI
        ai_tasks = await self.ai_service.generate_task_sequence(features, codebase_info)
        
        # Build task sequence
        return self.task_sequencer.create_from_ai_result(ai_tasks, context)
    
    async def _generate_templates(self, task_sequence: TaskSequence, context: AnalysisContext) -> dict[str, str]:
        """Generate XML templates for all tasks."""
        templates = {}
        
        for task in task_sequence.tasks:
            task_dict = {
                "id": str(task.id),
                "name": task.name,
                "description": task.description,
                "type": str(task.type),
            }
            
            context_dict = {
                "is_greenfield": context.is_greenfield,
                "has_codebase": context.has_codebase,
            }
            
            template = await self.ai_service.generate_xml_template(task_dict, context_dict)
            templates[task.id] = template
        
        return templates
    
    async def _save_results(self, output_dir: Path, task_sequence: TaskSequence, templates: dict[str, str]) -> None:
        """Save results to output directory."""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save task sequence summary
        summary_path = output_dir / "task_sequence.json"
        # Would implement JSON serialization here
        
        # Save individual templates
        templates_dir = output_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        for task in task_sequence.tasks:
            if task.id in templates:
                template_path = templates_dir / f"{task.sequence_number:03d}_{task.name.replace(' ', '_')}.xml"
                template_path.write_text(templates[task.id])
