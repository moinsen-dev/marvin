# Marvin 🤖

<div align="center">

[![PyPI version](https://badge.fury.io/py/marvin-prd.svg)](https://pypi.org/project/marvin-prd/)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://moinsen-dev.github.io/marvin/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat)](http://makeapullrequest.com)

*"Life? Don't talk to me about life."* - Marvin, the Paranoid Android

An intelligent tool for converting Product Requirements Documents (PRDs) into structured AI-Coding-Tasks

</div>

## 🌟 Overview

Marvin is an intelligent tool that analyzes Product Requirement Documents (PRDs) and converts them into structured AI-Coding-Tasks. Named after the depressive robot from "The Hitchhiker's Guide to the Galaxy," Marvin helps developers organize their projects more efficiently and make optimal use of AI coding assistants (like Cursor, Windsurf, or Claude Code).

## ✨ Features

- **📄 PRD Analysis**: Intelligent extraction of features and requirements from product documents
- **🔍 Codebase Scanning**: Deep analysis of existing codebases for seamless feature integration
- **📝 Template Generation**: Creation of structured AI-Coding-Task templates in XML format
- **📊 Sequence Planning**: Automatic division of requirements into logical, sequential tasks
- **🤖 AI-Powered**: Leverages Google ADK and advanced LLMs for intelligent analysis

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Using pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Basic Usage

```bash
# Process a PRD document
marvin process path/to/prd.md --output ./output

# Process with existing codebase context
marvin process path/to/prd.md --codebase ./my-project --output ./output

# Start API server
marvin server --host 0.0.0.0 --port 8000

# Get help
marvin --help
```

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- uv (recommended) or pip
- Git

### From PyPI (Recommended)

```bash
# Install with pip
pip install marvin-prd

# Or install with uv (faster)
uv pip install marvin-prd
```

### From Source

```bash
# Clone the repository
git clone https://github.com/moinsen-dev/marvin.git
cd marvin

# Install with uv (recommended)
uv venv
source .venv/bin/activate
uv pip install -e .

# For development
uv pip install -e ".[dev]"
```

### Configuration

Marvin uses environment variables for configuration:

```bash
# Create .env file
cp .env.example .env

# Configure your settings
GOOGLE_API_KEY=your_api_key_here
MARVIN_LOG_LEVEL=INFO
MARVIN_OUTPUT_DIR=./marvin-output
```

## 🛠️ Usage

### CLI Interface

Marvin provides a powerful command-line interface:

```bash
# Process a PRD
marvin process <prd_file> [options]

Options:
  --codebase, -c PATH    Path to existing codebase
  --output, -o PATH      Output directory for templates
  --format, -f FORMAT    Output format (xml, json, yaml)
  --verbose, -v          Enable verbose logging
```

### API Interface

Start the REST API server:

```bash
marvin server [--host HOST] [--port PORT]
```

API endpoints:
- `POST /process` - Process a PRD file
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)

### Python SDK

```python
from marvin import Marvin

# Initialize Marvin
marvin = Marvin()

# Process a PRD
result = await marvin.process_prd(
    prd_path="path/to/prd.md",
    codebase_path="path/to/project"
)

# Access results
for task in result.tasks:
    print(f"Task: {task.name}")
    print(f"Dependencies: {task.dependencies}")
```

## 🏗️ Architecture

Marvin follows a Hexagonal Architecture (Ports & Adapters) pattern:

```
marvin/
├── core/               # Business logic and domain models
│   ├── domain/         # Domain entities (PRD, Feature, Task, etc.)
│   ├── use_cases/      # Application business rules
│   └── agents/         # AI-powered analysis agents
├── adapters/           # External interfaces
│   ├── cli/            # Command-line interface
│   ├── api/            # REST API server
│   ├── mcp/            # MCP server (coming soon)
│   └── adk_agents/     # Google ADK agent implementations
└── infrastructure/     # Technical implementations
    └── template_generator/  # XML generation logic
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install
git clone https://github.com/moinsen/marvin.git
cd marvin
uv pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=marvin

# Format code
black src tests
isort src tests

# Lint code
ruff check src tests

# Type check
mypy src
```

### Code Quality

We maintain high code quality standards:
- 🎨 **Black** for code formatting
- 📦 **isort** for import sorting
- 🔍 **Ruff** for linting
- 📝 **mypy** for type checking
- ✅ **pytest** for testing (90% coverage target)

## 📚 Documentation

- [Full Documentation](https://marvin.readthedocs.io) (coming soon)
- [API Reference](docs/api.md)
- [Architecture Guide](docs/architecture.md)
- [Examples](examples/)

## 🗺️ Roadmap

- [x] Core domain models
- [x] Basic CLI interface
- [x] FastAPI server
- [ ] Complete PRD analysis with NLP
- [ ] Advanced codebase scanning
- [ ] Full XML template generation
- [ ] MCP server implementation
- [ ] Web UI dashboard
- [ ] VS Code extension

See our [Project Roadmap](docs/ROADMAP.md) for detailed plans.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Named after Marvin from Douglas Adams' "The Hitchhiker's Guide to the Galaxy"
- Built with [Google ADK](https://github.com/google/adk) for agent capabilities
- Inspired by the need for better AI coding assistant integration

## 💬 Support

- 📧 Email: support@marvin-ai.dev
- 💬 Discord: [Join our community](https://discord.gg/marvin)
- 🐛 Issues: [GitHub Issues](https://github.com/moinsen/marvin/issues)

---

<div align="center">

**Don't Panic!** 🚀

*Even though Marvin might be depressive at times, he's always here to help.*

</div>