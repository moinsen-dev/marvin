# GitHub Repository Metadata

This file contains the metadata that should be configured in the GitHub repository settings.

## About Section

**Description:**
```
🤖 Intelligent PRD-to-AI-Tasks converter | Transform Product Requirements into structured templates for Cursor, Windsurf & Claude Code
```

**Website:**
```
https://moinsen-dev.github.io/marvin/
```

**Topics (Tags):**
- `prd`
- `ai-coding-assistant`
- `cursor`
- `windsurf`
- `claude-code`
- `template-generator`
- `developer-tools`
- `ai-powered`
- `code-generation`
- `google-adk`
- `python`
- `fastapi`
- `xml-templates`
- `automation`

## Features to Enable

- ✅ Issues
- ✅ Projects
- ✅ Wiki
- ✅ Discussions
- ✅ Actions
- ✅ Security alerts
- ✅ Dependency graph
- ✅ Dependabot alerts

## Branch Protection Rules (for `main` branch)

- ✅ Require a pull request before merging
  - ✅ Require approvals (1)
  - ✅ Dismiss stale pull request approvals when new commits are pushed
- ✅ Require status checks to pass before merging
  - Required checks:
    - `test`
    - `lint`
    - `type-check`
- ✅ Require branches to be up to date before merging
- ✅ Include administrators
- ✅ Restrict who can push to matching branches (maintainers only)

## Release Settings

- **Default branch:** `develop`
- **Production branch:** `main`
- **Automatically delete head branches:** Yes
- **Allow merge commits:** Yes
- **Allow squash merging:** Yes
- **Allow rebase merging:** No
- **Suggest updating pull request branches:** Yes

## Pages Settings

- **Source:** Deploy from a branch
- **Branch:** `gh-pages`
- **Folder:** `/` (root)
- **Custom domain:** (optional - if you have one)
- **Enforce HTTPS:** Yes

## Environments

### `production`
- **URL:** https://pypi.org/project/marvin/
- **Required reviewers:** Maintainers
- **Deployment branches:** `main` only

### `test-pypi`
- **URL:** https://test.pypi.org/project/marvin/
- **Required reviewers:** None
- **Deployment branches:** All branches

### `documentation`
- **URL:** https://moinsen-dev.github.io/marvin/
- **Required reviewers:** None
- **Deployment branches:** `develop`, `main`

## Secrets and Variables

### Secrets (required)
- `PYPI_API_TOKEN` - PyPI API token for publishing
- `TEST_PYPI_API_TOKEN` - Test PyPI API token for testing
- `CODECOV_TOKEN` - (optional) For coverage reports
- `GOOGLE_API_KEY` - (for testing with Google ADK)

### Variables
- `MIN_COVERAGE` - Minimum test coverage percentage (e.g., "80")
- `PYTHON_VERSIONS` - Python versions to test (e.g., "3.11,3.12")

## Labels

Create these labels for better issue/PR management:

- `bug` - Something isn't working (color: #d73a4a)
- `enhancement` - New feature or request (color: #a2eeef)
- `documentation` - Improvements or additions to documentation (color: #0075ca)
- `good first issue` - Good for newcomers (color: #7057ff)
- `help wanted` - Extra attention is needed (color: #008672)
- `breaking change` - Introduces breaking changes (color: #d93f0b)
- `dependencies` - Pull requests that update a dependency file (color: #0366d6)
- `release` - Related to releases (color: #5319e7)
- `ci/cd` - Related to CI/CD workflows (color: #fbca04)
- `security` - Security-related issues (color: #d1260f)

## Issue Templates

See `.github/ISSUE_TEMPLATE/` directory for templates:
- Bug Report
- Feature Request
- Documentation Issue

## Pull Request Template

See `.github/pull_request_template.md`

## Community Standards

- Code of Conduct: `.github/CODE_OF_CONDUCT.md`
- Contributing Guidelines: `CONTRIBUTING.md`
- Security Policy: `.github/SECURITY.md`