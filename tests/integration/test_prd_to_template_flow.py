"""
Integration tests for PRD → Template flow.

Tests the complete flow from PRD analysis to XML template generation.
Following TDD approach - write tests first, then implement.
"""

from pathlib import Path

import pytest
from lxml import etree

from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.domain.models import Task
from marvin.infrastructure.template_generator.xml_generator import XMLTemplateGenerator


class TestPRDToTemplateFlow:
    """Integration tests for the complete PRD → Template flow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.document_agent = DocumentAnalysisAgent()
        self.xml_generator = XMLTemplateGenerator()

    @pytest.mark.asyncio
    async def test_complete_prd_to_template_flow(self, tmp_path: Path):
        """Test complete flow from PRD analysis to XML template generation."""
        # Setup - Create a comprehensive PRD
        prd_content = """# Product Requirements Document: Task Management System

Version: 2.1.0
Author: Product Development Team
Date: 2025-01-20

## Executive Summary
A comprehensive task management system for teams to organize, track, and collaborate on projects effectively.

## Features

### Feature 1: User Authentication
Users should be able to create accounts and authenticate securely.

**Requirements:**
- REQ-1.1: Email-based registration with verification
- REQ-1.2: Secure password storage using bcrypt
- REQ-1.3: JWT token-based authentication
- REQ-1.4: Multi-factor authentication support

**Priority:** High (P0)

### Feature 2: Task Management
Users can create, edit, and organize tasks efficiently.

**Requirements:**
- REQ-2.1: Create tasks with title, description, due date
- REQ-2.2: Assign tasks to team members
- REQ-2.3: Set task priorities and categories
- REQ-2.4: Track task status and progress

**Dependencies:** User Authentication
**Priority:** High (P0)

### Feature 3: Team Collaboration
Enable team members to collaborate on shared projects.

**Requirements:**
- REQ-3.1: Create and manage project workspaces
- REQ-3.2: Real-time comments and updates
- REQ-3.3: File sharing and attachments
- REQ-3.4: Activity notifications

**Dependencies:** User Authentication, Task Management
**Priority:** Medium (P1)
"""

        prd_file = tmp_path / "task_management_prd.md"
        prd_file.write_text(prd_content)

        # Execute - Analyze PRD
        prd, features = await self.document_agent.execute(str(prd_file))

        # Verify PRD analysis
        assert prd.title == "Task Management System"
        assert prd.version == "2.1.0"
        assert prd.author == "Product Development Team"
        assert len(features) == 3

        # Verify features were extracted correctly
        auth_feature = next(f for f in features if "Authentication" in f.name)
        assert len(auth_feature.requirements) == 4
        assert auth_feature.priority == 0  # High priority

        task_feature = next(f for f in features if "Task Management" in f.name)
        assert len(task_feature.requirements) == 4
        assert "User Authentication" in task_feature.dependencies

        collab_feature = next(f for f in features if "Collaboration" in f.name)
        assert len(collab_feature.requirements) == 4
        assert len(collab_feature.dependencies) == 2

        # Create tasks for each feature
        tasks = []
        for i, feature in enumerate(features):
            task = Task(
                task_id=f"task-{i + 1:03d}",
                sequence_number=i + 1,
                name=f"Implement {feature.name}",
                description=f"Implement the {feature.name.lower()} feature with all requirements",
                feature_id=feature.id,
                depends_on=[
                    f"task-{j + 1:03d}"
                    for j, dep_feature in enumerate(features)
                    if dep_feature.name in feature.dependencies
                ],
            )
            tasks.append(task)

        # Execute - Generate XML templates for each task
        xml_templates = []
        for task, feature in zip(tasks, features, strict=False):
            xml_content = self.xml_generator.generate_task_template(
                task=task,
                feature=feature,
                prd=prd,
            )
            xml_templates.append(xml_content)

        # Verify XML generation
        assert len(xml_templates) == 3

        # Verify each XML template
        for i, (xml_content, task, feature) in enumerate(
            zip(xml_templates, tasks, features, strict=False)
        ):
            # Validate XML structure
            is_valid, error = self.xml_generator.validate_xml(xml_content)
            assert is_valid, f"Template {i + 1} XML is invalid: {error}"

            # Parse and verify content
            root = etree.fromstring(xml_content.encode("utf-8"))
            assert root.tag == "CodingTask"

            # Verify task information
            assert root.find(".//TaskID").text == task.task_id
            assert root.find(".//SequenceNumber").text == str(task.sequence_number)
            assert root.find(".//TaskName").text == task.name

            # Verify PRD information
            assert root.find(".//ProjectName").text == "Task Management System"
            assert root.find(".//Author").text == "Product Development Team"

            # Verify feature requirements
            functional_req = root.find(".//FunctionalRequirements").text
            for req in feature.requirements:
                assert req in functional_req

            # Verify dependencies for dependent tasks
            if task.depends_on:
                depends_on = root.find(".//DependsOn").text
                for dependency in task.depends_on:
                    assert dependency in depends_on

    @pytest.mark.asyncio
    async def test_prd_with_complex_nested_structure(self, tmp_path: Path):
        """Test flow with complex nested PRD structure."""
        # Setup - PRD with nested subsections
        prd_content = """# PRD: E-Commerce Platform

Version: 3.0.0
Author: Product Team

## Features

### 1. User Management
Complete user lifecycle management system.

#### 1.1 Registration
**Requirements:**
- Email verification required
- Password strength validation
- CAPTCHA integration

#### 1.2 Authentication
**Requirements:**
- Multi-factor authentication
- OAuth integration (Google, Facebook)
- Session management

**Dependencies:** Registration

### 2. Product Catalog
Product management and display system.

**Requirements:**
- Product CRUD operations
- Category management
- Inventory tracking
- Search and filtering

**Priority:** High (P0)
"""

        prd_file = tmp_path / "ecommerce_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.document_agent.execute(str(prd_file))

        # Verify complex structure handling
        assert len(features) == 2  # Should extract main features, not subsections

        user_mgmt = next(f for f in features if "User Management" in f.name)
        assert len(user_mgmt.requirements) >= 5  # Combined from subsections

        # Generate template for user management feature
        task = Task(
            task_id="task-001",
            sequence_number=1,
            name="Implement User Management",
            description="Implement complete user management system",
            feature_id=user_mgmt.id,
        )

        xml_content = self.xml_generator.generate_task_template(
            task=task,
            feature=user_mgmt,
            prd=prd,
        )

        # Verify XML contains consolidated requirements
        is_valid, error = self.xml_generator.validate_xml(xml_content)
        assert is_valid, f"XML is invalid: {error}"

        root = etree.fromstring(xml_content.encode("utf-8"))
        functional_req = root.find(".//FunctionalRequirements").text

        # Should contain requirements from both subsections
        assert "Email verification required" in functional_req
        assert "Multi-factor authentication" in functional_req

    @pytest.mark.asyncio
    async def test_error_handling_in_flow(self, tmp_path: Path):
        """Test error handling in the complete flow."""
        # Setup - Invalid PRD file
        invalid_file = tmp_path / "nonexistent.md"

        # Execute & Assert - Document analysis should handle missing file
        with pytest.raises(FileNotFoundError):
            await self.document_agent.execute(str(invalid_file))

        # Setup - PRD with no features
        minimal_prd = """# Minimal PRD

Version: 1.0.0
Author: Test

## Overview
This is a minimal PRD without features.
"""

        minimal_file = tmp_path / "minimal.md"
        minimal_file.write_text(minimal_prd)

        # Execute
        prd, features = await self.document_agent.execute(str(minimal_file))

        # Verify graceful handling
        assert prd.title == "Minimal PRD"
        assert len(features) == 0

        # XML generation should still work with empty features
        dummy_task = Task(
            task_id="task-001",
            sequence_number=1,
            name="Setup Project",
            description="Initial project setup",
            feature_id="setup",
        )

        # Create a dummy feature for testing
        from marvin.core.domain.models import Feature, FeatureStatus

        dummy_feature = Feature(
            id="setup",
            name="Project Setup",
            description="Initial project setup",
            status=FeatureStatus.PROPOSED,
        )

        xml_content = self.xml_generator.generate_task_template(
            task=dummy_task,
            feature=dummy_feature,
            prd=prd,
        )

        is_valid, error = self.xml_generator.validate_xml(xml_content)
        assert is_valid, f"XML should be valid even with minimal data: {error}"

    @pytest.mark.asyncio
    async def test_template_customization_in_flow(self, tmp_path: Path):
        """Test template customization in the complete flow."""
        # Setup - Custom template
        custom_template = """<?xml version="1.0" encoding="UTF-8"?>
<SimpleTask>
    <ID>{task_id}</ID>
    <Name>{task_name}</Name>
    <Project>{project_name}</Project>
    <Feature>{purpose}</Feature>
    <Requirements>{functional_requirements}</Requirements>
</SimpleTask>"""

        template_file = tmp_path / "custom.xml"
        template_file.write_text(custom_template)

        # Setup PRD
        prd_content = """# PRD: Simple App

Version: 1.0.0
Author: Dev Team

## Features

### Feature 1: Basic Functionality
Simple feature for testing.

**Requirements:**
- REQ-1: Basic requirement
"""

        prd_file = tmp_path / "simple_prd.md"
        prd_file.write_text(prd_content)

        # Execute with custom template
        prd, features = await self.document_agent.execute(str(prd_file))

        custom_generator = XMLTemplateGenerator(template_path=str(template_file))

        task = Task(
            task_id="simple-001",
            sequence_number=1,
            name="Implement Basic Feature",
            description="Implement basic functionality",
            feature_id=features[0].id,
        )

        xml_content = custom_generator.generate_task_template(
            task=task,
            feature=features[0],
            prd=prd,
        )

        # Verify custom template structure
        root = etree.fromstring(xml_content.encode("utf-8"))
        assert root.tag == "SimpleTask"
        assert root.find(".//ID").text == "simple-001"
        assert root.find(".//Project").text == "Simple App"

    @pytest.mark.asyncio
    async def test_save_generated_templates(self, tmp_path: Path):
        """Test saving generated templates to files."""
        # Setup
        prd_content = """# PRD: File Output Test

Version: 1.0.0
Author: Test Team

## Features

### Feature 1: File Operations
Handle file input/output operations.

**Requirements:**
- File read operations
- File write operations
- Error handling
"""

        prd_file = tmp_path / "file_test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.document_agent.execute(str(prd_file))

        task = Task(
            task_id="file-001",
            sequence_number=1,
            name="Implement File Operations",
            description="Implement file handling functionality",
            feature_id=features[0].id,
        )

        xml_content = self.xml_generator.generate_task_template(
            task=task,
            feature=features[0],
            prd=prd,
        )

        # Save to file
        output_dir = tmp_path / "templates"
        output_file = output_dir / f"{task.task_id}.xml"

        self.xml_generator.save_to_file(xml_content, str(output_file))

        # Verify file was saved
        assert output_file.exists()
        saved_content = output_file.read_text(encoding="utf-8")
        assert saved_content == xml_content

        # Verify saved content is valid XML
        is_valid, error = self.xml_generator.validate_xml(saved_content)
        assert is_valid, f"Saved XML is invalid: {error}"
