# Installation

This guide will help you install Marvin and get started with converting PRDs to AI-ready coding tasks.

## Prerequisites

Before installing Marvin, ensure you have the following:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **uv** - Fast Python package manager - [Install uv](https://docs.astral.sh/uv/getting-started/installation/)
- **Git** - Version control system - [Download Git](https://git-scm.com/downloads)

!!! tip "Why uv?"
    We use uv for package management because it's:
    
    - **⚡ Lightning fast** - 10-100x faster than pip
    - **🔒 Reliable** - Better dependency resolution
    - **📦 Feature-rich** - Built-in virtual environment management
    - **🔧 Compatible** - Works with standard requirements.txt and pyproject.toml

## Installation Methods

=== "From Source (Recommended)"

    ### 1. Clone the Repository
    
    ```bash
    git clone https://github.com/moinsen-dev/marvin.git
    cd marvin
    ```
    
    ### 2. Set Up Virtual Environment
    
    ```bash
    # Create virtual environment
    uv venv
    
    # Activate virtual environment
    # On macOS/Linux:
    source .venv/bin/activate
    
    # On Windows:
    .venv\Scripts\activate
    ```
    
    ### 3. Install Dependencies
    
    ```bash
    # Install Marvin in development mode
    uv pip install -e .
    
    # For development (includes testing and linting tools)
    uv pip install -e ".[dev]"
    
    # For documentation building
    uv pip install -e ".[docs]"
    ```
    
    ### 4. Verify Installation
    
    ```bash
    # Check Marvin version
    marvin --version
    
    # Show available commands
    marvin --help
    ```

=== "From PyPI (Coming Soon)"

    ```bash
    # This will be available once we publish to PyPI
    uv pip install marvin-prd
    ```

=== "Using Docker (Coming Soon)"

    ```bash
    # Pull the Docker image
    docker pull marvin/marvin:latest
    
    # Run Marvin in a container
    docker run -v $(pwd):/workspace marvin/marvin process /workspace/my-prd.md
    ```

## Quick Verification

After installation, verify everything is working:

```bash
# Process the example PRD
marvin process examples/prd/example_prd.md --output ./test-output/

# Check the generated files
ls -la ./test-output/
```

You should see generated XML template files in the output directory.

## Environment Configuration

Marvin can be configured using environment variables:

```bash
# Set log level for debugging
export MARVIN_LOG_LEVEL=DEBUG

# Configure API server settings
export MARVIN_API_HOST=0.0.0.0
export MARVIN_API_PORT=8000

# Set environment
export MARVIN_ENVIRONMENT=development
```

!!! tip "Configuration File"
    You can also create a `.env` file in your project root:
    
    ```ini
    MARVIN_LOG_LEVEL=INFO
    MARVIN_ENVIRONMENT=development
    MARVIN_API_HOST=localhost
    MARVIN_API_PORT=8000
    ```

## Platform-Specific Notes

### macOS

If you're using Homebrew, you can install Python and uv:

```bash
# Install Python
brew install python@3.11

# Install uv
brew install uv
```

### Windows

On Windows, you might need to:

1. Enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
2. Add Python to PATH during installation
3. Use PowerShell or Windows Terminal for better experience

### Linux

Most Linux distributions come with Python. Install uv using:

```bash
# Using pip
pip install --user uv

# Or using pipx (recommended)
pipx install uv
```

## Troubleshooting

### Common Issues

??? question "Python version error"
    **Error**: `Python 3.11 or higher is required`
    
    **Solution**: 
    ```bash
    # Check your Python version
    python --version
    
    # If needed, install Python 3.11+
    # macOS: brew install python@3.11
    # Ubuntu: sudo apt install python3.11
    # Windows: Download from python.org
    ```

??? question "uv not found"
    **Error**: `command not found: uv`
    
    **Solution**:
    ```bash
    # Install uv
    pip install --user uv
    
    # Add to PATH if needed
    export PATH="$HOME/.local/bin:$PATH"
    ```

??? question "Import errors"
    **Error**: `ModuleNotFoundError: No module named 'marvin'`
    
    **Solution**:
    ```bash
    # Ensure you're in the virtual environment
    which python  # Should show .venv/bin/python
    
    # Reinstall in development mode
    uv pip install -e .
    ```

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/moinsen-dev/marvin/issues)
2. Join our [Discord Community](https://discord.gg/marvin)
3. Review the [Developer Guide](../developer-guide/setup.md)

## Next Steps

Now that you have Marvin installed:

- 📚 Follow the [Quick Start Guide](quickstart.md) to process your first PRD
- 🔧 Learn about [Configuration Options](configuration.md)
- 🚀 Explore [CLI Usage](../user-guide/cli-usage.md)
- 🔌 Set up the [API Server](../user-guide/api-usage.md)