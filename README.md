# Marvin

> "Life? Don't talk to me about life." - Marvin, the Paranoid Android

## Overview

Marvin is an intelligent tool that analyzes Product Requirement Documents (PRDs) and converts them into structured AI-Coding-Tasks. Named after the depressive robot from "The Hitchhiker's Guide to the Galaxy," Marvin helps developers organize their projects more efficiently and make optimal use of AI coding assistants (like Cursor, Windsurf, or Claude Code).

## Features

- **PRD Analysis**: Extraction of features and requirements from product requirement documents
- **Codebase Scanning**: Analysis of existing codebases for new feature integration
- **Template Generation**: Creation of structured AI-Coding-Task templates in XML format
- **Sequence Planning**: Automatic division of requirements into logical, sequential tasks

## Interfaces

Marvin offers three different access methods:

1. **CLI Tool**: For developers who want to use Marvin directly in their local environment
2. **API**: For integration into CI/CD pipelines and other tools
3. **MCP Server**: For collaborative development environments and complex use cases

## Technology

- Python 3.11+
- FastAPI
- Google ADK (Agent Development Kit)
- Context 7 for code analysis
- Agent-based architecture

## Installation

```bash
# With uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# For development
uv pip install -r requirements-dev.txt

# With pip
pip install -e .
```

## Quick Start

```bash
# As CLI tool
marvin analyze --prd path/to/prd.md --output path/to/output

# Start as API server
marvin serve-api

# Start as MCP server
marvin serve-mcp
```

## Project Structure

```
/marvin
  /src
    /core          # Domain logic
    /adapters      # Interfaces (CLI, API, MCP)
    /infrastructure # Technical implementations
  /tests
  /docs
  /examples
```

## License

MIT

## Note

*Don't Panic!* - Even though Marvin might be depressive at times, he's always here to help.
