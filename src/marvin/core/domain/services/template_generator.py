"""Template generator domain service."""

from ..entities.task import TaskDefinition, TaskTemplate
from ..value_objects.xml_template import XMLTemplateBuilder


class TemplateGenerator:
    """Service for generating XML templates for tasks."""
    
    def generate_template(self, task: TaskDefinition) -> TaskTemplate:
        """Generate an XML template for a single task."""
        builder = XMLTemplateBuilder()
        
        # Build the XML structure
        builder.create_root("ai-coding-task", version="1.0")
        builder.add_task_metadata(
            task_id=str(task.id),
            name=task.name,
            type=task.type.value,
        )
        
        # Add description
        builder.add_element("description", task.description)
        
        # Add context
        context_elem = builder.add_element("context")
        builder._current = context_elem
        
        if task.context.files_to_modify:
            files_elem = builder.add_element("files-to-modify")
            builder._current = files_elem
            for file in task.context.files_to_modify:
                builder.add_element("file", file)
            builder._current = context_elem
        
        if task.context.files_to_create:
            files_elem = builder.add_element("files-to-create")
            builder._current = files_elem
            for file in task.context.files_to_create:
                builder.add_element("file", file)
            builder._current = context_elem
        
        # Add acceptance criteria
        if task.acceptance_criteria:
            criteria_elem = builder.add_element("acceptance-criteria")
            builder._current = criteria_elem
            for criterion in task.acceptance_criteria:
                builder.add_element("criterion", criterion)
        
        # Build the template
        xml_template = builder.build()
        
        return TaskTemplate(
            task_id=task.id,
            template_content=xml_template.to_string(),
            format_version="1.0",
        )
