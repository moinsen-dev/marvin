# Configuration

Customize Marvin's behavior to match your workflow and preferences.

## 📁 **Configuration File Locations**

Marvin looks for configuration in these locations (in order):

1. `./marvin.toml` (project-specific)
2. `~/.config/marvin/config.toml` (user-wide)
3. Environment variables (highest priority)

## ⚙️ **Basic Configuration**

Create a `marvin.toml` file in your project root:

```toml title="marvin.toml"
[general]
# Default output directory for generated tasks
output_dir = "./tasks"

# Log level: DEBUG, INFO, WARNING, ERROR
log_level = "INFO"

# Maximum number of tasks to generate per PRD
max_tasks = 20

[templates]
# Template format: xml, json, markdown
output_format = "xml"

# Custom template directory
template_dir = "./templates"

# Include implementation notes in output
include_notes = true

# Include testing strategy in output
include_tests = true

[analysis]
# Enable codebase analysis
analyze_codebase = true

# Supported file extensions for codebase scanning
file_extensions = [".py", ".js", ".ts", ".java", ".cs", ".go"]

# Directories to exclude from analysis
exclude_dirs = ["node_modules", ".git", "__pycache__", "venv"]

[agents]
# Enable specific analysis agents
enable_document_analysis = true
enable_dependency_resolution = true
enable_template_generation = true

# Custom agent configurations
[agents.document_analysis]
chunk_size = 2000
overlap = 200

[agents.dependency_resolution]
max_depth = 5
include_external = false
```

## 🌍 **Environment Variables**

Override any configuration with environment variables:

```bash
# General settings
export MARVIN_OUTPUT_DIR="./output"
export MARVIN_LOG_LEVEL="DEBUG"
export MARVIN_MAX_TASKS="15"

# Template settings  
export MARVIN_OUTPUT_FORMAT="json"
export MARVIN_TEMPLATE_DIR="./custom-templates"

# Analysis settings
export MARVIN_ANALYZE_CODEBASE="false"
export MARVIN_EXCLUDE_DIRS="node_modules,.git,dist"

# API settings (when using server mode)
export MARVIN_API_HOST="0.0.0.0"
export MARVIN_API_PORT="8000"
export MARVIN_API_CORS_ORIGINS="*"

# External service keys
export MARVIN_OPENAI_API_KEY="your-key-here"
export MARVIN_ANTHROPIC_API_KEY="your-key-here"
```

## 🎨 **Template Customization**

### Custom Output Formats

Create custom templates in your template directory:

=== "XML Template"
    ```xml title="templates/custom-task.xml.j2"
    <?xml version="1.0" encoding="UTF-8"?>
    <coding_task>
      <metadata>
        <id>{{ task.id }}</id>
        <title>{{ task.title }}</title>
        <priority>{{ task.priority }}</priority>
        <company>{{ project.company_name }}</company>
      </metadata>
      
      <description>{{ task.description }}</description>
      
      <requirements>
        {% for req in task.requirements %}
        <requirement>{{ req }}</requirement>
        {% endfor %}
      </requirements>
      
      <!-- Custom sections -->
      <code_style>{{ project.coding_standards }}</code_style>
      <deployment_notes>{{ task.deployment_notes }}</deployment_notes>
    </coding_task>
    ```

=== "JSON Template"
    ```json title="templates/custom-task.json.j2"
    {
      "task": {
        "id": "{{ task.id }}",
        "title": "{{ task.title }}",
        "priority": "{{ task.priority }}",
        "description": "{{ task.description }}",
        "requirements": [
          {% for req in task.requirements %}
          "{{ req }}"{% if not loop.last %},{% endif %}
          {% endfor %}
        ],
        "custom_fields": {
          "company": "{{ project.company_name }}",
          "coding_standards": "{{ project.coding_standards }}",
          "deployment_target": "{{ project.deployment_target }}"
        }
      }
    }
    ```

=== "Markdown Template"
    ```markdown title="templates/custom-task.md.j2"
    # {{ task.title }}
    
    **Priority:** {{ task.priority }}  
    **Estimated Effort:** {{ task.estimated_effort }}
    
    ## Description
    {{ task.description }}
    
    ## Requirements
    {% for req in task.requirements %}
    - {{ req }}
    {% endfor %}
    
    ## Company Standards
    - **Coding Style:** {{ project.coding_standards }}
    - **Testing Framework:** {{ project.testing_framework }}
    - **Deployment Target:** {{ project.deployment_target }}
    
    ## Acceptance Criteria
    {% for criterion in task.acceptance_criteria %}
    - [ ] {{ criterion }}
    {% endfor %}
    ```

### Template Variables

Available variables in templates:

```python
# Task-specific variables
task.id                 # Unique task identifier
task.title             # Task title
task.description       # Detailed description
task.priority          # high, medium, low
task.estimated_effort  # Time estimate
task.requirements      # List of requirements
task.dependencies      # List of dependencies
task.acceptance_criteria # List of criteria
task.implementation_notes # Implementation hints
task.testing_strategy  # Testing approach

# Project-specific variables
project.name           # Project name
project.company_name   # Your company name
project.coding_standards # Coding style guide
project.testing_framework # Test framework
project.deployment_target # Where code deploys
project.tech_stack     # Technologies used

# Codebase analysis results
codebase.architecture  # Detected architecture pattern
codebase.languages     # Programming languages found
codebase.frameworks    # Frameworks detected
codebase.existing_models # Database models found
codebase.api_patterns  # API patterns used
```

## 🔌 **Integration Settings**

### AI Tool Integration

Configure output for specific AI coding assistants:

```toml title="marvin.toml"
[integrations]
# Optimize output for specific AI tools
target_ai_tool = "cursor"  # cursor, windsurf, claude-code, generic

# Include tool-specific hints
include_tool_hints = true

# Tool-specific settings
[integrations.cursor]
include_file_structure = true
include_import_suggestions = true
max_context_length = 8000

[integrations.windsurf]
include_workflow_steps = true
include_git_suggestions = true
max_context_length = 12000

[integrations.claude_code]
include_error_handling = true
include_testing_examples = true
max_context_length = 15000
```

### IDE Integration

For VS Code and other IDEs:

```json title=".vscode/settings.json"
{
  "marvin.outputDir": "./tasks",
  "marvin.autoAnalyze": true,
  "marvin.showPreview": true,
  "files.associations": {
    "*.marvin.xml": "xml",
    "*.marvin.json": "json"
  }
}
```

## 🏢 **Team Configuration**

### Shared Team Settings

Create a team configuration file:

```toml title="team-config.toml"
[team]
name = "Engineering Team"
company = "TechCorp Inc."
coding_standards_url = "https://wiki.company.com/coding-standards"

[project_defaults]
# Standard settings for all projects
output_format = "xml"
include_tests = true
include_notes = true
max_tasks = 25

# Company-specific template variables
[project_defaults.variables]
company_name = "TechCorp Inc."
coding_standards = "Google Style Guide"
testing_framework = "Jest + PyTest"
deployment_target = "AWS ECS"
code_review_process = "GitHub PR + 2 approvals"

[quality_gates]
# Enforce quality standards
min_acceptance_criteria = 3
require_testing_strategy = true
require_dependency_analysis = true
max_task_complexity = "medium"
```

### CI/CD Integration

For automated PRD processing in pipelines:

```yaml title=".github/workflows/process-prds.yml"
name: Process PRDs
on:
  push:
    paths: ['docs/prds/*.md']

jobs:
  generate-tasks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python & Marvin
        run: |
          pip install uv
          uv pip install marvin
          
      - name: Process PRDs
        run: |
          marvin process docs/prds/ --output tasks/ --config team-config.toml
          
      - name: Create PR with tasks
        uses: peter-evans/create-pull-request@v5
        with:
          title: "Auto-generated tasks from PRD updates"
          body: "Generated by Marvin from updated PRDs"
          branch: "auto/marvin-tasks"
```

## 🔍 **Advanced Configuration**

### Custom Agents

Add your own analysis agents:

```toml title="marvin.toml"
[agents.custom]
# Enable custom agents
enable_security_analysis = true
enable_performance_analysis = true
enable_compliance_check = true

[agents.custom.security_analysis]
module = "my_company.agents.security"
class = "SecurityAnalysisAgent"
config = { "severity_threshold" = "medium" }

[agents.custom.performance_analysis]
module = "my_company.agents.performance"
class = "PerformanceAgent"
config = { "target_response_time" = "200ms" }
```

### Database Configuration

For persistent storage of analysis results:

```toml title="marvin.toml"
[database]
# Store analysis results for reuse
enable_persistence = true
connection_string = "sqlite:///./marvin_cache.db"

# Cache settings
cache_prd_analysis = true
cache_codebase_analysis = true
cache_duration_days = 30
```

## 🚨 **Troubleshooting Configuration**

### Common Issues

??? question "Configuration not being loaded"
    **Check:** 
    - File location and naming (`marvin.toml`)
    - File permissions (readable)
    - TOML syntax validity
    
    **Debug:**
    ```bash
    marvin config show  # Display current configuration
    marvin config validate  # Check configuration validity
    ```

??? question "Environment variables not working"
    **Check:**
    - Variable naming (must start with `MARVIN_`)
    - Variable export in current shell
    - Variable precedence (env vars override file config)
    
    **Debug:**
    ```bash
    env | grep MARVIN  # Show Marvin environment variables
    ```

??? question "Custom templates not found"
    **Check:**
    - Template directory path
    - File naming convention (`.j2` extension)
    - Template syntax (Jinja2 format)
    
    **Debug:**
    ```bash
    marvin templates list  # Show available templates
    marvin templates validate  # Check template syntax
    ```

### Configuration Validation

Validate your configuration:

```bash
# Check current configuration
marvin config show

# Validate configuration file
marvin config validate ./marvin.toml

# Test template rendering
marvin templates test ./templates/custom-task.xml.j2

# Dry run with configuration
marvin process example.md --dry-run --config ./marvin.toml
```

## 📚 **Configuration Examples**

### Startup Team
```toml title="startup-config.toml"
[general]
output_dir = "./sprint-tasks"
log_level = "INFO"
max_tasks = 15

[templates]
output_format = "markdown"
include_notes = false  # Keep it simple

[project_defaults.variables]
company_name = "StartupCo"
coding_standards = "Prettier + ESLint"
testing_framework = "Vitest"
deployment_target = "Vercel"
```

### Enterprise Team
```toml title="enterprise-config.toml"
[general]
output_dir = "./generated-tasks"
log_level = "WARNING"
max_tasks = 50

[templates]
output_format = "xml"
include_notes = true
include_tests = true

[quality_gates]
min_acceptance_criteria = 5
require_testing_strategy = true
require_security_review = true

[project_defaults.variables]
company_name = "Enterprise Corp"
coding_standards = "Company Standard v2.1"
testing_framework = "Jest + Cypress + JUnit"
deployment_target = "Kubernetes"
compliance_requirements = "SOX, GDPR, HIPAA"
```

---

**Next:** [Learn about processing different PRD formats →](../user-guide/processing-prds.md)