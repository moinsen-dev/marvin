# Contributing to Marvin

Thank you for your interest in contributing to Marvin! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Versioning Guidelines](#versioning-guidelines)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please be respectful and professional in all interactions.

## Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- Git

### Setting Up Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/marvin.git
cd marvin

# Create a virtual environment with uv
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
uv pip install -e ".[dev]"

# Run tests to ensure everything is working
uv run pytest
```

### Development Tools

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Linting
- **MyPy**: Type checking
- **pytest**: Testing

Run all checks with:
```bash
./check_code.sh
```

## Development Workflow

### 1. Create a Branch

```bash
# Update develop branch
git checkout develop
git pull origin develop

# Create feature branch
git checkout -b feature/your-feature-name

# Or for bugs
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write your code following our [coding standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed
- Update CHANGELOG.md (see [changelog guidelines](#changelog-guidelines))

### 3. Test Your Changes

```bash
# Run tests
uv run pytest

# Run specific tests
uv run pytest tests/unit/test_specific.py -v

# Run with coverage
uv run pytest --cov=marvin --cov-report=term-missing
```

### 4. Check Code Quality

```bash
# Run all checks
./check_code.sh

# Or run individually
uv run black src tests
uv run isort src tests
uv run ruff check src tests
uv run mypy src
```

### 5. Commit Your Changes

Follow our [commit message guidelines](#commit-message-guidelines):

```bash
git add .
git commit -m "feat: add new PRD parsing feature"
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks
- **ci**: CI/CD changes

### Examples

```bash
# Feature
feat(parser): add support for YAML PRD format

# Bug fix
fix(cli): resolve path issue on Windows

# Documentation
docs(api): update API endpoint documentation

# Breaking change
feat(api)!: change response format for /analyze endpoint

BREAKING CHANGE: The API now returns a different JSON structure
```

## Versioning Guidelines

We use [Semantic Versioning](https://semver.org/):

### Version Format

`MAJOR.MINOR.PATCH[-PRERELEASE]`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)
- **PRERELEASE**: alpha, beta, rc

### When to Update Version

Versions are updated as part of the release process. Contributors should NOT update version numbers in their PRs.

### Changelog Guidelines

Every PR that changes functionality should update `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- Your new feature here

### Changed
- Your changes here

### Fixed
- Your bug fixes here
```

Categories:
- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Features to be removed
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security fixes

## Pull Request Process

### 1. Before Submitting

- [ ] All tests pass
- [ ] Code quality checks pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages follow guidelines

### 2. Creating the PR

1. Push your branch to your fork
2. Create a PR against the `develop` branch
3. Fill out the PR template completely
4. Link any related issues

### 3. PR Review Process

- At least one maintainer must review
- All CI checks must pass
- Address review feedback promptly
- Keep PR focused on a single change

### 4. After Merge

Your changes will be included in the next release!

## Coding Standards

### Python Style

We follow PEP 8 with these tools:
- **Black** for formatting (line length: 88)
- **isort** for import sorting
- **Ruff** for linting

### Type Hints

All new code should include type hints:

```python
from typing import List, Optional

def process_prd(file_path: str, options: Optional[dict] = None) -> List[Task]:
    """Process a PRD file and return tasks."""
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_complexity(features: List[Feature]) -> int:
    """Calculate the complexity score for features.
    
    Args:
        features: List of Feature objects to analyze
        
    Returns:
        Complexity score as an integer
        
    Raises:
        ValueError: If features list is empty
    """
    ...
```

### Error Handling

Always provide helpful error messages:

```python
if not file_path.exists():
    raise FileNotFoundError(
        f"PRD file not found: {file_path}\n"
        f"Please check the file path and try again."
    )
```

## Testing Guidelines

### Test Structure

```python
# tests/unit/test_feature.py
import pytest
from marvin.feature import MyFeature

class TestMyFeature:
    """Test cases for MyFeature."""
    
    def test_basic_functionality(self):
        """Test that basic functionality works."""
        result = MyFeature().process("input")
        assert result == "expected"
    
    def test_error_handling(self):
        """Test that errors are handled properly."""
        with pytest.raises(ValueError):
            MyFeature().process(None)
```

### Test Coverage

- Aim for 80%+ coverage
- Test both success and failure cases
- Include edge cases
- Mock external dependencies

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=marvin

# Run specific test file
uv run pytest tests/unit/test_specific.py -v
```

## Documentation

### Code Documentation

- All public functions need docstrings
- Complex logic should have inline comments
- Update README.md for user-facing changes

### Documentation Site

Our documentation uses MkDocs:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Serve locally
mkdocs serve

# Build docs
mkdocs build
```

### API Documentation

API endpoints should be documented with:
- Request/response examples
- Error codes
- Authentication requirements

## Getting Help

- 💬 [Discord Community](https://discord.gg/marvin)
- 🐛 [GitHub Issues](https://github.com/moinsen-dev/marvin/issues)
- 📖 [Documentation](https://moinsen-dev.github.io/marvin/)

## Recognition

Contributors are recognized in:
- Release notes
- CONTRIBUTORS.md file
- GitHub contributors page

Thank you for contributing to Marvin! 🎉