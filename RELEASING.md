# Releasing Marvin to PyPI

This guide describes how to release Marvin to the Python Package Index (PyPI).

## Prerequisites

1. **PyPI Account**: Create accounts on [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/)
2. **API Tokens**: Generate API tokens for both PyPI and Test PyPI
3. **GitHub Secrets**: Add the following secrets to the repository:
   - `PYPI_API_TOKEN` - Your PyPI API token
   - `TEST_PYPI_API_TOKEN` - Your Test PyPI API token

## Release Process

### 1. Prepare the Release

```bash
# Ensure all tests pass
uv run pytest

# Run code quality checks
uv run black src tests
uv run isort src tests
uv run ruff check src tests
uv run mypy src

# Update version in pyproject.toml
# Update CHANGELOG.md with release notes
```

### 2. Test the Release (Recommended)

Use the GitHub Actions workflow to test the release on Test PyPI:

1. Go to Actions → "Publish to PyPI" workflow
2. Click "Run workflow"
3. Keep "Publish to Test PyPI" checked
4. Run the workflow

Test the package from Test PyPI:
```bash
pip install -i https://test.pypi.org/simple/ marvin-prd
marvin --version
```

### 3. Create a GitHub Release

1. Go to the repository's Releases page
2. Click "Draft a new release"
3. Create a new tag (e.g., `v0.1.0`)
4. Set the release title (e.g., "v0.1.0 - Initial Release")
5. Add release notes from CHANGELOG.md
6. Publish the release

This will automatically trigger the PyPI publication workflow.

### 4. Verify the Release

```bash
# Install from PyPI
pip install marvin-prd

# Verify installation
marvin --version
marvin --help
```

## Manual Release (Alternative)

If you prefer to release manually:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
python -m build

# Check the package
twine check dist/*

# Upload to Test PyPI (optional)
twine upload -r testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Version Management

Follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

Update the version in `pyproject.toml`:
```toml
[project]
version = "0.1.0"  # Update this
```

## Release Checklist

- [ ] All tests pass (`uv run pytest`)
- [ ] Code quality checks pass
- [ ] Version updated in `pyproject.toml`
- [ ] CHANGELOG.md updated with release notes
- [ ] Documentation updated if needed
- [ ] README updated if needed
- [ ] Test release on Test PyPI
- [ ] Create GitHub release with tag
- [ ] Verify package on PyPI
- [ ] Announce release (Twitter, Discord, etc.)

## Troubleshooting

### Package Name Already Taken

If `marvin` is taken on PyPI, we use `marvin-prd` as the package name.

### Build Errors

```bash
# Ensure build tools are up to date
pip install --upgrade build twine setuptools wheel

# Clean and rebuild
rm -rf dist/ build/
python -m build
```

### Authentication Errors

- Ensure you're using API tokens, not username/password
- Tokens should start with `pypi-`
- Check that tokens are correctly set in GitHub Secrets

## Post-Release

1. Monitor PyPI download statistics
2. Watch for issues reported by users
3. Plan next release based on feedback