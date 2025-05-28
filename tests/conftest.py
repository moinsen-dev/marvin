"""
Global pytest configuration and fixtures for Marvin tests.
"""

import asyncio
import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_prd_content() -> str:
    """Sample PRD content for testing."""
    return """# Product Requirements Document: Task Management System

Version: 1.0.0
Author: Test Author
Date: 2025-01-01

## Overview
A simple task management system for teams.

## Features

### Feature 1: User Authentication
Users should be able to sign up and log in to the system.

**Requirements:**
- REQ-1.1: Email-based registration
- REQ-1.2: Secure password storage
- REQ-1.3: JWT-based authentication

**Dependencies:** None

### Feature 2: Task Management
Users should be able to create, update, and delete tasks.

**Requirements:**
- REQ-2.1: Create new tasks with title and description
- REQ-2.2: Update task status
- REQ-2.3: Delete tasks

**Dependencies:** User Authentication
"""


@pytest.fixture
def sample_prd_path(tmp_path: Path, sample_prd_content: str) -> Path:
    """Create a temporary PRD file for testing."""
    prd_file = tmp_path / "test_prd.md"
    prd_file.write_text(sample_prd_content)
    return prd_file


@pytest.fixture
def sample_codebase_path(tmp_path: Path) -> Path:
    """Create a temporary codebase structure for testing."""
    codebase = tmp_path / "sample_project"
    codebase.mkdir()

    # Create some sample files
    (codebase / "src").mkdir()
    (codebase / "src" / "__init__.py").touch()
    (codebase / "src" / "main.py").write_text(
        """
# Sample Python file
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
"""
    )

    (codebase / "requirements.txt").write_text("fastapi>=0.100.0\npydantic>=2.0.0\n")
    (codebase / "README.md").write_text("# Sample Project\n\nA test project.")

    return codebase


@pytest.fixture
def api_client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app."""
    from marvin.api import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
async def mock_llm_response():
    """Mock LLM response for testing ADK agents."""
    return {
        "prd_title": "Task Management System",
        "prd_version": "1.0.0",
        "prd_author": "Test Author",
        "prd_description": "A simple task management system for teams.",
        "features": [
            {
                "name": "User Authentication",
                "description": "Users should be able to sign up and log in to the system.",
                "requirements": [
                    "Email-based registration",
                    "Secure password storage",
                    "JWT-based authentication",
                ],
                "dependencies": [],
            },
            {
                "name": "Task Management",
                "description": "Users should be able to create, update, and delete tasks.",
                "requirements": [
                    "Create new tasks with title and description",
                    "Update task status",
                    "Delete tasks",
                ],
                "dependencies": ["User Authentication"],
            },
        ],
    }


# Markers for test categorization
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "unit: Unit tests that test individual components"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests that test multiple components"
    )
    config.addinivalue_line("markers", "slow: Tests that take a long time to run")
    config.addinivalue_line("markers", "adk: Tests that require ADK components")
