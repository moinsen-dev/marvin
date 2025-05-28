# Releasing Marvin

This guide describes the release process for Marvin, including versioning, testing, and publishing to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on [PyPI](https://pypi.org/) and [Test PyPI](https://test.pypi.org/)
2. **API Tokens**: Generate API tokens for both PyPI and Test PyPI
3. **GitHub Secrets**: Add the following secrets to the repository:
   - `PYPI_API_TOKEN` - Your PyPI API token
   - `TEST_PYPI_API_TOKEN` - Your Test PyPI API token
4. **Permissions**: Ensure you have write access to the repository and can create tags

## Versioning Strategy

We follow [Semantic Versioning 2.0.0](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (0.X.0): New features, backwards compatible
- **PATCH** (0.0.X): Bug fixes, backwards compatible
- **Pre-releases**: 
  - Alpha (X.Y.Z-alpha.N): Early testing, may be unstable
  - Beta (X.Y.Z-beta.N): Feature complete, needs testing
  - RC (X.Y.Z-rc.N): Release candidate, final testing

## Automated Release Process

### 1. Prepare the Release

```bash
# Ensure you're on the develop branch
git checkout develop
git pull origin develop

# Run all quality checks
./check_code.sh

# Bump version using the script
python scripts/bump_version.py patch  # or minor/major/alpha/beta/rc

# This will:
# - Update version in pyproject.toml and __init__.py
# - Add a new section to CHANGELOG.md
# - Show you the next steps
```

### 2. Update Changelog

Edit `CHANGELOG.md` to add your actual changes under the new version section:

```markdown
## [0.1.1] - 2024-05-28

### Added
- New feature for X
- Support for Y

### Changed
- Improved performance of Z

### Fixed
- Bug in feature A
- Issue with B

### Security
- Updated dependency C to fix CVE-XXXX
```

### 3. Commit and Create PR

```bash
# Commit the version changes
git add -A
git commit -m "chore: bump version to 0.1.1"

# Push to a feature branch
git push origin develop:release/v0.1.1

# Create a PR from release/v0.1.1 to main
# The PR will trigger changelog validation
```

### 4. Merge and Tag

After PR approval and merge to main:

```bash
# Switch to main
git checkout main
git pull origin main

# Create and push the version tag
git tag -a v0.1.1 -m "Release v0.1.1"
git push origin v0.1.1
```

### 5. Automated Release

The tag push will trigger the automated release workflow that:

1. Validates version consistency
2. Runs all tests and quality checks
3. Builds the distribution packages
4. Creates a GitHub Release with changelog
5. Publishes to PyPI (or Test PyPI for pre-releases)
6. Updates the documentation

### 6. Verify the Release

```bash
# Wait for the workflow to complete (~5-10 minutes)

# Install from PyPI
pip install --upgrade marvin

# Verify installation
marvin --version  # Should show 0.1.1
marvin --help

# Check PyPI page
# https://pypi.org/project/marvin/
```

## Manual Release Process

For special cases or troubleshooting:

```bash
# 1. Clean previous builds
rm -rf dist/ build/ *.egg-info

# 2. Ensure version is correct
python scripts/bump_version.py --current

# 3. Build the package
uv run python -m build

# 4. Check the package
uv run twine check dist/*

# 5. Upload to Test PyPI (optional)
uv run twine upload -r testpypi dist/*

# 6. Test installation from Test PyPI
pip install -i https://test.pypi.org/simple/ marvin==0.1.1

# 7. Upload to PyPI
uv run twine upload dist/*
```

## Pre-release Workflow

For alpha/beta/RC releases:

```bash
# 1. Bump to pre-release version
python scripts/bump_version.py alpha  # Creates X.Y.Z-alpha.1

# 2. Follow normal release process
# Pre-releases will automatically:
# - Be marked as pre-release on GitHub
# - Be published to Test PyPI instead of PyPI
# - Not update the "latest" documentation

# 3. To promote to stable:
python scripts/bump_version.py patch  # Removes pre-release suffix
```

## Hotfix Process

For urgent fixes to production:

```bash
# 1. Create hotfix branch from main
git checkout main
git checkout -b hotfix/v0.1.2

# 2. Make the fix and bump patch version
python scripts/bump_version.py patch

# 3. Update CHANGELOG.md with the fix

# 4. Create PR directly to main
# 5. After merge, tag and release as normal
```

## Version Management Commands

```bash
# Show current version
python scripts/bump_version.py --current

# Bump versions
python scripts/bump_version.py major     # 0.1.0 -> 1.0.0
python scripts/bump_version.py minor     # 0.1.0 -> 0.2.0
python scripts/bump_version.py patch     # 0.1.0 -> 0.1.1

# Pre-releases
python scripts/bump_version.py alpha     # 0.1.0 -> 0.1.1-alpha.1
python scripts/bump_version.py beta      # 0.1.1-alpha.1 -> 0.1.1-beta.1
python scripts/bump_version.py rc        # 0.1.1-beta.1 -> 0.1.1-rc.1

# Dry run (see what would change)
python scripts/bump_version.py patch --dry-run
```

## Release Checklist

### Pre-release
- [ ] All tests pass (`uv run pytest`)
- [ ] Code quality checks pass (`./check_code.sh`)
- [ ] No security vulnerabilities (`uv pip audit`)
- [ ] Documentation is up to date
- [ ] CHANGELOG.md has been updated
- [ ] Version bumped appropriately

### Release
- [ ] Create release PR from develop to main
- [ ] PR passes all CI checks
- [ ] PR approved by maintainer
- [ ] Merge PR to main
- [ ] Create and push version tag
- [ ] GitHub Release created automatically
- [ ] PyPI package published automatically

### Post-release
- [ ] Verify package on PyPI
- [ ] Test installation: `pip install marvin=={version}`
- [ ] Documentation deployed successfully
- [ ] Announce release:
  - [ ] GitHub Discussions
  - [ ] Discord community
  - [ ] Twitter/Social media
- [ ] Create milestone for next version

## Workflow Triggers

### Automatic Workflows

1. **On PR to main**: Changelog validation
2. **On push to tag v***: Full release workflow
3. **On release creation**: PyPI publication
4. **On push to develop/main**: Documentation update

### Manual Workflows

1. **Generate Changelog**: Actions → Changelog Management → Run workflow
2. **Test PyPI Release**: Actions → Publish to PyPI → Run workflow
3. **Version Bump PR**: Use `scripts/bump_version.py` locally

## Troubleshooting

### Version Mismatch Error

If the release workflow fails with version mismatch:

```bash
# Check all version locations
grep -n "0.1.0" pyproject.toml src/marvin/__init__.py

# Fix using the script
python scripts/bump_version.py --current
python scripts/bump_version.py patch  # Re-apply version
```

### Package Name Conflicts

If `marvin` is taken on PyPI, update `pyproject.toml`:

```toml
[project]
name = "marvin-prd"  # or another unique name
```

### Failed GitHub Release

If the automated release fails:

1. Check Actions tab for error details
2. Fix the issue
3. Delete the failed release/tag if created
4. Re-run by pushing the tag again

### PyPI Upload Errors

Common issues and solutions:

```bash
# Token authentication failed
# → Check PYPI_API_TOKEN secret in GitHub

# Package already exists
# → Bump version and try again

# Invalid package format
# → Run: uv run twine check dist/*
```

### Documentation Not Updating

```bash
# Check GitHub Pages settings
# Ensure gh-pages branch exists
# Check Actions → docs workflow for errors
```

## Release Schedule

We aim to follow this release cadence:

- **Patch releases**: As needed for bug fixes
- **Minor releases**: Every 4-6 weeks with new features
- **Major releases**: When breaking changes are necessary

Pre-releases:
- **Alpha**: For early testing of major changes
- **Beta**: 1-2 weeks before minor/major release
- **RC**: 3-5 days before final release

## Security Releases

For security vulnerabilities:

1. Create fix in a private security advisory
2. Bump patch version
3. Add security notice to CHANGELOG.md
4. Release immediately after fix is ready
5. Announce through security channels

## Rollback Procedure

If a release has critical issues:

```bash
# 1. Mark release as pre-release on GitHub

# 2. Yank from PyPI (if necessary)
# This prevents new installations but doesn't break existing ones
# Contact PyPI support for this

# 3. Create hotfix
git checkout main
git checkout -b hotfix/v{version}

# 4. Fix issue and release new patch version
```

## Monitoring

After each release, monitor:

1. **PyPI Stats**: https://pypi.org/project/marvin/
2. **GitHub Issues**: Watch for bug reports
3. **Error Tracking**: If configured
4. **Community Channels**: Discord, discussions

## Release Communication Template

```markdown
🎉 **Marvin v{version} Released!**

We're excited to announce the release of Marvin v{version}.

### ✨ Highlights
- Feature 1
- Feature 2
- Bug fixes

### 📦 Installation
```bash
pip install --upgrade marvin
```

### 📚 Documentation
- [Changelog](link)
- [Documentation](link)

### 🙏 Thanks
Thanks to all contributors who made this release possible!

#opensource #python #ai #developer-tools
```