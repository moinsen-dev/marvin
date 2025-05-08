# Marvin - Installation Guide

This guide describes how to install Marvin locally and start development.

## Prerequisites

- Python 3.11 or higher
- uv (for dependency management)
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/marvin.git
cd marvin
```

### 2. Set up virtual environment with uv

```bash
# Install uv (if not already installed)
pip install uv

# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -e .

# For development dependencies
uv pip install -r requirements-dev.txt
```

### 3. Verify installation

```bash
# Check if Marvin is correctly installed
marvin --version
```

## Usage

Marvin can be used in three different ways:

### 1. As CLI tool

```bash
# Show help
marvin --help

# Analyze a PRD and generate AI-Coding-Tasks
marvin analyze path/to/prd.md --output ./output-dir

# With codebase analysis
marvin analyze path/to/prd.md --codebase path/to/codebase --output ./output-dir
```

### 2. As API server

```bash
# Start API server
marvin serve-api

# With custom host and port
marvin serve-api --host 0.0.0.0 --port 8080
```

The API is then accessible at `http://localhost:8000` (or the specified host/port).

### 3. As MCP server

```bash
# Start MCP server
marvin serve-mcp

# With custom host and port
marvin serve-mcp --host 0.0.0.0 --port 9090
```

## Development

### Running tests

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=marvin

# Unit tests only
pytest tests/unit
```

### Formatting code

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests
```

### Linting

```bash
# Check code with Ruff
ruff check src tests
```

## Configuration

Marvin can be configured via environment variables:

- `MARVIN_API_HOST` - Host for the API server
- `MARVIN_API_PORT` - Port for the API server
- `MARVIN_MCP_HOST` - Host for the MCP server
- `MARVIN_MCP_PORT` - Port for the MCP server
- `MARVIN_CONTEXT7_API_KEY` - API key for Context 7
- `MARVIN_LOG_LEVEL` - Log level (INFO, DEBUG, WARNING, ERROR)
- `MARVIN_ENVIRONMENT` - Environment (development, production)

Example:

```bash
export MARVIN_LOG_LEVEL=DEBUG
export MARVIN_ENVIRONMENT=development
marvin analyze path/to/prd.md
```

## Using the example PRD

You can find an example PRD in the `examples` directory:

```bash
marvin analyze examples/prd/example_prd.md
```

## Troubleshooting

If you encounter problems, check the following:

1. Is Python 3.11 or higher installed? `python --version`
2. Is uv installed? `uv --version`
3. Is the virtual environment activated? `which python` should point to your virtual environment
4. Are all dependencies installed? `uv pip freeze`

## Why uv?

We use uv instead of other package managers because:

1. **Speed**: uv is significantly faster than pip and Poetry
2. **Compatibility**: uv works with standard requirements.txt files and pyproject.toml
3. **Reliability**: uv has improved dependency resolution
4. **Feature-rich**: uv includes virtual environment management and more

## Next Steps

- Implement your own agent
- Add new features
- Improve documentation
- Contribute to project development
