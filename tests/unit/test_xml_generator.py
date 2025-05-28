"""
Unit tests for XMLTemplateGenerator.

Following TDD approach - write tests first, then implement.
"""

from datetime import datetime
from pathlib import Path

import pytest
from lxml import etree

from marvin.core.domain.models import (
    PRD,
    Codebase,
    Component,
    Feature,
    FeatureStatus,
    Task,
    Technology,
)
from marvin.infrastructure.template_generator.xml_generator import XMLTemplateGenerator


class TestXMLTemplateGenerator:
    """Test cases for XMLTemplateGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = XMLTemplateGenerator()

        # Create test PRD
        self.test_prd = PRD(
            id="prd-001",
            title="E-Commerce Platform",
            description="A comprehensive e-commerce platform for online retail",
            author="Product Team",
            created_at=datetime(2025, 1, 20),
            updated_at=datetime(2025, 1, 20),
            version="2.0.0",
        )

        # Create test feature
        self.test_feature = Feature(
            id="user_authentication_00",
            name="User Authentication",
            description="Users should be able to sign up and log in securely",
            requirements=[
                "Email-based registration",
                "Secure password storage",
                "JWT token authentication",
                "Multi-factor authentication support",
            ],
            dependencies=["Database Setup"],
            status=FeatureStatus.PROPOSED,
            priority=0,
        )

        # Create test task
        self.test_task = Task(
            task_id="task-001",
            sequence_number=1,
            name="Implement User Registration",
            description="Create user registration functionality with email verification",
            feature_id=self.test_feature.id,
            depends_on=["database-setup"],
        )

        # Create test codebase
        self.test_codebase = Codebase(
            id="codebase-001",
            name="ecommerce-platform",
            root_path="/path/to/project",
            technologies=[
                Technology(name="Python", version="3.11", category="language"),
                Technology(name="FastAPI", version="0.104", category="framework"),
                Technology(name="PostgreSQL", version="15", category="database"),
            ],
            architecture_patterns=["Hexagonal Architecture", "CQRS"],
            components=[
                Component(
                    name="auth_service",
                    path="/auth",
                    type="module",
                    description="Authentication service",
                )
            ],
        )

    @pytest.mark.asyncio
    async def test_generate_task_template_creates_valid_xml(self):
        """Test that generator creates valid XML template."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            codebase=self.test_codebase,
        )

        # Assert - XML is valid
        is_valid, error = self.generator.validate_xml(xml_content)
        assert is_valid, f"Generated XML is invalid: {error}"

        # Assert - XML can be parsed
        root = etree.fromstring(xml_content.encode("utf-8"))
        assert root.tag == "CodingTask"

    @pytest.mark.asyncio
    async def test_populate_template_from_models(self):
        """Test that template is correctly populated from domain models."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            codebase=self.test_codebase,
        )

        # Parse XML for assertions
        root = etree.fromstring(xml_content.encode("utf-8"))

        # Assert - Basic task information
        task_id = root.find(".//TaskID").text
        assert task_id == "task-001"

        sequence_number = root.find(".//SequenceNumber").text
        assert sequence_number == "1"

        task_name = root.find(".//TaskName").text
        assert task_name == "Implement User Registration"

        # Assert - PRD information
        project_name = root.find(".//ProjectName").text
        assert project_name == "E-Commerce Platform"

        author = root.find(".//Author").text
        assert author == "Product Team"

        # Assert - Feature information
        purpose = root.find(".//Purpose").text
        assert "Users should be able to sign up and log in securely" in purpose

        # Assert - User stories are generated
        story_elements = root.findall(".//Story")
        assert len(story_elements) >= 1
        assert story_elements[0].get("role") == "User"

    @pytest.mark.asyncio
    async def test_generate_user_stories_from_feature(self):
        """Test that user stories are correctly generated from feature."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )

        # Parse and assert
        root = etree.fromstring(xml_content.encode("utf-8"))
        story_elements = root.findall(".//Story")

        assert len(story_elements) >= 1
        story = story_elements[0]

        # Check story attributes
        assert story.get("id") == "user_authentication_00_story_01"
        assert story.get("role") == "User"
        assert "User Authentication" in story.get("goal")
        assert story.get("acceptanceCriteria") is not None

    @pytest.mark.asyncio
    async def test_technology_stack_section_populated(self):
        """Test that technology stack section is populated from codebase."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            codebase=self.test_codebase,
        )

        # Parse and assert
        root = etree.fromstring(xml_content.encode("utf-8"))

        # Check languages
        language_elements = root.findall(".//Language")
        assert len(language_elements) >= 1
        python_lang = next(
            (lang for lang in language_elements if lang.get("name") == "Python"), None
        )
        assert python_lang is not None
        assert python_lang.get("version") == "3.11"

        # Check frameworks
        framework_elements = root.findall(".//Framework")
        assert len(framework_elements) >= 1
        fastapi_framework = next(
            (fw for fw in framework_elements if fw.get("name") == "FastAPI"), None
        )
        assert fastapi_framework is not None
        assert fastapi_framework.get("version") == "0.104"

    @pytest.mark.asyncio
    async def test_functional_requirements_extracted(self):
        """Test that functional requirements are extracted from feature."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )

        # Parse and assert
        root = etree.fromstring(xml_content.encode("utf-8"))
        functional_req = root.find(".//FunctionalRequirements").text

        assert "Email-based registration" in functional_req
        assert "Secure password storage" in functional_req
        assert "JWT token authentication" in functional_req

    @pytest.mark.asyncio
    async def test_dependencies_handled(self):
        """Test that task dependencies are correctly handled."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )

        # Parse and assert
        root = etree.fromstring(xml_content.encode("utf-8"))
        depends_on = root.find(".//DependsOn").text

        assert "database-setup" in depends_on

    @pytest.mark.asyncio
    async def test_missing_placeholders_filled(self):
        """Test that missing placeholders are filled with empty strings."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )

        # Assert - XML should not contain unfilled placeholders
        assert "{" not in xml_content or "}" not in xml_content.replace(
            "<?xml", ""
        ).replace("UTF-8?>", "")

    @pytest.mark.asyncio
    async def test_save_to_file_creates_output(self, tmp_path: Path):
        """Test that XML content can be saved to file."""
        # Setup
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )
        output_file = tmp_path / "output" / "task-001.xml"

        # Execute
        self.generator.save_to_file(xml_content, str(output_file))

        # Assert
        assert output_file.exists()
        assert output_file.read_text(encoding="utf-8") == xml_content

    @pytest.mark.asyncio
    async def test_custom_template_path_used(self, tmp_path: Path):
        """Test that custom template path is used when provided."""
        # Setup - Create custom template
        custom_template = """<?xml version="1.0" encoding="UTF-8"?>
<CustomTask>
    <TaskID>{task_id}</TaskID>
    <Name>{task_name}</Name>
</CustomTask>"""

        template_file = tmp_path / "custom_template.xml"
        template_file.write_text(custom_template, encoding="utf-8")

        # Execute
        custom_generator = XMLTemplateGenerator(template_path=str(template_file))
        xml_content = custom_generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
        )

        # Assert
        root = etree.fromstring(xml_content.encode("utf-8"))
        assert root.tag == "CustomTask"
        assert root.find(".//TaskID").text == "task-001"

    @pytest.mark.asyncio
    async def test_additional_context_merged(self):
        """Test that additional context is merged into template."""
        # Setup
        additional_context = {
            "business_domain": "E-Commerce",
            "stakeholder_name": "John Doe",
            "test_framework": "pytest",
        }

        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            additional_context=additional_context,
        )

        # Assert
        assert "E-Commerce" in xml_content
        assert "John Doe" in xml_content
        assert "pytest" in xml_content

    @pytest.mark.asyncio
    async def test_validate_xml_detects_invalid_xml(self):
        """Test that XML validation correctly detects invalid XML."""
        # Setup - Invalid XML
        invalid_xml = "<InvalidXML><UnclosedTag></InvalidXML>"

        # Execute
        is_valid, error = self.generator.validate_xml(invalid_xml)

        # Assert
        assert not is_valid
        assert error is not None

    @pytest.mark.asyncio
    async def test_validate_xml_accepts_valid_xml(self):
        """Test that XML validation accepts valid XML."""
        # Setup - Valid XML
        valid_xml = '<?xml version="1.0"?><Root><Child>Content</Child></Root>'

        # Execute
        is_valid, error = self.generator.validate_xml(valid_xml)

        # Assert
        assert is_valid
        assert error is None

    @pytest.mark.asyncio
    async def test_architecture_patterns_included(self):
        """Test that architecture patterns from codebase are included."""
        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            codebase=self.test_codebase,
        )

        # Parse and assert
        root = etree.fromstring(xml_content.encode("utf-8"))
        pattern = root.find(".//Pattern").text

        assert "Hexagonal Architecture" in pattern
        assert "CQRS" in pattern

    @pytest.mark.asyncio
    async def test_empty_codebase_handled_gracefully(self):
        """Test that empty codebase is handled gracefully."""
        # Setup - Empty codebase
        empty_codebase = Codebase(
            id="empty-001",
            name="empty-project",
            root_path="/empty",
        )

        # Execute
        xml_content = self.generator.generate_task_template(
            task=self.test_task,
            feature=self.test_feature,
            prd=self.test_prd,
            codebase=empty_codebase,
        )

        # Assert - Should still generate valid XML
        is_valid, error = self.generator.validate_xml(xml_content)
        assert is_valid, f"XML should be valid even with empty codebase: {error}"
