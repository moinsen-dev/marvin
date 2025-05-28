"""
Unit tests for DocumentAnalysisAgent.

Following TDD approach - write tests first, then implement.
"""

from pathlib import Path

import pytest

from marvin.core.agents.document_analysis import DocumentAnalysisAgent


class TestDocumentAnalysisAgent:
    """Test cases for DocumentAnalysisAgent."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = DocumentAnalysisAgent()

    @pytest.mark.asyncio
    async def test_analyze_markdown_extracts_title(self, tmp_path: Path):
        """Test that agent correctly extracts PRD title from markdown."""
        # Create test PRD content
        prd_content = """# Product Requirements Document: Task Management System

Version: 1.0.0
Author: John Doe

## Overview
A simple task management system.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert prd.title == "Task Management System"

    @pytest.mark.asyncio
    async def test_analyze_markdown_extracts_metadata(self, tmp_path: Path):
        """Test that agent extracts version and author metadata."""
        prd_content = """# Product Requirements Document: My App

Version: 2.1.0
Author: Jane Smith
Date: 2025-01-15

## Overview
An application.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert prd.version == "2.1.0"
        assert prd.author == "Jane Smith"

    @pytest.mark.asyncio
    async def test_analyze_markdown_extracts_features(self, tmp_path: Path):
        """Test that agent extracts features from markdown sections."""
        prd_content = """# PRD: Test App

## Features

### Feature 1: User Authentication
Users should be able to sign up and log in.

### Feature 2: Task Management
Users can create and manage tasks.

### Feature 3: Reporting
Generate reports on task completion.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert len(features) == 3
        assert features[0].name == "User Authentication"
        assert features[1].name == "Task Management"
        assert features[2].name == "Reporting"

    @pytest.mark.asyncio
    async def test_analyze_markdown_parses_requirements(self, tmp_path: Path):
        """Test that agent extracts requirements for each feature."""
        prd_content = """# PRD: Test App

## Features

### Feature 1: User Authentication
Users should be able to authenticate.

**Requirements:**
- REQ-1.1: Email-based registration
- REQ-1.2: Secure password storage
- REQ-1.3: JWT token authentication
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert len(features) == 1
        feature = features[0]
        assert len(feature.requirements) == 3
        assert "Email-based registration" in feature.requirements[0]
        assert "Secure password storage" in feature.requirements[1]
        assert "JWT token authentication" in feature.requirements[2]

    @pytest.mark.asyncio
    async def test_analyze_markdown_handles_dependencies(self, tmp_path: Path):
        """Test that agent correctly parses feature dependencies."""
        prd_content = """# PRD: Test App

## Features

### Feature 1: User Authentication
Basic auth system.

### Feature 2: Task Management
Task CRUD operations.

**Dependencies:** User Authentication

### Feature 3: Reporting
Generate reports.

**Dependencies:** Task Management, User Authentication
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert len(features) == 3
        assert features[0].dependencies == []
        assert features[1].dependencies == ["User Authentication"]
        assert set(features[2].dependencies) == {
            "Task Management",
            "User Authentication",
        }

    @pytest.mark.asyncio
    async def test_analyze_markdown_handles_priority(self, tmp_path: Path):
        """Test that agent extracts priority information."""
        prd_content = """# PRD: Test App

## Features

### Feature 1: Core Auth
**Priority:** High (P0)
Must have authentication.

### Feature 2: Nice Feature
**Priority:** Low (P2)
Nice to have feature.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert features[0].priority == 0  # High priority
        assert features[1].priority == 2  # Low priority

    @pytest.mark.asyncio
    async def test_analyze_markdown_generates_feature_ids(self, tmp_path: Path):
        """Test that agent generates unique feature IDs."""
        prd_content = """# PRD: Test App

## Features

### User Login
Allow users to log in.

### User Logout
Allow users to log out.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert len(features) == 2
        assert features[0].id.startswith("user_login")
        assert features[1].id.startswith("user_logout")
        assert features[0].id != features[1].id

    @pytest.mark.asyncio
    async def test_analyze_markdown_handles_malformed_content(self, tmp_path: Path):
        """Test that agent handles malformed markdown gracefully."""
        prd_content = """This is not a proper PRD

Just some random text
Without proper structure
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert - should still create a PRD with defaults
        assert prd is not None
        assert prd.title == "Unknown PRD"
        assert prd.version == "0.0.0"
        assert len(features) == 0

    @pytest.mark.asyncio
    async def test_analyze_markdown_with_complex_structure(self, tmp_path: Path):
        """Test analysis of PRD with complex nested structure."""
        prd_content = """# Product Requirements Document: E-Commerce Platform

Version: 3.0.0
Author: Product Team
Date: 2025-01-20

## Executive Summary
A comprehensive e-commerce platform.

## Features

### 1. User Management
Complete user lifecycle management.

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
Product management system.

**Requirements:**
- Product CRUD operations
- Category management
- Inventory tracking

**Priority:** High (P0)

### 3. Shopping Cart
**Requirements:**
- Add/remove items
- Quantity updates
- Price calculations

**Dependencies:** User Management, Product Catalog
**Priority:** High (P0)
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert prd.title == "E-Commerce Platform"
        assert prd.version == "3.0.0"
        assert prd.author == "Product Team"

        # Should extract main features, not sub-sections
        assert len(features) == 3

        # Check User Management feature
        user_mgmt = next(f for f in features if "User Management" in f.name)
        assert (
            len(user_mgmt.requirements) >= 5
        )  # Combined requirements from subsections

        # Check dependencies
        cart_feature = next(f for f in features if "Shopping Cart" in f.name)
        assert "User Management" in cart_feature.dependencies
        assert "Product Catalog" in cart_feature.dependencies

    @pytest.mark.asyncio
    async def test_execute_with_nonexistent_file(self):
        """Test execution with non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            await self.agent.execute("nonexistent_file.md")

    @pytest.mark.asyncio
    async def test_execute_with_unsupported_format(self, tmp_path: Path):
        """Test execution with unsupported file format."""
        # Create a non-markdown file
        test_file = tmp_path / "test.xyz"
        test_file.write_text("Some content")

        with pytest.raises(ValueError, match="Unsupported document format"):
            await self.agent.execute(str(test_file))

    @pytest.mark.asyncio
    async def test_analyze_markdown_extracts_description(self, tmp_path: Path):
        """Test that agent extracts PRD description from overview section."""
        prd_content = """# PRD: Amazing App

## Overview
This is an amazing application that helps users manage their daily tasks
efficiently. It provides a simple and intuitive interface for productivity.

## Features
### Task Creation
Create tasks easily.
"""
        prd_file = tmp_path / "test_prd.md"
        prd_file.write_text(prd_content)

        # Execute
        prd, features = await self.agent.execute(str(prd_file))

        # Assert
        assert "amazing application" in prd.description.lower()
        assert "manage their daily tasks" in prd.description
