# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Marvin is an intelligent tool that analyzes Product Requirement Documents (PRDs) and converts them into structured AI-Coding-Tasks. It generates XML-based task templates for AI coding assistants (Cursor, Windsurf, Claude Code).

## 🚨 CRITICAL: Test-Driven Development (TDD) Workflow

**MANDATORY**: Follow this TDD workflow for EVERY implementation:

### The TDD Cycle (Red-Green-Refactor)

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve the code while keeping tests green
4. **VERIFY**: Run code quality checks after EVERY step

### Implementation Workflow

For EACH feature from the STATE_TRACKER.md:

```bash
# 1. Create/update test file FIRST
uv run pytest tests/unit/test_<feature>.py -v  # Should FAIL (RED)

# 2. Implement minimal code to pass the test
# Edit the implementation file...

# 3. Run test again
uv run pytest tests/unit/test_<feature>.py -v  # Should PASS (GREEN)

# 4. Run ALL code quality checks (MANDATORY after each implementation)
uv run black src tests
uv run isort src tests  
uv run ruff check src tests --fix
uv run mypy src
uv run pytest --cov=marvin --cov-report=term-missing

# 5. Fix any issues before proceeding to next feature
```

### Code Quality Check Script

Create and run this after EVERY implementation step:

```bash
#!/bin/bash
# check_code.sh
echo "🔍 Running code quality checks..."
uv run black src tests || exit 1
uv run isort src tests || exit 1
uv run ruff check src tests --fix || exit 1
uv run mypy src || exit 1
echo "✅ Code quality checks passed!"
```

## 📦 Package Management with uv

**ALWAYS use `uv` - NEVER use pip directly!**

### Essential uv Commands

```bash
# Virtual environment (automatic with uv)
uv venv                          # Create venv
source .venv/bin/activate        # Activate (Linux/Mac)
.venv\Scripts\activate           # Activate (Windows)

# Package management
uv pip install -e .              # Install project in dev mode
uv pip install -e ".[dev]"       # Install with dev dependencies
uv add <package>                 # Add new dependency
uv pip sync requirements.txt     # Sync exact dependencies
uv pip list                      # List installed packages
uv pip freeze > requirements.txt # Export dependencies

# Running commands
uv run pytest                    # Run command in venv
uv run python -m marvin          # Run module

# Tools
uvx ruff check .                 # Run tool without installing
uv tool install ruff             # Install tool globally
```

## 🧪 Testing Guidelines

### Test Structure

```python
# tests/unit/test_<module>.py
import pytest
from unittest.mock import Mock, patch

class Test<ClassName>:
    """Test cases for <ClassName>."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Initialize test objects
    
    def test_<method>_<scenario>_<expected_result>(self):
        """Test that <method> <expected behavior> when <scenario>."""
        # Arrange
        # Act  
        # Assert
```

### ADK Agent Testing

```python
# tests/unit/test_<agent>_adk.py
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

def test_agent_basic_functionality():
    """Test agent's basic ability via session file."""
    AgentEvaluator.evaluate(
        agent_module="marvin.agents.<agent_name>",
        eval_dataset_file_path_or_dir="tests/fixtures/<agent>/test.json",
    )
```

### Async Testing

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    """Test async functionality."""
    result = await async_function()
    assert result == expected
```

## 🛠️ Development Commands

### Testing Commands
```bash
# Run all tests
uv run pytest -v

# Run specific test file
uv run pytest tests/unit/test_domain_models.py -v

# Run with coverage
uv run pytest --cov=marvin --cov-report=term-missing

# Run only marked tests
uv run pytest -m "not slow" -v

# Run tests in parallel
uv run pytest -n auto
```

### Code Quality Commands
```bash
# Format code (ALWAYS run after changes)
uv run black src tests

# Sort imports (ALWAYS run after changes)
uv run isort src tests

# Lint with Ruff (ALWAYS run after changes)
uv run ruff check src tests --fix

# Type checking (ALWAYS run after changes)
uv run mypy src

# All checks in one command
uv run black src tests && uv run isort src tests && uv run ruff check src tests --fix && uv run mypy src
```

### Running Marvin
```bash
# Process a PRD
uv run marvin process <prd_file> [--codebase <path>] [--output <dir>]

# Start API server
uv run marvin server [--host 0.0.0.0] [--port 8000]

# Run as module
uv run python -m marvin
```

## 🏗️ Architecture

The project follows Hexagonal Architecture (Ports & Adapters):

```
marvin/
├── core/               # Domain logic (test first!)
│   ├── domain/         # Models (Feature, PRD, Task, etc.)
│   ├── use_cases/      # Business rules
│   └── agents/         # Core agent logic
├── adapters/           # External interfaces
│   ├── cli/            # CLI commands
│   ├── api/            # REST API
│   ├── mcp/            # MCP server
│   └── adk_agents/     # ADK implementations
├── infrastructure/     # Technical details
│   └── template_generator/  # XML generation
└── tests/              # Mirror src structure
    ├── unit/           # Unit tests (write first!)
    ├── integration/    # Integration tests
    └── fixtures/       # Test data
```

## 📋 Implementation Priority (from STATE_TRACKER.md)

Follow this order, using TDD for each:

1. **DocumentAnalysisAgent** - Complete the markdown parsing
2. **XMLGenerator** - Use provided template structure
3. **Wire up agents** - Connect implementations
4. **Basic integration tests** - End-to-end PRD→Template
5. **Codebase scanner** - AST-based analysis
6. **Sequence planner** - Dependency resolution
7. **API enhancements** - Auth, rate limiting
8. **MCP server** - Collaborative features

## ⚡ Quick Start for New Features

1. **Read STATE_TRACKER.md** for next priority item
2. **Write failing test** in `tests/unit/test_<feature>.py`
3. **Run test** - verify it fails (RED)
4. **Implement feature** with minimal code
5. **Run test** - verify it passes (GREEN)
6. **Run quality checks** - fix any issues
7. **Refactor** if needed (tests still GREEN)
8. **Update STATE_TRACKER.md** with progress
9. **Commit** with descriptive message

## 🚫 Common Pitfalls to Avoid

- ❌ Writing code before tests
- ❌ Skipping code quality checks
- ❌ Using pip instead of uv
- ❌ Large commits (commit after each GREEN test)
- ❌ Implementing beyond test requirements
- ❌ Ignoring mypy/ruff warnings

## 📝 Commit Message Format

```
<type>: <description>

<body>

<footer>
```

Types: feat, fix, test, refactor, docs, chore

Example:
```
test: Add unit tests for DocumentAnalysisAgent markdown parsing

- Test parsing of PRD title and version
- Test feature extraction with dependencies
- Test error handling for invalid files
```

## 🔧 VS Code Settings (Recommended)

```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

## 📚 Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Testing Guide](https://google.github.io/adk-docs/get-started/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [TDD Best Practices](https://testdriven.io/blog/modern-tdd/)

## Current State

Version 0.1.0 - Early development phase. Using TDD to systematically implement features from STATE_TRACKER.md.