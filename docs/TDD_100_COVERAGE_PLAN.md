# 🎯 Test-Driven Development & 100% Code Coverage Plan

## 📊 Current State Analysis

**Current Coverage: 37%** (Target: 100%)

### Coverage Breakdown:
- ✅ **100% Coverage**: domain models, XML generator
- ⚠️ **Partial Coverage**: ADK agents (18-77%), document analysis (92%)
- ❌ **Zero Coverage**: API, CLI, MCP, config, legacy agents

## 🚀 TDD Implementation Strategy

### Phase 1: Foundation (Week 1-2)
**Goal: Establish TDD culture and tooling**

1. **Coverage Infrastructure**
   ```bash
   # Add to pyproject.toml
   [tool.coverage.run]
   source = ["src/marvin"]
   omit = ["*/tests/*", "*/__pycache__/*", "*/venv/*"]
   
   [tool.coverage.report]
   fail_under = 100
   show_missing = true
   skip_covered = false
   
   [tool.pytest.ini_options]
   addopts = """
   --cov=marvin
   --cov-report=term-missing
   --cov-report=html
   --cov-fail-under=100
   --strict-markers
   """
   ```

2. **Pre-commit Hooks**
   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: local
       hooks:
         - id: test-coverage
           name: Check test coverage
           entry: uv run pytest --cov-fail-under=100
           language: system
           pass_filenames: false
           always_run: true
   ```

3. **GitHub Actions Gate**
   ```yaml
   # .github/workflows/coverage.yml
   name: Coverage Gate
   on: [push, pull_request]
   
   jobs:
     coverage:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: astral-sh/setup-uv@v3
         - run: uv sync
         - run: uv run pytest --cov-fail-under=100
         - uses: codecov/codecov-action@v4
   ```

### Phase 2: Core Module Testing (Week 3-4)
**Goal: 100% coverage for core business logic**

#### Priority Order:
1. **config.py** (103 statements)
   - Test all configuration loading
   - Mock environment variables
   - Test validation logic

2. **logging.py** (53 statements)
   - Test all log levels
   - Mock file operations
   - Test rotation logic

3. **core/agents/base.py** (33 statements)
   - Test abstract methods
   - Test initialization
   - Mock subclasses

4. **core/agents/** (remaining)
   - Test each agent independently
   - Mock external dependencies
   - Test error paths

### Phase 3: Adapter Testing (Week 5-6)
**Goal: 100% coverage for all adapters**

#### CLI Testing Strategy:
```python
# tests/unit/test_cli_commands.py
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

class TestCLICommands:
    def setup_method(self):
        self.runner = CliRunner()
    
    @patch('marvin.adapters.cli.commands.process_prd')
    def test_process_command_success(self, mock_process):
        result = self.runner.invoke(process, ['test.md'])
        assert result.exit_code == 0
        mock_process.assert_called_once()
```

#### API Testing Strategy:
```python
# tests/unit/test_api_server.py
from fastapi.testclient import TestClient
from unittest.mock import patch

class TestAPIServer:
    def setup_method(self):
        from marvin.adapters.api.server import app
        self.client = TestClient(app)
    
    def test_health_endpoint(self):
        response = self.client.get("/health")
        assert response.status_code == 200
```

#### MCP Testing Strategy:
```python
# tests/unit/test_mcp_server.py
import pytest
from unittest.mock import AsyncMock, patch

class TestMCPServer:
    @pytest.mark.asyncio
    async def test_handle_process_prd(self):
        # Test MCP protocol implementation
        pass
```

### Phase 4: ADK Agent Testing (Week 7)
**Goal: Complete ADK agent coverage**

```python
# tests/unit/test_adk_agent_internals.py
class TestADKAgentInternals:
    """Test internal methods not covered by session tests."""
    
    def test_callback_context_handling(self):
        """Test google.adk.agents.callback_context usage."""
        # Mock ADK context
        # Test all branches
```

### Phase 5: Legacy Code Removal (Week 8)
**Goal: Remove or test legacy code**

Decision matrix:
- If used → Add tests
- If unused → Delete
- If deprecated → Mark and schedule removal

## 📋 Test Categories & Patterns

### 1. Unit Tests (80% of tests)
```python
# Pattern: tests/unit/test_<module>.py
class Test<ClassName>:
    def test_<method>_<scenario>_<expected>(self):
        # Arrange
        # Act
        # Assert
```

### 2. Integration Tests (15% of tests)
```python
# Pattern: tests/integration/test_<flow>.py
class Test<Flow>Integration:
    @pytest.mark.integration
    def test_end_to_end_<scenario>(self):
        # Test full flow
```

### 3. Contract Tests (5% of tests)
```python
# Pattern: tests/contract/test_<api>.py
class Test<API>Contract:
    @pytest.mark.contract
    def test_api_contract_<endpoint>(self):
        # Validate API contracts
```

## 🛡️ Coverage Rules

### Mandatory Coverage Rules:
1. **No PR merge < 100% coverage**
2. **Every new file must have tests FIRST**
3. **Every bug fix must add a test**
4. **Coverage reports on every PR**

### Exceptions (Require Approval):
- Generated code (with `# pragma: no cover`)
- Third-party integrations (mock instead)
- Debug/development code

## 🔧 Testing Tools & Utilities

### 1. Test Factories
```python
# tests/factories.py
class PRDFactory:
    @staticmethod
    def create_valid_prd(**kwargs):
        defaults = {
            "title": "Test PRD",
            "version": "1.0.0",
            "features": []
        }
        return PRD(**{**defaults, **kwargs})
```

### 2. Fixtures
```python
# tests/conftest.py
@pytest.fixture
def mock_file_system(tmp_path):
    """Provide isolated file system."""
    return tmp_path

@pytest.fixture
def mock_config():
    """Provide test configuration."""
    return Config(debug=True)
```

### 3. Mocking Helpers
```python
# tests/helpers.py
class AsyncMockHelper:
    @staticmethod
    def async_return(value):
        future = asyncio.Future()
        future.set_result(value)
        return future
```

## 📊 Metrics & Monitoring

### Weekly Metrics:
- Coverage percentage
- New tests added
- Tests per developer
- Average test execution time

### Dashboard:
```yaml
# .github/workflows/metrics.yml
- name: Update Coverage Badge
  uses: codecov/codecov-action@v4
  
- name: Comment PR with Coverage
  uses: py-cov-action/python-coverage-comment-action@v3
```

## 🎓 TDD Training Plan

### Week 1: TDD Basics
- Red-Green-Refactor cycle
- Writing testable code
- Mocking strategies

### Week 2: Advanced Testing
- Async testing
- Property-based testing
- Performance testing

### Week 3: Tool Mastery
- pytest advanced features
- Coverage analysis
- CI/CD integration

## 📅 Timeline & Milestones

| Week | Target Coverage | Focus Area |
|------|----------------|------------|
| 1-2  | 40% → 50%     | Foundation & Tools |
| 3-4  | 50% → 70%     | Core Modules |
| 5-6  | 70% → 85%     | Adapters |
| 7    | 85% → 95%     | ADK Agents |
| 8    | 95% → 100%    | Final Push |

## 🏆 Success Criteria

1. **100% code coverage maintained**
2. **All tests run < 30 seconds**
3. **Zero flaky tests**
4. **TDD adopted by all developers**
5. **Coverage gates enforced**

## 🚦 Implementation Checklist

- [ ] Set up coverage infrastructure
- [ ] Configure pre-commit hooks
- [ ] Update CI/CD with coverage gates
- [ ] Create test templates
- [ ] Write missing unit tests
- [ ] Add integration tests
- [ ] Remove/test legacy code
- [ ] Document testing best practices
- [ ] Train team on TDD
- [ ] Celebrate 100% coverage! 🎉

## 📚 Resources

- [TDD by Example - Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Python Testing with pytest](https://pragprog.com/titles/bopytest2/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Google ADK Testing Guide](https://google.github.io/adk-docs/get-started/testing/)