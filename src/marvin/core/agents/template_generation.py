"""Agent for generating AI coding task templates."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Codebase, Feature, PRD, Task
from marvin.infrastructure.template_generator.xml_generator import XMLTemplateGenerator


class TemplateGenerationAgent(Agent):
    """Agent for generating XML-based AI coding task templates."""
    
    def __init__(self, name: str = "template_generation", config: Optional[Dict[str, Any]] = None):
        """Initializes the TemplateGenerationAgent.
        
        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        super().__init__(name, config)
        self.template_generator = XMLTemplateGenerator()
    
    async def execute(
        self,
        task: Task,
        feature: Feature,
        prd: PRD,
        output_dir: str,
        codebase: Optional[Codebase] = None,
        **kwargs: Any,
    ) -> str:
        """Generates an XML template for an AI coding task.
        
        Args:
            task: The task for which the template should be generated
            feature: The feature to which the task belongs
            prd: The PRD to which the feature belongs
            output_dir: Output directory for the template
            codebase: (Optional) The analyzed codebase
            **kwargs: Additional parameters
            
        Returns:
            Path to the generated template
            
        Raises:
            IOError: If the template cannot be saved
        """
        # Create additional context for the template
        additional_context = await self._prepare_additional_context(task, feature, prd, codebase, **kwargs)
        
        # Generate template
        template_content = self.template_generator.generate_task_template(
            task, feature, prd, codebase, additional_context
        )
        
        # Check if the template is valid
        is_valid, error = self.template_generator.validate_xml(template_content)
        if not is_valid:
            raise ValueError(f"Generated template is invalid: {error}")
        
        # Create output path
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(
            output_dir, f"{task.sequence_number:02d}_{feature.id}_{task.task_id}.xml"
        )
        
        # Save template
        self.template_generator.save_to_file(template_content, output_path)
        
        return output_path
    
    async def _prepare_additional_context(
        self,
        task: Task,
        feature: Feature,
        prd: PRD,
        codebase: Optional[Codebase],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Prepares additional context for the template.
        
        Args:
            task: The task for which the template should be generated
            feature: The feature to which the task belongs
            prd: The PRD to which the feature belongs
            codebase: (Optional) The analyzed codebase
            **kwargs: Additional parameters
            
        Returns:
            Additional context for the template
        """
        # Here we would use Google ADK to improve the context
        # For now, we implement a simple context creation
        
        context = {}
        
        # Derive business domain from PRD title
        business_domain = prd.title.split(":")[1].strip() if ":" in prd.title else prd.title
        context["business_domain"] = business_domain
        
        # Add assumptions
        context["assumptions"] = f"Feature '{feature.name}' can be implemented independently."
        
        # Add risks
        context["risks"] = f"Changes to {feature.name} may affect other components."
        context["risk_mitigation"] = "Perform comprehensive tests"
        
        # Add affected components
        if codebase:
            affected_files = []
            affected_folders = []
            
            # In a complete implementation, we would use Context 7 here
            for component in codebase.components:
                # Simple heuristic: If the component name is contained in the feature name
                if component.name.lower() in feature.name.lower():
                    if component.type == "file":
                        affected_files.append(component.path)
                    elif component.type == "directory":
                        affected_folders.append(component.path)
            
            context["affected_files"] = ", ".join(affected_files[:5])
            context["affected_folders"] = ", ".join(affected_folders[:3])
        
        # Derive acceptance criteria from feature requirements
        if feature.requirements:
            context["acceptance_criteria"] = "\n".join(
                f"- {req}" for req in feature.requirements
            )
        
        # Estimate expected timeframe
        context["expected_timeframe"] = "1-2 days"
        
        return context
