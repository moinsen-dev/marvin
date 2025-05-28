# CLI Usage Guide

Master Marvin's command-line interface for efficient PRD processing and task generation.

## 🚀 **Quick Reference**

```bash
# Basic usage
marvin process <prd-file> [options]

# Common patterns
marvin process feature.md --output ./tasks/
marvin process *.md --codebase ./src/ --output ./tasks/
marvin process prds/ --recursive --format json
```

## 📋 **Core Commands**

### **`marvin process`** - Convert PRDs to Tasks

The main command for processing Product Requirement Documents:

```bash
marvin process [PRD_FILES] [OPTIONS]
```

#### **Basic Examples**

=== "Single File"
    ```bash
    # Process one PRD file
    marvin process user-auth.md
    
    # With custom output directory
    marvin process user-auth.md --output ./auth-tasks/
    ```

=== "Multiple Files"
    ```bash
    # Process multiple files
    marvin process auth.md dashboard.md settings.md
    
    # Using wildcards
    marvin process *.md
    marvin process prds/feature-*.md
    ```

=== "Directory Processing"
    ```bash
    # Process all files in directory
    marvin process ./prds/
    
    # Recursive processing
    marvin process ./docs/ --recursive
    
    # With file filtering
    marvin process ./docs/ --include "*.md" --include "*.txt"
    ```

#### **Advanced Options**

```bash
marvin process feature.md \
  --output ./tasks/ \
  --codebase ./src/ \
  --format xml \
  --config ./team-config.toml \
  --max-tasks 15 \
  --verbose
```

### **Options Reference**

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output directory for generated tasks | `--output ./tasks/` |
| `--codebase` | `-c` | Path to existing codebase for analysis | `--codebase ./src/` |
| `--format` | `-f` | Output format (xml, json, markdown, yaml) | `--format json` |
| `--config` | | Custom configuration file | `--config ./marvin.toml` |
| `--max-tasks` | | Maximum number of tasks to generate | `--max-tasks 20` |
| `--recursive` | `-r` | Process directories recursively | `--recursive` |
| `--include` | | Include files matching pattern | `--include "*.md"` |
| `--exclude` | | Exclude files matching pattern | `--exclude "*draft*"` |
| `--dry-run` | | Preview output without creating files | `--dry-run` |
| `--verbose` | `-v` | Enable detailed output | `--verbose` |
| `--quiet` | `-q` | Suppress non-error output | `--quiet` |

---

## 🔧 **Configuration Commands**

### **`marvin config`** - Manage Configuration

```bash
# Show current configuration
marvin config show

# Show configuration from specific file
marvin config show --file ./team-config.toml

# Validate configuration
marvin config validate

# Initialize new configuration
marvin config init --interactive
```

#### **Configuration Examples**

=== "View Configuration"
    ```bash
    $ marvin config show
    
    📋 Current Configuration:
    
    [general]
    output_dir = "./tasks"
    log_level = "INFO"
    max_tasks = 20
    
    [templates]
    output_format = "xml"
    include_notes = true
    include_tests = true
    
    [analysis]
    analyze_codebase = true
    file_extensions = [".py", ".js", ".ts"]
    ```

=== "Interactive Setup"
    ```bash
    $ marvin config init --interactive
    
    🔧 Marvin Configuration Setup
    
    Project name: My Awesome Project
    Company name: TechCorp Inc.
    Default output directory [./tasks]: ./generated-tasks
    Output format [xml]: json
    Include implementation notes? [Y/n]: Y
    Enable codebase analysis? [Y/n]: Y
    
    ✅ Configuration saved to ./marvin.toml
    ```

---

## 🔍 **Analysis Commands**

### **`marvin analyze`** - Detailed Analysis

Get insights without generating tasks:

```bash
# Analyze PRD structure
marvin analyze feature.md --type prd

# Analyze codebase
marvin analyze ./src/ --type codebase

# Combined analysis
marvin analyze feature.md --codebase ./src/ --type combined
```

#### **Analysis Types**

=== "PRD Analysis"
    ```bash
    $ marvin analyze social-feed.md --type prd
    
    📄 PRD Analysis: social-feed.md
    
    📊 Structure Analysis:
       ├── Sections found: 6
       ├── Requirements: 12 functional, 5 technical
       ├── User stories: 8
       ├── Acceptance criteria: 15
       └── Technical constraints: 7
    
    🎯 Feature Breakdown:
       ├── User Posts (complexity: medium)
       ├── Engagement System (complexity: high)
       ├── Real-time Updates (complexity: high)
       └── Feed Display (complexity: medium)
    
    ⚡ Estimated Effort: 18-24 hours
    📈 Recommended Tasks: 6-8
    ```

=== "Codebase Analysis"
    ```bash
    $ marvin analyze ./src/ --type codebase
    
    🏗️  Codebase Analysis: ./src/
    
    📁 Project Structure:
       ├── Architecture: Django REST API
       ├── Language: Python 3.11
       ├── Framework: Django 4.2, DRF 3.14
       ├── Database: PostgreSQL (detected)
       └── Testing: PyTest, Factory Boy
    
    📦 Components Found:
       ├── Models: 12 (User, Post, Comment, etc.)
       ├── Views: 8 API viewsets
       ├── Serializers: 15
       ├── Tests: 45 test files
       └── Migrations: 23
    
    🔗 API Patterns:
       ├── REST endpoints follow /api/v1/ pattern
       ├── Token authentication in use
       ├── Pagination with PageNumberPagination
       └── Custom permission classes
    ```

### **`marvin dependencies`** - Dependency Analysis

Understand task relationships:

```bash
# Show task dependencies
marvin dependencies ./tasks/

# Visualize dependency graph
marvin dependencies ./tasks/ --graph --output deps.svg

# Check for circular dependencies
marvin dependencies ./tasks/ --check-circular
```

```bash
$ marvin dependencies ./tasks/

🔗 Task Dependencies Analysis

📋 Dependency Graph:
   task_001_data_model
   ├── No dependencies
   └── Required by: task_002, task_003
   
   task_002_api_endpoints  
   ├── Depends on: task_001_data_model
   └── Required by: task_004, task_005
   
   task_003_user_interface
   ├── Depends on: task_001_data_model
   └── Required by: task_005
   
   task_004_real_time_updates
   ├── Depends on: task_002_api_endpoints
   └── Required by: None
   
   task_005_integration
   ├── Depends on: task_002_api_endpoints, task_003_user_interface
   └── Required by: None

⚡ Recommended Order:
   1. task_001_data_model
   2. task_002_api_endpoints, task_003_user_interface (parallel)
   3. task_004_real_time_updates
   4. task_005_integration

✅ No circular dependencies found
```

---

## 🎨 **Template Commands**

### **`marvin templates`** - Template Management

```bash
# List available templates
marvin templates list

# Show template details
marvin templates show auth-system

# Validate custom template
marvin templates validate ./my-template.xml.j2

# Test template rendering
marvin templates test ./my-template.xml.j2 --data ./test-data.json
```

#### **Template Operations**

=== "List Templates"
    ```bash
    $ marvin templates list
    
    📋 Available Templates:
    
    Built-in Templates:
    ├── 🔐 auth-system-basic (User authentication)
    ├── 🔐 auth-system-advanced (OAuth, 2FA, etc.)
    ├── 📊 crud-api (REST API with CRUD operations)
    ├── 🎨 react-component (React component with tests)
    ├── ⚡ websocket-feature (Real-time functionality)
    └── 🧪 testing-suite (Comprehensive test setup)
    
    Custom Templates (./templates/):
    ├── 🏢 company-task-template
    └── 🚀 startup-task-template
    ```

=== "Template Testing"
    ```bash
    $ marvin templates test ./custom-template.xml.j2 --data test-data.json
    
    🧪 Template Test: custom-template.xml.j2
    
    ✅ Syntax valid
    ✅ All variables resolved
    ✅ Output structure correct
    
    📄 Rendered Output:
    <?xml version="1.0" encoding="UTF-8"?>
    <coding_task>
      <title>User Authentication System</title>
      <!-- ... rendered content ... -->
    </coding_task>
    ```

---

## 🔧 **Utility Commands**

### **`marvin validate`** - Validation Tools

```bash
# Validate PRD structure
marvin validate prd feature.md

# Validate generated tasks
marvin validate tasks ./tasks/

# Validate configuration
marvin validate config ./marvin.toml
```

### **`marvin stats`** - Project Statistics

```bash
# Show project statistics
marvin stats ./tasks/

# Detailed breakdown
marvin stats ./tasks/ --detailed

# Export statistics
marvin stats ./tasks/ --export stats.json
```

```bash
$ marvin stats ./tasks/ --detailed

📊 Project Statistics

📋 Task Overview:
   ├── Total tasks: 8
   ├── High priority: 3
   ├── Medium priority: 4
   ├── Low priority: 1
   └── Total estimated effort: 24-32 hours

🏷️  Task Categories:
   ├── Backend API: 4 tasks (12-16 hours)
   ├── Frontend UI: 3 tasks (8-12 hours)
   └── Testing: 1 task (4 hours)

🔗 Dependencies:
   ├── Independent tasks: 2
   ├── Tasks with dependencies: 6
   ├── Maximum dependency depth: 3
   └── Parallel execution opportunities: 4

📈 Complexity Distribution:
   ├── Simple: 2 tasks
   ├── Medium: 4 tasks
   └── Complex: 2 tasks
```

### **`marvin export`** - Export Tools

```bash
# Export to different formats
marvin export ./tasks/ --format json --output tasks.json
marvin export ./tasks/ --format csv --output tasks.csv

# Export for project management tools
marvin export ./tasks/ --format jira --output jira-import.json
marvin export ./tasks/ --format trello --output trello-import.json
```

---

## 🚀 **Workflow Examples**

### **Daily Development Workflow**

```bash
# 1. Morning: Process new requirements
marvin process new-feature.md --codebase ./src/ --output ./today-tasks/

# 2. Review generated tasks
marvin stats ./today-tasks/ --detailed

# 3. Check dependencies
marvin dependencies ./today-tasks/ --graph

# 4. Start development with first task
cat ./today-tasks/task_001_*.xml
# Copy content to AI coding assistant

# 5. Validate completed work
marvin validate tasks ./today-tasks/
```

### **Team Collaboration Workflow**

```bash
# 1. Process PRDs with team config
marvin process ./prds/ --config ./team-config.toml --output ./sprint-tasks/

# 2. Generate team statistics
marvin stats ./sprint-tasks/ --export team-stats.json

# 3. Export for project management
marvin export ./sprint-tasks/ --format jira --output sprint-import.json

# 4. Validate all tasks meet standards
marvin validate tasks ./sprint-tasks/ --strict
```

### **CI/CD Integration Workflow**

```bash
#!/bin/bash
# .github/workflows/process-prds.sh

# Process any new or updated PRDs
changed_prds=$(git diff --name-only HEAD~1 HEAD | grep "\.md$")

if [ ! -z "$changed_prds" ]; then
  echo "Processing changed PRDs: $changed_prds"
  
  # Process with team configuration
  marvin process $changed_prds \
    --config ./team-config.toml \
    --codebase ./src/ \
    --output ./generated-tasks/ \
    --format json
  
  # Validate output
  marvin validate tasks ./generated-tasks/
  
  # Generate statistics
  marvin stats ./generated-tasks/ --export task-stats.json
  
  # Create PR with generated tasks
  git add ./generated-tasks/
  git commit -m "Auto-generated tasks from PRD updates"
fi
```

---

## 🔍 **Debugging and Troubleshooting**

### **Verbose Mode**

```bash
# Enable detailed logging
marvin process feature.md --verbose

# Debug-level logging
marvin process feature.md --log-level DEBUG

# Save logs to file
marvin process feature.md --verbose --log-file marvin.log
```

### **Dry Run Mode**

```bash
# Preview what would be generated
marvin process feature.md --dry-run

# Show analysis without creating files
marvin process feature.md --dry-run --verbose
```

### **Common Issues and Solutions**

??? question "Command not found: marvin"
    **Problem:** Marvin not in PATH or not installed properly
    
    **Solution:**
    ```bash
    # Check installation
    which marvin
    pip list | grep marvin
    
    # Reinstall if needed
    uv pip install -e .
    
    # Check virtual environment
    which python
    ```

??? question "No tasks generated"
    **Problem:** PRD format not recognized or empty requirements
    
    **Solution:**
    ```bash
    # Use verbose mode to see parsing details
    marvin process feature.md --verbose
    
    # Validate PRD structure
    marvin validate prd feature.md
    
    # Check file encoding
    file feature.md
    ```

??? question "Tasks are too generic"
    **Problem:** PRD lacks detail or codebase analysis disabled
    
    **Solution:**
    ```bash
    # Include codebase analysis
    marvin process feature.md --codebase ./src/
    
    # Use custom configuration
    marvin process feature.md --config ./detailed-config.toml
    
    # Analyze PRD quality first
    marvin analyze feature.md --type prd
    ```

### **Performance Optimization**

```bash
# Fast processing for large projects
marvin process ./prds/ \
  --exclude "*draft*" \
  --exclude "*template*" \
  --max-tasks 10 \
  --parallel

# Cache codebase analysis
marvin process feature.md \
  --codebase ./src/ \
  --cache-analysis \
  --cache-duration 24h
```

---

## 📚 **Advanced Usage**

### **Environment Variables**

```bash
# Set defaults via environment
export MARVIN_OUTPUT_DIR="./tasks"
export MARVIN_LOG_LEVEL="INFO"
export MARVIN_MAX_TASKS="15"

# Then run without flags
marvin process feature.md
```

### **Shell Completion**

```bash
# Enable shell completion
marvin --install-completion

# For bash
marvin --install-completion bash

# For zsh
marvin --install-completion zsh
```

### **Aliases and Shortcuts**

```bash
# Add to your shell profile
alias mp="marvin process"
alias ma="marvin analyze"
alias ms="marvin stats"

# Usage
mp feature.md -o ./tasks/ -c ./src/
ma feature.md --type prd
ms ./tasks/ --detailed
```

---

**Next:** [API Usage Guide →](api-usage.md)