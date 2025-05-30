"""
Enhanced Markdown PRD Parser Tests - Following TDD Methodology

Tests for Issue #2: Enhanced Markdown PRD Parser with Advanced Feature Extraction
Following strict TDD approach - write tests first, then implement.

Acceptance Criteria Coverage:
- Parse complex nested markdown structures (headers, lists, tables)
- Extract feature titles, descriptions, and requirements with 95% accuracy
- Support metadata extraction (version, author, dates, status)
- Handle priority and effort estimation extraction from text
- Detect and parse user stories in multiple formats
- Extract acceptance criteria and definition of done
- Support markdown tables for requirements matrices
- Generate feature dependency graphs from markdown content
- Validate extracted data against PRD schema
- Achieve 100% test coverage for all new functionality
"""

from datetime import datetime
from pathlib import Path

import pytest

from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.domain.models import FeatureStatus


class TestEnhancedMarkdownParser:
    """Test cases for enhanced markdown parsing capabilities."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = DocumentAnalysisAgent()

    @pytest.mark.asyncio
    async def test_parse_complex_nested_structure(self, tmp_path: Path):
        """Test parsing of complex nested markdown structures."""
        # RED: This test will fail - we need to implement enhanced parsing
        prd_content = """---
title: Advanced Task Management System
version: 2.1.0
author: Jane Smith
status: Draft
priority: High
---

# Product Requirements Document: Advanced Task Management System

## 1. Overview
This PRD outlines the requirements for an advanced task management system.

### 1.1 Background
Current systems lack advanced features.

### 1.2 Goals
- Improve productivity by 50%
- Reduce task overhead

## 2. Features

### 2.1 User Authentication
**Priority**: High | **Effort**: 8 Story Points

#### Description
Secure user authentication system with multi-factor support.

#### Requirements
- [ ] Email/password authentication
- [ ] Multi-factor authentication (MFA)
- [ ] Social login integration

#### User Stories
- As a user, I want to log in securely so that my data is protected
- As an admin, I want to manage user accounts so that I can control access

#### Acceptance Criteria
- Given a valid email and password, when user logs in, then access is granted
- Given invalid credentials, when user attempts login, then access is denied
- Given MFA is enabled, when user logs in, then second factor is required

#### Dependencies
- None

### 2.2 Task Management
**Priority**: High | **Effort**: 13 Story Points

#### Description
Core task management functionality with advanced features.

#### Requirements
- [ ] Create, edit, delete tasks
- [ ] Task prioritization
- [ ] Due date management
- [ ] Task assignment

#### Dependencies
- User Authentication (2.1)

## 3. Requirements Matrix

| Feature | Priority | Effort | Dependencies | Status |
|---------|----------|--------|--------------|--------|
| User Authentication | High | 8 SP | None | Not Started |
| Task Management | High | 13 SP | User Authentication | Not Started |
| Notifications | Medium | 5 SP | Task Management | Not Started |

## 4. Technical Requirements

### 4.1 Performance
- Page load time < 2 seconds
- Support 10,000 concurrent users

### 4.2 Security
- HTTPS only
- Data encryption at rest
"""

        # Create test file
        prd_file = tmp_path / "complex_prd.md"
        prd_file.write_text(prd_content)

        # Execute analysis
        prd, features = await self.agent.execute(str(prd_file))

        # Assert metadata extraction
        assert prd.title == "Advanced Task Management System"
        assert prd.version == "2.1.0"
        assert prd.author == "Jane Smith"
        assert hasattr(prd, 'metadata')
        assert prd.metadata.get('status') == 'Draft'
        assert prd.metadata.get('priority') == 'High'

        # Assert feature extraction with nested structure
        assert len(features) >= 2

        auth_feature = next((f for f in features if "Authentication" in f.title), None)
        assert auth_feature is not None
        assert auth_feature.title == "User Authentication"
        assert auth_feature.priority == 0  # High priority
        # Check if effort is extracted correctly (flexible format matching)
        assert (auth_feature.effort and "8" in auth_feature.effort) or "8 Story Points" in auth_feature.description

        task_feature = next((f for f in features if "Task Management" in f.title), None)
        assert task_feature is not None
        assert task_feature.dependencies == ["User Authentication"]

    @pytest.mark.asyncio
    async def test_extract_metadata_from_frontmatter(self, tmp_path: Path):
        """Test extraction of metadata from YAML frontmatter."""
        # RED: This test will fail - we need frontmatter parsing
        prd_content = """---
title: "E-commerce Platform"
version: "3.0.0"
author: "Product Team"
created_date: "2024-01-15"
last_modified: "2024-01-20"
status: "In Review"
stakeholders:
  - "Engineering"
  - "Design"
  - "Marketing"
tags:
  - "e-commerce"
  - "platform"
  - "web"
---

# E-commerce Platform Requirements

## Overview
This document outlines requirements for our new e-commerce platform.
"""

        prd_file = tmp_path / "metadata_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Assert metadata extraction
        assert prd.title == "E-commerce Platform"
        assert prd.version == "3.0.0"
        assert prd.author == "Product Team"
        assert prd.metadata.get('status') == 'In Review'
        assert prd.metadata.get('created_date') == '2024-01-15'
        assert 'Engineering' in prd.metadata.get('stakeholders', [])

    @pytest.mark.asyncio
    async def test_extract_priority_and_effort_estimation(self, tmp_path: Path):
        """Test extraction of priority and effort estimations from text."""
        # RED: This test will fail - we need intelligent text parsing
        prd_content = """# Mobile App Features

## Push Notifications
This is a **critical priority** feature that will require approximately *3 weeks* of development.
**Effort Estimate**: 15 story points
**Priority Level**: Must Have

## User Profile
This feature has **medium priority** and should take about *1 week* to implement.
Estimated effort: 5 SP
Priority: Should Have

## Analytics Dashboard
**Low priority** feature requiring significant effort (*2 months* development time).
Story Points: 25
Priority: Could Have
"""

        prd_file = tmp_path / "estimation_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Assert priority extraction
        push_feature = next((f for f in features if "Push Notifications" in f.title), None)
        assert push_feature is not None
        assert push_feature.priority in ["Critical", "Must Have", "High"]
        assert "15" in str(push_feature.effort) or push_feature.effort == "15 SP"

        profile_feature = next((f for f in features if "User Profile" in f.title), None)
        assert profile_feature is not None
        assert profile_feature.priority in ["Medium", "Should Have"]

    @pytest.mark.asyncio
    async def test_parse_user_stories_multiple_formats(self, tmp_path: Path):
        """Test parsing of user stories in multiple formats."""
        # RED: This test will fail - we need user story pattern recognition
        prd_content = """# User Story Examples

## Login Feature

### Format 1: Standard User Stories
- As a customer, I want to log in with my email so that I can access my account
- As an admin, I want to view user login history so that I can monitor security

### Format 2: Given-When-Then
- Given I am on the login page, When I enter valid credentials, Then I should be redirected to dashboard
- Given I enter invalid credentials, When I click login, Then I should see an error message

### Format 3: Job Stories
- When I need to access my account, I want to log in quickly so I can complete my tasks without delay

### Format 4: Simple Stories
- User can log in with email and password
- System validates credentials against database
- Failed login attempts are logged for security
"""

        prd_file = tmp_path / "user_stories_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        login_feature = next((f for f in features if "Login" in f.title), None)
        assert login_feature is not None

        # Should extract multiple user stories
        assert hasattr(login_feature, 'user_stories')
        assert len(login_feature.user_stories) >= 3

        # Should recognize different formats
        user_story_formats = [story.format for story in login_feature.user_stories if hasattr(story, 'format')]
        assert 'as_a_user' in user_story_formats or 'given_when_then' in user_story_formats

    @pytest.mark.asyncio
    async def test_extract_acceptance_criteria(self, tmp_path: Path):
        """Test extraction of acceptance criteria and definition of done."""
        # RED: This test will fail - we need acceptance criteria parsing
        prd_content = """# Search Functionality

## Description
Implement global search across all content types.

## Acceptance Criteria
1. Search should return results within 2 seconds
2. Results should be ranked by relevance
3. Search should support autocomplete
4. Search should handle typos and fuzzy matching
5. Empty search should show recent/popular items

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Unit tests written with 90%+ coverage
- [ ] Performance tests validate 2-second requirement
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Accessibility audit passed

## Additional Requirements
- Search must work offline with cached results
- Search history should be saved for logged-in users
"""

        prd_file = tmp_path / "acceptance_criteria_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        search_feature = next((f for f in features if "Search" in f.title), None)
        assert search_feature is not None

        # Should extract acceptance criteria
        assert hasattr(search_feature, 'acceptance_criteria')
        assert len(search_feature.acceptance_criteria) >= 5
        assert any("2 seconds" in criteria for criteria in search_feature.acceptance_criteria)

        # Should extract definition of done
        assert hasattr(search_feature, 'definition_of_done')
        assert len(search_feature.definition_of_done) >= 5
        assert any("Unit tests" in item for item in search_feature.definition_of_done)

    @pytest.mark.asyncio
    async def test_parse_requirements_matrix_table(self, tmp_path: Path):
        """Test parsing of markdown tables for requirements matrices."""
        # RED: This test will fail - we need table parsing
        prd_content = """# Requirements Matrix

## Feature Overview

| Feature ID | Feature Name | Priority | Effort (SP) | Owner | Dependencies | Status |
|------------|--------------|----------|-------------|--------|--------------|--------|
| F001 | User Registration | High | 8 | Frontend Team | None | In Progress |
| F002 | User Profile | Medium | 5 | Frontend Team | F001 | Not Started |
| F003 | Payment System | High | 13 | Backend Team | F001, F002 | Planning |
| F004 | Order History | Low | 3 | Backend Team | F003 | Not Started |

## Technical Requirements Matrix

| Requirement | Category | Priority | Acceptance Criteria |
|-------------|----------|----------|-------------------|
| Page Load Speed | Performance | High | < 2 seconds |
| Uptime | Reliability | High | 99.9% |
| Mobile Support | Compatibility | Medium | iOS & Android |
"""

        prd_file = tmp_path / "matrix_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Should extract features from table
        assert len(features) >= 4

        reg_feature = next((f for f in features if f.id == "F001"), None)
        assert reg_feature is not None
        assert reg_feature.title == "User Registration"
        assert reg_feature.priority == "High"
        assert reg_feature.effort == "8 SP"

        payment_feature = next((f for f in features if f.id == "F003"), None)
        assert payment_feature is not None
        assert len(payment_feature.dependencies) == 2
        assert "F001" in payment_feature.dependencies
        assert "F002" in payment_feature.dependencies

    @pytest.mark.asyncio
    async def test_generate_dependency_graph(self, tmp_path: Path):
        """Test generation of feature dependency graphs from markdown content."""
        # RED: This test will fail - we need dependency graph generation
        prd_content = """# Dependency Example

## Authentication Service
**ID**: AUTH-001
**Dependencies**: None

## User Profile
**ID**: PROFILE-001
**Dependencies**: Authentication Service (AUTH-001)

## Shopping Cart
**ID**: CART-001
**Dependencies**: User Profile (PROFILE-001), Authentication Service (AUTH-001)

## Payment Processing
**ID**: PAYMENT-001
**Dependencies**: Shopping Cart (CART-001)

## Order Management
**ID**: ORDER-001
**Dependencies**: Payment Processing (PAYMENT-001), User Profile (PROFILE-001)
"""

        prd_file = tmp_path / "dependency_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Should extract dependency relationships
        cart_feature = next((f for f in features if "Shopping Cart" in f.title), None)
        assert cart_feature is not None
        assert len(cart_feature.dependencies) == 2

        # Should generate dependency graph
        assert hasattr(prd, 'dependency_graph')
        graph = prd.dependency_graph

        # Verify graph structure
        assert 'AUTH-001' in graph
        assert 'PROFILE-001' in graph['AUTH-001']  # Profile depends on Auth
        assert 'CART-001' in graph['PROFILE-001']   # Cart depends on Profile

    @pytest.mark.asyncio
    async def test_validate_extracted_data_against_schema(self, tmp_path: Path):
        """Test validation of extracted data against PRD schema."""
        # RED: This test will fail - we need schema validation
        prd_content = """# Valid PRD Structure

## Feature: Data Validation
**Priority**: High
**Effort**: 5 SP
**Status**: Not Started

This feature ensures all data meets our quality standards.
"""

        prd_file = tmp_path / "validation_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Should validate PRD schema
        assert prd.is_valid()
        assert prd.title is not None
        assert prd.created_at is not None

        # Should validate feature schema
        feature = features[0]
        assert feature.is_valid()
        assert feature.title is not None
        assert feature.priority in ["High", "Medium", "Low"]
        assert feature.status in [status.value for status in FeatureStatus]

    @pytest.mark.asyncio
    async def test_performance_large_document(self, tmp_path: Path):
        """Test parsing performance with large documents (10MB target)."""
        # RED: This test will fail - we need performance optimization

        # Generate large PRD content
        large_content = """# Large PRD Performance Test

## Overview
This is a performance test for large documents.

"""

        # Add many features to create large document
        for i in range(1000):
            large_content += f"""
## Feature {i:04d}: Test Feature {i}
**Priority**: {'High' if i % 3 == 0 else 'Medium' if i % 3 == 1 else 'Low'}
**Effort**: {(i % 20) + 1} SP

### Description
This is test feature number {i} designed to test parser performance.

### Requirements
- Requirement 1 for feature {i}
- Requirement 2 for feature {i}
- Requirement 3 for feature {i}

### User Stories
- As a user, I want feature {i} so that I can accomplish task {i}

### Acceptance Criteria
- Given feature {i} is implemented
- When user interacts with feature {i}
- Then expected outcome {i} occurs

"""

        prd_file = tmp_path / "large_prd.md"
        prd_file.write_text(large_content)

        # Should be approximately 10MB
        file_size = prd_file.stat().st_size
        assert file_size > 5_000_000  # At least 5MB

        # Measure parsing time
        start_time = datetime.now()
        prd, features = await self.agent.execute(str(prd_file))
        parse_time = (datetime.now() - start_time).total_seconds()

        # Should parse in under 5 seconds (acceptance criteria)
        assert parse_time < 5.0

        # Should extract all features
        assert len(features) == 1000

    @pytest.mark.asyncio
    async def test_extract_95_percent_accuracy_benchmark(self, tmp_path: Path):
        """Test 95% accuracy benchmark for feature extraction."""
        # RED: This test will fail - we need accuracy measurement
        prd_content = """# Accuracy Benchmark Test

## Feature 1: User Authentication
Priority: High
Effort: 8 SP

## Feature 2: Data Export
Priority: Medium
Effort: 5 SP

## Feature 3: Real-time Notifications
Priority: High
Effort: 13 SP

## Feature 4: Analytics Dashboard
Priority: Low
Effort: 21 SP

## Feature 5: Mobile App
Priority: Medium
Effort: 34 SP
"""

        prd_file = tmp_path / "accuracy_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))

        # Expected features (ground truth)
        expected_features = [
            {"title": "User Authentication", "priority": "High", "effort": "8 SP"},
            {"title": "Data Export", "priority": "Medium", "effort": "5 SP"},
            {"title": "Real-time Notifications", "priority": "High", "effort": "13 SP"},
            {"title": "Analytics Dashboard", "priority": "Low", "effort": "21 SP"},
            {"title": "Mobile App", "priority": "Medium", "effort": "34 SP"}
        ]

        # Calculate accuracy
        correct_extractions = 0
        total_expected = len(expected_features)

        for expected in expected_features:
            found_feature = next(
                (f for f in features if expected["title"].lower() in f.title.lower()),
                None
            )
            if found_feature and found_feature.priority == expected["priority"]:
                correct_extractions += 1

        accuracy = correct_extractions / total_expected

        # Should achieve 95% accuracy (acceptance criteria)
        assert accuracy >= 0.95, f"Accuracy {accuracy:.2%} below 95% threshold"
        assert len(features) == total_expected


class TestEnhancedMarkdownParserEdgeCases:
    """Test edge cases and error handling for enhanced markdown parser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = DocumentAnalysisAgent()

    @pytest.mark.asyncio
    async def test_malformed_frontmatter(self, tmp_path: Path):
        """Test handling of malformed YAML frontmatter."""
        prd_content = """---
title: "Malformed Example
version: 2.0.0
author: [invalid yaml
status: Draft
---

# Document with Malformed Frontmatter
Content should still be parseable.
"""

        prd_file = tmp_path / "malformed_prd.md"
        prd_file.write_text(prd_content)

        # Should handle gracefully without crashing
        prd, features = await self.agent.execute(str(prd_file))
        assert prd.title is not None  # Should fall back to document title

    @pytest.mark.asyncio
    async def test_empty_document(self, tmp_path: Path):
        """Test handling of empty or minimal documents."""
        prd_content = "# Empty PRD\n\nThis document has no features."

        prd_file = tmp_path / "empty_prd.md"
        prd_file.write_text(prd_content)

        prd, features = await self.agent.execute(str(prd_file))
        assert prd.title == "Empty PRD"
        assert len(features) == 0

    @pytest.mark.asyncio
    async def test_unicode_and_special_characters(self, tmp_path: Path):
        """Test handling of Unicode and special characters."""
        prd_content = """# PRD avec Caractères Spéciaux 🚀

## Función de Autenticación
**Prioridad**: Alta
**Esfuerzo**: 8 SP

### Descripción
Esta función permite a los usuarios autenticarse de forma segura.

## 功能：用户管理
**优先级**: 高
**工作量**: 13 SP

### 描述
用户管理功能包括创建、编辑和删除用户账户。
"""

        prd_file = tmp_path / "unicode_prd.md"
        prd_file.write_text(prd_content, encoding='utf-8')

        prd, features = await self.agent.execute(str(prd_file))
        assert "🚀" in prd.title
        assert len(features) >= 2

        # Should handle Unicode feature names
        spanish_feature = next((f for f in features if "Autenticación" in f.title), None)
        assert spanish_feature is not None

        chinese_feature = next((f for f in features if "用户管理" in f.title), None)
        assert chinese_feature is not None
