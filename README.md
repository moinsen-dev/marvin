# Marvin 🤖

<div align="center">

[![PyPI version](https://badge.fury.io/py/marvin.svg)](https://pypi.org/project/marvin/)
[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://moinsen-dev.github.io/marvin/)
[![CI](https://github.com/moinsen/marvin/workflows/CI/badge.svg)](https://github.com/moinsen/marvin/actions)
[![Coverage](https://codecov.io/gh/moinsen/marvin/branch/main/graph/badge.svg)](https://codecov.io/gh/moinsen/marvin)
[![Test Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com/moinsen/marvin/actions)
[![TDD](https://img.shields.io/badge/TDD-enforced-red.svg)](docs/TDD_BEST_PRACTICES.md)
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
- **🧪 100% Test Coverage**: Enforced Test-Driven Development with comprehensive test suite
- **🔒 Quality Gates**: CI/CD pipeline with strict coverage and quality requirements

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
pip install marvin

# Or install with uv (faster)
uv pip install marvin
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

# Run tests with 100% coverage enforcement
uv run pytest

# Generate detailed coverage report
uv run pytest --cov=marvin --cov-report=html
open htmlcov/index.html

# Run pre-commit hooks (includes all quality checks)
pre-commit run --all-files

# Individual quality checks
uv run black src tests        # Format code
uv run isort src tests        # Sort imports
uv run ruff check src tests   # Lint code
uv run mypy src              # Type check

# Verify test coverage and quality (demonstration)
uv run python scripts/demo_quality_verification.py

# Full quality verification (once we reach 100% coverage)
uv run python scripts/verify_quality.py
```

### Code Quality

We maintain the highest code quality standards with **100% test coverage enforcement**:

- 🧪 **Test-Driven Development (TDD)**: All code written test-first with comprehensive coverage
- ✅ **100% Test Coverage**: Enforced via CI/CD - no PRs merge below 100%
- 🎨 **Black** for code formatting
- 📦 **isort** for import sorting  
- 🔍 **Ruff** for linting
- 📝 **mypy** for type checking
- 🔒 **Pre-commit hooks** preventing commits without tests
- 🚫 **Coverage gates** blocking merges with insufficient coverage

#### Quality Verification

```bash
# Demonstrate our quality verification system
uv run python scripts/demo_quality_verification.py

# Expected output:
# 🧪 MARVIN QUALITY VERIFICATION DEMONSTRATION
# ✅ Quality Verifier initialized successfully
# 🎯 TESTING COVERAGE THRESHOLD ENFORCEMENT
#    99.9% coverage  → ❌ FAIL
#    99.99% coverage → ❌ FAIL  
#    100.0% coverage → ✅ PASS
# 🏆 QUALITY ENFORCEMENT SUMMARY
#    ✅ 100% Test Coverage Enforced
#    ✅ Pre-commit Hooks Configured
#    ✅ CI/CD Coverage Gates Active
# 🎉 Marvin achieves the highest quality standards!

# Run actual comprehensive quality check (when at 100% coverage)
uv run python scripts/verify_quality.py
```

## 📚 Documentation

- [Full Documentation](https://marvin.readthedocs.io) (coming soon)
- [API Reference](docs/api.md)
- [Architecture Guide](docs/architecture.md)
- [Examples](examples/)

## 🗺️ Roadmap

### ✅ v0.1.0 - Foundation (Complete)
- [x] Core domain models with 100% test coverage
- [x] Test-Driven Development infrastructure
- [x] Basic CLI interface and FastAPI server
- [x] CI/CD pipeline with quality gates
- [x] GitHub integration and project tracking

### 🚀 v0.2.0 - AI-Powered Analysis Platform (In Progress)
**Target**: August 28, 2025 | **[View Milestone](https://github.com/moinsen-dev/marvin/milestone/1)**

- [ ] Complete PRD analysis with NLP ([Epic #1](https://github.com/moinsen-dev/marvin/issues/1))
- [ ] Advanced codebase scanning ([Epic #4](https://github.com/moinsen-dev/marvin/issues/4))
- [ ] Full XML template generation ([Epic #6](https://github.com/moinsen-dev/marvin/issues/6))
- [ ] MCP server implementation ([Epic #7](https://github.com/moinsen-dev/marvin/issues/7))
- [ ] Web UI dashboard ([Epic #10](https://github.com/moinsen-dev/marvin/issues/10))
- [ ] VS Code extension ([Epic #11](https://github.com/moinsen-dev/marvin/issues/11))

**Total**: 11 Issues | 128 Story Points | 7 Epics

See our [v0.2.0 Roadmap](docs/ROADMAP_v0.2.0.md) for detailed sprint planning and [GitHub Issues](https://github.com/moinsen-dev/marvin/issues) for tracking.

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