# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Marvin is an intelligent tool that analyzes Product Requirement Documents (PRDs) and converts them into structured AI-Coding-Tasks. It generates XML-based task templates for AI coding assistants (Cursor, Windsurf, Claude Code).

## Development Commands

### Testing
```bash
pytest                    # Run all tests
pytest --cov=marvin      # Run with coverage report
pytest tests/unit        # Run unit tests only
```

### Code Quality
```bash
black src tests          # Format code with Black
isort src tests          # Sort imports with isort
ruff check src tests     # Check code with Ruff
```

### Running Marvin
```bash
marvin process <prd_file> [--codebase <path>] [--output <dir>]  # Process a PRD
marvin server [--host 0.0.0.0] [--port 8000]                    # Start API server
```

## Architecture

The project follows Hexagonal Architecture (Ports & Adapters):

- **core/**: Domain logic - models, use cases, and business rules
- **adapters/**: External interfaces - CLI, API, MCP server, ADK agents
- **infrastructure/**: Technical implementations - XML generation, utilities
- **agents/**: AI-powered components for analysis and generation

Key domain models: `Feature`, `PRD`, `Codebase`, `Task`, `Workflow`

## Development Guidelines

1. **Python Version**: Requires Python 3.11+
2. **Dependency Management**: Uses `uv` (not pip/Poetry)
3. **Code Standards**:
   - Black formatting (88 char line length)
   - Ruff for linting
   - Type hints required
   - Loguru for logging

4. **Testing**:
   - Write tests for all new functionality
   - Coverage target: 90%
   - Test structure mirrors source structure
   - Use pytest-asyncio for async tests

5. **Agent Development** (when using Google ADK):
   - Follow ADK framework patterns
   - Implement proper error handling and logging
   - Use shared session state for agent communication
   - Test agents using ADK's evaluation tools

## Current State

Version 0.1.0 - Early development phase focusing on core functionality. The project is transitioning to integrate Google's Agent Development Kit (ADK) for enhanced agent capabilities.