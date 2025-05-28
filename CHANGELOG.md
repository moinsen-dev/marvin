# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive project documentation including state tracker
- MIT License
- Professional README with badges and detailed usage instructions
- This CHANGELOG file to track version history
- CLAUDE.md file for AI assistant guidance
- ADK rules documentation for agent development

### Changed
- Updated project dependencies to include google-adk
- Enhanced CLI with better command structure
- Improved project structure following Hexagonal Architecture

### Fixed
- Module import paths for proper package structure

## [0.1.0] - 2025-05-08

### Added
- Initial project structure with Hexagonal Architecture
- Core domain models (Feature, PRD, Codebase, Task, Workflow)
- Basic agent framework using Google ADK
- CLI interface with process and server commands
- FastAPI server for REST API access
- DocumentAnalyzerADK agent implementation
- Basic PRD analysis capabilities
- Codebase scanning agent skeleton
- Template generation agent skeleton
- Sequence planning agent skeleton
- Unit test structure
- Logging configuration with Loguru
- Project configuration with pyproject.toml
- Example PRD document
- XML task template format v2.0

### Security
- Content filter for document analysis
- Input validation for file paths

## [0.0.1] - 2025-05-01

### Added
- Initial project concept and planning
- Product Requirements Document (PRD)
- Basic project scaffolding

---

## Version Guidelines

### Version Format
`MAJOR.MINOR.PATCH`

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

### Pre-release Versions
- Alpha: `X.Y.Z-alpha.N` (feature incomplete)
- Beta: `X.Y.Z-beta.N` (feature complete, testing)
- RC: `X.Y.Z-rc.N` (release candidate)

[Unreleased]: https://github.com/moinsen/marvin/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/moinsen/marvin/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/moinsen/marvin/releases/tag/v0.0.1