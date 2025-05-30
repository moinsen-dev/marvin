# Marvin Refactoring - Domain-Driven Design

## Overview
This document describes the major refactoring of Marvin from the problematic Google ADK implementation to a clean domain-driven architecture.

## Problems with the Original Implementation
1. **ADK Integration Issues**: The Google ADK agents were not properly implemented
2. **No Business Logic**: Agents had no actual processing logic
3. **Poor Separation of Concerns**: Mixed infrastructure with domain logic
4. **Hard to Test**: ADK runners made unit testing difficult
5. **Limited Flexibility**: Tied to ADK's agent framework

## New Architecture

### Domain Layer (`core/domain/`)
**Entities** - Core business objects with behavior:
- `PRDDocument`: Represents a product requirements document
- `FeatureSpecification`: Individual features with requirements
- `TaskDefinition`: AI coding tasks with context
- `CodebaseAnalysis`: Analyzed codebase structure
- `AnalysisResult`: Complete analysis output

**Value Objects** - Immutable domain concepts:
- `XMLTemplate`: Structured task templates
- `TaskPriority`: Priority levels with validation
- `TimeEstimate`: Time estimates with conversions

**Domain Services** - Business logic:
- `PRDAnalyzer`: Extracts features from PRD content
- `CodebaseScanner`: Analyzes project structure
- `TaskSequencer`: Creates optimal task sequences
- `TemplateGenerator`: Generates XML templates

### Infrastructure Layer (`infrastructure/`)
- `GeminiClient`: Direct integration with Gemini API
- `AIService`: Abstract interface for AI providers
- Structured prompts for each AI operation

### Application Layer (`core/application/`)
- `ProcessPRDUseCase`: Main workflow orchestration
- Clear use case boundaries
- Dependency injection ready

## Benefits of the New Architecture

1. **Clean Separation**: Domain logic is isolated from infrastructure
2. **Testable**: Each component can be tested independently
3. **Flexible**: Easy to swap AI providers or add new ones
4. **Maintainable**: Clear boundaries and responsibilities
5. **Performant**: Direct API calls without ADK overhead

## Migration Guide

### Old Way (ADK):
```python
from marvin.agents.main_agent import main_agent_runner
# Complex ADK runner setup
```

### New Way (Domain-Driven):
```python
from marvin.agents.main_agent import process_prd
result = process_prd(prd_path, codebase_path, output_dir)
```

## Next Steps

1. **Complete Implementation**:
   - Add missing method implementations in domain services
   - Implement proper error handling
   - Add retry logic for AI calls

2. **Testing**:
   - Unit tests for all domain entities
   - Integration tests for use cases
   - Mock AI service for testing

3. **Enhancement**:
   - Add more sophisticated PRD parsing
   - Implement caching for AI responses
   - Add progress tracking

4. **Documentation**:
   - Update API documentation
   - Create developer guide
   - Add more examples

## Example Usage

```bash
# Process a PRD with the new architecture
marvin process examples/sample_prd.md --output ./output

# The system will:
# 1. Parse the PRD using domain services
# 2. Use Gemini AI to enhance analysis
# 3. Generate optimal task sequences
# 4. Create XML templates for each task
# 5. Save results to the output directory
```

## Technical Details

### Gemini Integration
- Uses `gemini-2.0-flash-exp` for fast operations
- Uses `gemini-1.5-pro` for complex analysis
- Structured JSON prompts for consistency
- Proper error handling and parsing

### Task Sequencing
- Topological sort for dependencies
- Complexity estimation
- Context-aware task generation
- Support for various task types

### Template Generation
- XML format for AI assistants
- Includes metadata and context
- Acceptance criteria
- File modification hints

This refactoring sets a solid foundation for Marvin's future development!
