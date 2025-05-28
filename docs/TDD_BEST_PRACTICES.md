# 🧪 Test-Driven Development Best Practices

## 🎯 TDD Philosophy

> "Never write a line of code without a failing test." - Kent Beck

## 🔄 The TDD Cycle

### 1. RED 🔴 - Write a Failing Test
```python
def test_calculate_discount_applies_percentage():
    """Test that discount calculation applies correct percentage."""
    # This test will fail because calculate_discount doesn't exist yet
    result = calculate_discount(100, 0.2)
    assert result == 80
```

### 2. GREEN 🟢 - Make it Pass (Minimal Code)
```python
def calculate_discount(price, discount_rate):
    """Calculate discounted price."""
    return price * (1 - discount_rate)
```

### 3. REFACTOR 🔵 - Improve the Code
```python
from decimal import Decimal

def calculate_discount(price: Decimal, discount_rate: Decimal) -> Decimal:
    """
    Calculate discounted price with proper decimal handling.
    
    Args:
        price: Original price
        discount_rate: Discount rate (0.0 to 1.0)
        
    Returns:
        Discounted price
        
    Raises:
        ValueError: If discount_rate is not between 0 and 1
    """
    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1")
    
    return price * (Decimal('1') - discount_rate)
```

## 📋 Test Writing Guidelines

### 1. Test Naming Convention
```python
def test_<unit>_<scenario>_<expected_behavior>():
    """Test that <unit> <expected behavior> when <scenario>."""
```

**Examples:**
```python
def test_user_repository_find_by_email_returns_none_when_not_found():
    """Test that UserRepository returns None when email not found."""

def test_prd_parser_extract_features_handles_empty_document():
    """Test that PRD parser handles empty document gracefully."""
```

### 2. Test Structure (AAA Pattern)
```python
def test_feature_extraction():
    """Test feature extraction from PRD."""
    # Arrange - Set up test data
    prd_content = "# PRD\n## Features\n- Feature 1\n- Feature 2"
    parser = PRDParser()
    
    # Act - Execute the code
    features = parser.extract_features(prd_content)
    
    # Assert - Verify the result
    assert len(features) == 2
    assert features[0].title == "Feature 1"
```

### 3. Test Isolation
```python
class TestDatabaseOperations:
    """Test database operations in isolation."""
    
    def setup_method(self):
        """Create test database for each test."""
        self.db = create_test_database()
        self.repository = UserRepository(self.db)
    
    def teardown_method(self):
        """Clean up after each test."""
        self.db.drop_all_tables()
        self.db.close()
    
    def test_save_user(self):
        """Test saving user to database."""
        # Each test gets a fresh database
        user = User(email="test@example.com")
        self.repository.save(user)
        assert self.repository.count() == 1
```

## 🎨 Test Patterns

### 1. Parameterized Tests
```python
@pytest.mark.parametrize("input_value,expected", [
    ("", ValueError),
    ("invalid-email", ValueError),
    ("user@example.com", None),
    ("user+tag@example.com", None),
])
def test_email_validation(input_value, expected):
    """Test email validation with various inputs."""
    if expected is ValueError:
        with pytest.raises(ValueError):
            validate_email(input_value)
    else:
        assert validate_email(input_value) is None
```

### 2. Fixture Composition
```python
@pytest.fixture
def valid_prd():
    """Provide a valid PRD for testing."""
    return PRD(
        title="Test PRD",
        version="1.0.0",
        features=[
            Feature(id="F1", title="Feature 1"),
            Feature(id="F2", title="Feature 2"),
        ]
    )

@pytest.fixture
def template_generator(valid_prd):
    """Provide template generator with PRD."""
    return TemplateGenerator(prd=valid_prd)

def test_template_generation(template_generator):
    """Test template generation with fixtures."""
    result = template_generator.generate()
    assert "<template>" in result
```

### 3. Mock External Dependencies
```python
def test_api_client_handles_network_error():
    """Test API client handles network errors gracefully."""
    with patch('requests.get') as mock_get:
        # Simulate network error
        mock_get.side_effect = ConnectionError("Network error")
        
        client = APIClient()
        result = client.fetch_data()
        
        assert result is None
        assert client.last_error == "Network error"
```

## 🚫 Common Anti-Patterns

### ❌ Testing Implementation Details
```python
# BAD - Tests internal implementation
def test_cache_uses_dict():
    cache = Cache()
    assert isinstance(cache._storage, dict)  # Don't test internals!
```

### ✅ Test Behavior Instead
```python
# GOOD - Tests behavior
def test_cache_stores_and_retrieves_values():
    cache = Cache()
    cache.set("key", "value")
    assert cache.get("key") == "value"
```

### ❌ Multiple Assertions Without Context
```python
# BAD - Hard to know which assertion failed
def test_user_creation():
    user = User("John", "Doe", "john@example.com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"
    assert user.full_name == "John Doe"
```

### ✅ Use Descriptive Assertions
```python
# GOOD - Clear failure messages
def test_user_creation():
    user = User("John", "Doe", "john@example.com")
    
    assert user.first_name == "John", "First name not set correctly"
    assert user.last_name == "Doe", "Last name not set correctly"
    assert user.email == "john@example.com", "Email not set correctly"
    assert user.full_name == "John Doe", "Full name not computed correctly"
```

## 🎯 Coverage Best Practices

### 1. Branch Coverage
```python
def divide(a, b):
    """Divide two numbers."""
    if b == 0:  # Branch 1
        return None
    return a / b  # Branch 2

# Tests must cover both branches
def test_divide_normal_case():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    assert divide(10, 0) is None
```

### 2. Edge Cases
```python
class TestStringProcessor:
    """Test string processing edge cases."""
    
    def test_empty_string(self):
        assert process_string("") == ""
    
    def test_none_input(self):
        with pytest.raises(TypeError):
            process_string(None)
    
    def test_unicode_characters(self):
        assert process_string("héllo 世界") == "HÉLLO 世界"
    
    def test_very_long_string(self):
        long_string = "a" * 1_000_000
        result = process_string(long_string)
        assert len(result) == 1_000_000
```

### 3. Error Paths
```python
def test_file_reader_handles_missing_file():
    """Test file reader handles missing files."""
    reader = FileReader()
    
    with pytest.raises(FileNotFoundError) as exc_info:
        reader.read("nonexistent.txt")
    
    assert "not found" in str(exc_info.value)
```

## 🛠️ Testing Tools

### Essential pytest Plugins
```bash
# Install testing tools
uv pip install pytest-cov pytest-xdist pytest-timeout pytest-mock pytest-asyncio

# Run tests in parallel
uv run pytest -n auto

# Run with timeout
uv run pytest --timeout=10

# Run only fast tests
uv run pytest -m "not slow"
```

### Helpful Fixtures
```python
# conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    yield file_path
    # Cleanup happens automatically

@pytest.fixture
def mock_time():
    """Mock time for deterministic tests."""
    with patch('time.time', return_value=1234567890):
        yield

@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset singleton instances between tests."""
    SingletonClass._instance = None
    yield
    SingletonClass._instance = None
```

## 📊 Measuring Test Quality

### 1. Mutation Testing
```bash
# Install mutmut
uv pip install mutmut

# Run mutation testing
mutmut run --paths-to-mutate=src/

# View results
mutmut results
```

### 2. Test Execution Time
```python
# Mark slow tests
@pytest.mark.slow
def test_complex_algorithm():
    """Test complex algorithm (takes >1 second)."""
    result = complex_calculation()
    assert result == expected

# Run excluding slow tests
# uv run pytest -m "not slow"
```

### 3. Test Flakiness Detection
```bash
# Run tests multiple times to detect flaky tests
uv run pytest --count=10 -x

# Use pytest-randomly to randomize test order
uv pip install pytest-randomly
uv run pytest --randomly-seed=1234
```

## 🏃 TDD Workflow Commands

```bash
# 1. Create test file first
touch tests/unit/test_new_feature.py

# 2. Write failing test
echo 'def test_new_feature():
    assert calculate_value(10) == 20' > tests/unit/test_new_feature.py

# 3. Run test (should fail)
uv run pytest tests/unit/test_new_feature.py -v

# 4. Implement minimal code
echo 'def calculate_value(x):
    return x * 2' > src/marvin/new_feature.py

# 5. Run test again (should pass)
uv run pytest tests/unit/test_new_feature.py -v

# 6. Check coverage
uv run pytest --cov=marvin --cov-report=term-missing

# 7. Refactor if needed
# ... edit code ...

# 8. Ensure tests still pass
uv run pytest
```

## 🎓 Learning Resources

1. **Books:**
   - "Test Driven Development: By Example" - Kent Beck
   - "Growing Object-Oriented Software, Guided by Tests" - Freeman & Pryce
   - "Working Effectively with Legacy Code" - Michael Feathers

2. **Online Resources:**
   - [pytest Documentation](https://docs.pytest.org/)
   - [Python Testing 101](https://realpython.com/python-testing/)
   - [TDD with Python](https://www.obeythetestinggoat.com/)

3. **Videos:**
   - [TDD in Python by Harry Percival](https://www.youtube.com/watch?v=Hw7K6KI5M6o)
   - [Ian Cooper - TDD, Where Did It All Go Wrong](https://www.youtube.com/watch?v=EZ05e7EMOLM)

## 🏆 TDD Checklist

Before committing code, ensure:

- [ ] ✅ Test written BEFORE implementation
- [ ] ✅ Test fails initially (RED)
- [ ] ✅ Minimal code to pass test (GREEN)
- [ ] ✅ Code refactored (BLUE)
- [ ] ✅ All tests still pass
- [ ] ✅ 100% code coverage maintained
- [ ] ✅ No TODOs in tests
- [ ] ✅ Tests are readable and documented
- [ ] ✅ Edge cases covered
- [ ] ✅ Error paths tested

Remember: **The test is the first user of your code!**