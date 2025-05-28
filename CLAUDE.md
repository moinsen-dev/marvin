# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨🚨🚨 CRITICAL REMINDER - READ THIS FIRST! 🚨🚨🚨

**ALWAYS USE `uv` FOR ALL PYTHON OPERATIONS - NEVER USE `python` OR `pip` DIRECTLY!**

- ✅ `uv run python script.py` - NOT `python script.py`
- ✅ `uv pip install package` - NOT `pip install package`  
- ✅ `uv run pytest` - NOT `pytest`
- ✅ `uv run black src` - NOT `black src`
- ✅ `uv run python -m build` - NOT `python -m build`

**THIS IS NON-NEGOTIABLE - UV IS OUR PACKAGE MANAGER!**

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

## 🚨🚨🚨 CRITICAL: ALWAYS USE UV - NEVER USE PYTHON OR PIP DIRECTLY! 🚨🚨🚨

**THIS IS ABSOLUTELY CRITICAL - FAILURE TO USE UV WILL CAUSE ISSUES!**

### ⚠️ NEVER DO THIS:
```bash
# ❌ WRONG - DO NOT USE:
python script.py          # ❌ NO!
pip install package       # ❌ NO!
python -m build          # ❌ NO!
pytest                   # ❌ NO!
black src                # ❌ NO!
```

### ✅ ALWAYS DO THIS:
```bash
# ✅ CORRECT - ALWAYS USE UV:
uv run python script.py   # ✅ YES!
uv pip install package    # ✅ YES!
uv run python -m build    # ✅ YES!
uv run pytest            # ✅ YES!
uv run black src         # ✅ YES!
```

## 📦 What is UV?

**UV is an extremely fast Python package and project manager, written in Rust by Astral.**

- **10-100x faster** than pip
- **All-in-one solution**: Replaces pip, pip-tools, pipx, poetry, pyenv, virtualenv
- **Automatic virtual environment management**
- **Built-in Python version management**
- **Smart caching and parallelization**
- **Drop-in replacement** for pip commands

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
uv run ruff check src tests --fix --unsafe-fixes  # For remaining issues

# Type checking (ALWAYS run after changes)
uv run mypy src

# All checks in one command
uv run black src tests && uv run isort src tests && uv run ruff check src tests --fix && uv run mypy src

# Full code quality workflow (comprehensive fix)
uv run ruff check src tests --fix && \
uv run ruff check src tests --fix --unsafe-fixes && \
uv run mypy src && \
uv run black src tests && \
uv run isort src tests
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

## 🐙 GitHub Integration & Tracking

**MANDATORY**: Use GitHub for ALL project tracking, collaboration, and deployment.

### 📊 Issue Tracking

**Every task MUST have a corresponding GitHub issue:**

```bash
# Create issue via GitHub CLI
gh issue create --title "Implement feature X" --body "Description..." --label "enhancement"

# List open issues
gh issue list --assignee @me

# View issue details
gh issue view <number>

# Close issue with comment
gh issue close <number> --comment "Completed in PR #123"
```

**Issue Templates:**
- Bug Report: Use for defects and errors
- Feature Request: Use for new functionality
- Task: Use for implementation work
- Documentation: Use for docs updates

### 🔄 Pull Request Workflow

**ALL changes MUST go through PR review:**

```bash
# Create feature branch
git checkout -b feature/<issue-number>-<short-description>

# Make changes following TDD workflow
# ... implement with tests ...

# Push branch
git push -u origin feature/<issue-number>-<short-description>

# Create PR linked to issue
gh pr create --title "feat: <description>" --body "Closes #<issue-number>" --draft

# After reviews, merge
gh pr merge <number> --squash --delete-branch
```

**PR Requirements:**
- ✅ All tests passing
- ✅ Code quality checks passed
- ✅ Linked to GitHub issue
- ✅ Descriptive title and body
- ✅ At least one approval
- ✅ No merge conflicts

### 🌿 Branch Strategy

```
main
├── develop (default branch)
│   ├── feature/<issue>-<description>
│   ├── fix/<issue>-<description>
│   └── docs/<issue>-<description>
├── release/v<version>
└── hotfix/<issue>-<description>
```

**Branch Rules:**
- `main`: Production-ready code only
- `develop`: Integration branch for features
- `feature/*`: New functionality (from develop)
- `fix/*`: Bug fixes (from develop)
- `release/*`: Release preparation (from develop)
- `hotfix/*`: Emergency fixes (from main)

### 🏷️ Release Management

```bash
# Create release branch
git checkout -b release/v0.2.0 develop

# Update version
uv run python scripts/bump_version.py --version 0.2.0

# Create GitHub release
gh release create v0.2.0 --title "Release v0.2.0" --notes-file CHANGELOG.md --target release/v0.2.0

# Tag and merge to main
git tag -a v0.2.0 -m "Release version 0.2.0"
git checkout main
git merge --no-ff release/v0.2.0
git push origin main --tags
```

### 📋 Project Board Integration

**Use GitHub Projects for sprint planning:**

```bash
# Add issue to project
gh issue edit <number> --add-project "<project-name>"

# Move issue between columns
gh api graphql -f query='mutation ...'

# View project status
gh project list
```

**Project Columns:**
- 📥 Backlog: All unplanned work
- 📋 To Do: Sprint planned work
- 🚧 In Progress: Active development
- 👀 In Review: PR submitted
- ✅ Done: Merged to develop

### 🤖 GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop, main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run pytest --cov
      - run: uv run black src tests --check
      - run: uv run isort src tests --check
      - run: uv run ruff check src tests
      - run: uv run mypy src
```

### 🔍 Code Review Guidelines

**Reviewer Checklist:**
- [ ] Tests cover new functionality
- [ ] No decrease in code coverage
- [ ] Follows project conventions
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered

**Review Commands:**
```bash
# Checkout PR locally
gh pr checkout <number>

# Add review comment
gh pr review <number> --comment --body "Looks good!"

# Approve PR
gh pr review <number> --approve

# Request changes
gh pr review <number> --request-changes --body "Please fix..."
```

### 📈 GitHub Insights & Metrics

**Track project health:**
```bash
# View repository insights
gh api repos/:owner/:repo/stats/contributors

# Check workflow runs
gh run list --workflow=ci.yml

# View deployment status
gh api repos/:owner/:repo/deployments
```

### 🔐 Security & Dependabot

**Enable security features:**
- Dependabot alerts for vulnerabilities
- Dependabot updates for dependencies
- Code scanning with CodeQL
- Secret scanning

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "dependencies"
      - "python"
```

### 📝 GitHub Integration Best Practices

1. **Link Everything**: Every commit references an issue
2. **Automate Workflows**: Use GitHub Actions extensively
3. **Document Decisions**: Use issue/PR discussions
4. **Track Progress**: Update issues with progress comments
5. **Review Thoroughly**: Never merge without review
6. **Tag Releases**: Use semantic versioning
7. **Monitor Health**: Check Actions, coverage, dependencies

### 🚀 Quick GitHub Commands

```bash
# Clone with GitHub CLI
gh repo clone <owner>/<repo>

# Fork repository
gh repo fork <owner>/<repo> --clone

# View repo in browser
gh repo view --web

# Check CI status
gh run list --limit 5

# View PR diff
gh pr diff <number>

# List milestones
gh api repos/:owner/:repo/milestones

# Create discussion
gh api repos/:owner/:repo/discussions -f title="RFC: ..." -f body="..."
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

## 🎯 Code Quality Status

**✅ ZERO VALIDATION ERRORS ACHIEVED!**

Last validated: Current session
- **Ruff**: 292 → 0 errors (all linting issues resolved)
- **MyPy**: 5 → 0 errors (all type checking issues resolved)  
- **Black**: All formatting issues resolved
- **isort**: All import sorting issues resolved
- **Pylance**: 15 → 9 diagnostics (only expected Google ADK import warnings remain)

### Code Quality Validation Workflow

When fixing validation errors systematically:

```bash
# 1. Initial assessment
uv run ruff check src tests              # Identify all linting issues
uv run mypy src                          # Identify type checking issues

# 2. Auto-fix with Ruff (most effective first)
uv run ruff check src tests --fix        # Fix standard issues
uv run ruff check src tests --fix --unsafe-fixes  # Fix remaining issues

# 3. Manual fixes for remaining issues
# - Update deprecated type hints (typing.Dict → dict, typing.List → list)
# - Fix unused imports and variables (prefix with _ if intentionally unused)
# - Add missing type annotations
# - Fix async/await syntax issues

# 4. Type checking
uv run mypy src                          # Fix any remaining type issues

# 5. Formatting (final cleanup)
uv run black src tests                   # Format code
uv run isort src tests                   # Sort imports

# 6. Final validation
uv run ruff check src tests              # Should show 0 errors
uv run mypy src                          # Should show 0 errors
uv run pytest                           # Should pass all tests
```

### IDE Integration

For VS Code/Pylance diagnostics:
- Use `mcp__ide__getDiagnostics` tool to identify IDE-specific issues
- Import warnings for missing libraries (like Google ADK) are expected
- Unused parameter warnings can be resolved by prefixing with underscore

## Current State

Version 0.1.0 - Early development phase. 

**Recent Achievements:**
- ✅ Implemented DocumentAnalysisAgent with TDD approach
- ✅ Implemented XMLTemplateGenerator with proper template structure  
- ✅ Created Google ADK agents (MarvinOrchestratorADKAgent, SequencePlannerADKAgent)
- ✅ **ACHIEVED ZERO PYTHON VALIDATION ERRORS** - Complete code quality cleanup
- ✅ All tests passing (20/20 ADK agent tests)

**Next:** Continue implementing features from STATE_TRACKER.md using TDD approach.