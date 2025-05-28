# 🧪 Test Implementation Guide

## Overview
This guide provides concrete examples for implementing tests for modules with zero coverage.

## 1. Testing `config.py` (0% → 100%)

### Test Structure
```python
# tests/unit/test_config.py
import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
from pathlib import Path

from marvin.config import (
    Config, MarvinConfig, DatabaseConfig, ServerConfig,
    LoggingConfig, get_config, load_from_env, load_from_file
)

class TestConfig:
    """Test Config dataclass and its components."""
    
    def test_database_config_defaults(self):
        """Test DatabaseConfig default values."""
        db_config = DatabaseConfig()
        assert db_config.url == "sqlite:///marvin.db"
        assert db_config.echo is False
        assert db_config.pool_size == 5
        assert db_config.max_overflow == 10
    
    def test_server_config_custom_values(self):
        """Test ServerConfig with custom values."""
        server_config = ServerConfig(host="0.0.0.0", port=8080)
        assert server_config.host == "0.0.0.0"
        assert server_config.port == 8080
        assert server_config.workers == 1  # default
    
    def test_logging_config_validation(self):
        """Test LoggingConfig level validation."""
        log_config = LoggingConfig(level="DEBUG", format="json")
        assert log_config.level == "DEBUG"
        assert log_config.format == "json"
        
        # Test invalid level
        with pytest.raises(ValueError):
            LoggingConfig(level="INVALID")

class TestConfigLoading:
    """Test configuration loading functions."""
    
    @patch.dict(os.environ, {
        'MARVIN_HOST': '127.0.0.1',
        'MARVIN_PORT': '9000',
        'MARVIN_LOG_LEVEL': 'DEBUG',
        'MARVIN_DB_URL': 'postgresql://localhost/marvin'
    })
    def test_load_from_env(self):
        """Test loading configuration from environment variables."""
        config = load_from_env()
        assert config.server.host == '127.0.0.1'
        assert config.server.port == 9000
        assert config.logging.level == 'DEBUG'
        assert config.database.url == 'postgresql://localhost/marvin'
    
    @patch('builtins.open', mock_open(read_data='''
    {
        "server": {"host": "localhost", "port": 8888},
        "logging": {"level": "WARNING"},
        "database": {"pool_size": 20}
    }
    '''))
    def test_load_from_json_file(self):
        """Test loading configuration from JSON file."""
        config = load_from_file("config.json")
        assert config.server.host == "localhost"
        assert config.server.port == 8888
        assert config.logging.level == "WARNING"
        assert config.database.pool_size == 20
    
    @patch('builtins.open', mock_open(read_data='''
    server:
      host: 0.0.0.0
      port: 3000
    logging:
      level: ERROR
    '''))
    @patch('marvin.config.yaml')
    def test_load_from_yaml_file(self, mock_yaml):
        """Test loading configuration from YAML file."""
        mock_yaml.safe_load.return_value = {
            'server': {'host': '0.0.0.0', 'port': 3000},
            'logging': {'level': 'ERROR'}
        }
        
        config = load_from_file("config.yaml")
        assert config.server.host == "0.0.0.0"
        assert config.server.port == 3000
        assert config.logging.level == "ERROR"
    
    def test_load_from_nonexistent_file(self):
        """Test loading from non-existent file raises error."""
        with pytest.raises(FileNotFoundError):
            load_from_file("nonexistent.json")
    
    @patch('marvin.config.load_from_file')
    @patch('marvin.config.load_from_env')
    @patch.dict(os.environ, {'MARVIN_CONFIG': 'custom.json'})
    def test_get_config_precedence(self, mock_env, mock_file):
        """Test configuration loading precedence."""
        file_config = Config(server=ServerConfig(port=8001))
        env_config = Config(server=ServerConfig(port=8002))
        
        mock_file.return_value = file_config
        mock_env.return_value = env_config
        
        # Should prefer file config when MARVIN_CONFIG is set
        config = get_config()
        mock_file.assert_called_once_with('custom.json')
        assert config == file_config

class TestMarvinConfig:
    """Test Marvin-specific configuration."""
    
    def test_marvin_config_defaults(self):
        """Test MarvinConfig default values."""
        marvin_config = MarvinConfig()
        assert marvin_config.template_dir == Path("templates")
        assert marvin_config.output_dir == Path("output")
        assert marvin_config.cache_enabled is True
        assert marvin_config.cache_ttl == 3600
    
    def test_marvin_config_path_expansion(self):
        """Test path expansion for directories."""
        marvin_config = MarvinConfig(
            template_dir="~/templates",
            output_dir="$HOME/output"
        )
        assert str(marvin_config.template_dir).startswith(str(Path.home()))
        assert str(marvin_config.output_dir).startswith(str(Path.home()))
```

## 2. Testing `cli.py` (0% → 100%)

### Test Structure
```python
# tests/unit/test_cli.py
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from pathlib import Path

from marvin.cli import cli, process_prd, server, version

class TestCLI:
    """Test CLI main entry point and commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
    
    def test_cli_help(self):
        """Test CLI help command."""
        result = self.runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Marvin CLI' in result.output
        assert 'Commands:' in result.output
    
    def test_version_command(self):
        """Test version command."""
        result = self.runner.invoke(cli, ['version'])
        assert result.exit_code == 0
        assert 'Marvin version' in result.output
        assert '0.1.0' in result.output  # Update with actual version

class TestProcessCommand:
    """Test process_prd command."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    @patch('marvin.cli.DocumentAnalysisAgent')
    @patch('marvin.cli.TemplateGenerationAgent')
    def test_process_prd_success(self, mock_template_agent, mock_doc_agent):
        """Test successful PRD processing."""
        # Mock agent responses
        mock_doc_agent.return_value.execute.return_value = MagicMock(
            features=[MagicMock(id='F001', title='Test Feature')]
        )
        mock_template_agent.return_value.execute.return_value = MagicMock(
            template_path=Path('output/template.xml')
        )
        
        with self.runner.isolated_filesystem():
            # Create test PRD file
            with open('test_prd.md', 'w') as f:
                f.write('# Test PRD\n\n## Features\n\n- Feature 1')
            
            result = self.runner.invoke(cli, ['process', 'test_prd.md'])
            
            assert result.exit_code == 0
            assert 'Processing PRD' in result.output
            assert 'Generated template' in result.output
    
    def test_process_prd_file_not_found(self):
        """Test process command with non-existent file."""
        result = self.runner.invoke(cli, ['process', 'nonexistent.md'])
        assert result.exit_code != 0
        assert 'Error' in result.output
        assert 'not found' in result.output.lower()
    
    @patch('marvin.cli.Path')
    def test_process_prd_with_codebase_option(self, mock_path):
        """Test process command with codebase option."""
        mock_path.return_value.exists.return_value = True
        mock_path.return_value.is_dir.return_value = True
        
        with self.runner.isolated_filesystem():
            with open('test_prd.md', 'w') as f:
                f.write('# Test PRD')
            
            result = self.runner.invoke(cli, [
                'process', 'test_prd.md',
                '--codebase', '/path/to/code'
            ])
            
            # Verify codebase path was validated
            mock_path.assert_called_with('/path/to/code')

class TestServerCommand:
    """Test server command."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    @patch('marvin.cli.uvicorn.run')
    def test_server_default_options(self, mock_uvicorn):
        """Test server with default options."""
        result = self.runner.invoke(cli, ['server'])
        
        assert result.exit_code == 0
        mock_uvicorn.assert_called_once_with(
            'marvin.adapters.api.server:app',
            host='127.0.0.1',
            port=8000,
            reload=False
        )
    
    @patch('marvin.cli.uvicorn.run')
    def test_server_custom_options(self, mock_uvicorn):
        """Test server with custom options."""
        result = self.runner.invoke(cli, [
            'server',
            '--host', '0.0.0.0',
            '--port', '9000',
            '--reload'
        ])
        
        assert result.exit_code == 0
        mock_uvicorn.assert_called_once_with(
            'marvin.adapters.api.server:app',
            host='0.0.0.0',
            port=9000,
            reload=True
        )

class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def setup_method(self):
        self.runner = CliRunner()
    
    def test_invalid_command(self):
        """Test invalid command handling."""
        result = self.runner.invoke(cli, ['invalid-command'])
        assert result.exit_code != 0
        assert 'No such command' in result.output
    
    @patch('marvin.cli.logger')
    def test_exception_logging(self, mock_logger):
        """Test that exceptions are properly logged."""
        with patch('marvin.cli.DocumentAnalysisAgent') as mock_agent:
            mock_agent.side_effect = Exception("Test error")
            
            result = self.runner.invoke(cli, ['process', 'test.md'])
            
            assert result.exit_code != 0
            mock_logger.error.assert_called()
```

## 3. Testing `api.py` (0% → 100%)

### Test Structure
```python
# tests/unit/test_api.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime

from marvin.api import create_app, process_prd_endpoint, health_check

class TestAPI:
    """Test API endpoints and application factory."""
    
    def setup_method(self):
        """Set up test client."""
        self.app = create_app()
        self.client = TestClient(self.app)
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
    
    def test_root_redirect(self):
        """Test root path redirects to docs."""
        response = self.client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/docs"

class TestProcessPRDEndpoint:
    """Test PRD processing endpoint."""
    
    def setup_method(self):
        self.app = create_app()
        self.client = TestClient(self.app)
    
    @patch('marvin.api.DocumentAnalysisAgent')
    @patch('marvin.api.TemplateGenerationAgent')
    def test_process_prd_success(self, mock_template_agent, mock_doc_agent):
        """Test successful PRD processing via API."""
        # Mock agent responses
        mock_prd = MagicMock()
        mock_prd.dict.return_value = {
            "title": "Test PRD",
            "version": "1.0.0",
            "features": [{"id": "F001", "title": "Feature 1"}]
        }
        mock_doc_agent.return_value.execute.return_value = mock_prd
        
        mock_template_agent.return_value.execute.return_value = MagicMock(
            template_content="<template>...</template>"
        )
        
        response = self.client.post(
            "/process",
            files={"file": ("test.md", b"# Test PRD", "text/markdown")}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "prd" in data
        assert "template" in data
    
    def test_process_prd_no_file(self):
        """Test process endpoint without file."""
        response = self.client.post("/process")
        assert response.status_code == 422
    
    def test_process_prd_invalid_file_type(self):
        """Test process endpoint with non-markdown file."""
        response = self.client.post(
            "/process",
            files={"file": ("test.txt", b"Not markdown", "text/plain")}
        )
        assert response.status_code == 400
        assert "must be markdown" in response.json()["detail"].lower()
    
    @patch('marvin.api.DocumentAnalysisAgent')
    def test_process_prd_agent_error(self, mock_doc_agent):
        """Test process endpoint when agent fails."""
        mock_doc_agent.return_value.execute.side_effect = Exception("Agent error")
        
        response = self.client.post(
            "/process",
            files={"file": ("test.md", b"# Test", "text/markdown")}
        )
        
        assert response.status_code == 500
        assert "error" in response.json()["status"]

class TestAPIMiddleware:
    """Test API middleware and configuration."""
    
    def setup_method(self):
        self.app = create_app()
        self.client = TestClient(self.app)
    
    def test_cors_headers(self):
        """Test CORS headers are properly set."""
        response = self.client.options("/health")
        assert "access-control-allow-origin" in response.headers
    
    def test_request_id_header(self):
        """Test request ID is added to responses."""
        response = self.client.get("/health")
        assert "x-request-id" in response.headers
    
    @patch('marvin.api.logger')
    def test_request_logging(self, mock_logger):
        """Test requests are logged."""
        self.client.get("/health")
        mock_logger.info.assert_called()

class TestAPISecurity:
    """Test API security features."""
    
    def setup_method(self):
        self.app = create_app(enable_auth=True)
        self.client = TestClient(self.app)
    
    def test_unauthorized_request(self):
        """Test request without auth token."""
        response = self.client.get("/process")
        assert response.status_code == 401
    
    def test_authorized_request(self):
        """Test request with valid auth token."""
        headers = {"Authorization": "Bearer valid-token"}
        with patch('marvin.api.verify_token', return_value=True):
            response = self.client.get("/health", headers=headers)
            assert response.status_code == 200
```

## 4. Testing ADK Agents Internal Methods

### Test Structure for ADK Callback Context
```python
# tests/unit/test_adk_agents_internals.py
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import google.adk.agents.callback_context as callback_context

from marvin.adapters.adk_agents.marvin_orchestrator_adk import MarvinOrchestratorADKAgent

class TestADKCallbackContext:
    """Test ADK callback context handling."""
    
    @patch('google.adk.agents.callback_context.get_callback_context')
    def test_callback_context_in_agent_methods(self, mock_get_context):
        """Test callback context is properly used in agent methods."""
        # Mock context
        mock_context = MagicMock()
        mock_context.session_id = "test-session-123"
        mock_context.user_id = "user-456"
        mock_get_context.return_value = mock_context
        
        agent = MarvinOrchestratorADKAgent()
        
        # Test context is accessed during initialization
        assert agent._get_session_context() is not None
        mock_get_context.assert_called()
    
    @patch('google.adk.agents.callback_context.set_callback_context')
    def test_callback_context_propagation(self, mock_set_context):
        """Test callback context is propagated to sub-agents."""
        agent = MarvinOrchestratorADKAgent()
        
        # Simulate context propagation
        test_context = {"session": "test", "user": "test-user"}
        agent._propagate_context(test_context)
        
        mock_set_context.assert_called_with(test_context)
    
    def test_callback_context_error_handling(self):
        """Test graceful handling when callback context is unavailable."""
        with patch('google.adk.agents.callback_context.get_callback_context', 
                  side_effect=Exception("Context not available")):
            
            agent = MarvinOrchestratorADKAgent()
            # Should handle gracefully and use defaults
            assert agent._get_session_context() is None

class TestADKAgentEdgeCases:
    """Test edge cases in ADK agent implementations."""
    
    def test_agent_state_persistence(self):
        """Test agent state is properly persisted across calls."""
        agent = MarvinOrchestratorADKAgent()
        
        # Set some state
        agent._internal_state = {"key": "value"}
        
        # Simulate new request with same session
        with patch.object(agent, '_load_state') as mock_load:
            mock_load.return_value = agent._internal_state
            
            new_state = agent._get_state()
            assert new_state == {"key": "value"}
    
    @pytest.mark.asyncio
    async def test_async_callback_handling(self):
        """Test async callbacks in ADK agents."""
        agent = MarvinOrchestratorADKAgent()
        
        # Mock async callback
        async_callback = AsyncMock(return_value="callback_result")
        
        result = await agent._handle_async_callback(async_callback)
        assert result == "callback_result"
        async_callback.assert_awaited_once()
```

## 5. Coverage Configuration Updates

### Update `pyproject.toml`
```toml
[tool.coverage.run]
branch = true
source = ["src/marvin"]
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/venv/*",
    "*/site-packages/*",
    "*/.tox/*",
    "*/migrations/*",
    "*/config/*",
    "*/manage.py",
    "*/setup.py",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
fail_under = 100
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if 0:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"

[tool.pytest.ini_options]
minversion = "6.0"
addopts = """
    -ra
    --strict-markers
    --cov=marvin
    --cov-branch
    --cov-report=term-missing:skip-covered
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=100
    --maxfail=1
    --tb=short
"""
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
    "asyncio: marks tests as async",
]
```

## 6. Pre-commit Hook for TDD

### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: local
    hooks:
      - id: test-before-commit
        name: Run tests before commit
        entry: bash -c 'uv run pytest --cov-fail-under=100 || (echo "Tests failed or coverage below 100%!" && exit 1)'
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]

      - id: check-test-exists
        name: Check test file exists for new code
        entry: python scripts/check_test_exists.py
        language: python
        files: '^src/.*\.py$'
        exclude: '^src/.*/__init__\.py$'
```

### Test Existence Checker Script
```python
# scripts/check_test_exists.py
#!/usr/bin/env python3
import sys
import os
from pathlib import Path

def check_test_exists(filepath):
    """Check if a test file exists for the given source file."""
    src_path = Path(filepath)
    
    # Convert src path to test path
    test_path = Path(str(src_path).replace('src/', 'tests/unit/').replace('.py', '_test.py'))
    alt_test_path = Path(str(src_path).replace('src/', 'tests/unit/test_'))
    
    if not test_path.exists() and not alt_test_path.exists():
        print(f"ERROR: No test file found for {filepath}")
        print(f"Expected: {test_path} or {alt_test_path}")
        return False
    
    return True

if __name__ == "__main__":
    all_good = True
    for filepath in sys.argv[1:]:
        if not check_test_exists(filepath):
            all_good = False
    
    sys.exit(0 if all_good else 1)
```

## Next Steps

1. **Immediate Actions:**
   - Install pre-commit: `uv pip install pre-commit && pre-commit install`
   - Run coverage baseline: `uv run pytest --cov --cov-report=html`
   - Review coverage report: `open htmlcov/index.html`

2. **Week 1 Goals:**
   - Implement tests for `config.py`
   - Implement tests for `cli.py`
   - Set up CI/CD coverage gates

3. **Tracking Progress:**
   - Create GitHub issues for each module
   - Use labels: `test-coverage`, `tdd`
   - Track in project board

Remember: **No code without tests! Red → Green → Refactor**