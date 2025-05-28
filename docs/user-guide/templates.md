# Understanding Generated Templates

Learn how to interpret and customize Marvin's task templates for maximum AI coding effectiveness.

## 📋 **Template Structure**

Marvin generates structured templates that provide AI coding assistants with comprehensive context. Here's what each section contains:

### **Complete Template Anatomy**

```xml title="Complete Task Template"
<?xml version="1.0" encoding="UTF-8"?>
<coding_task>
  <!-- 🏷️ Metadata: Task identification and management -->
  <metadata>
    <task_id>task_001</task_id>
    <title>User Authentication System</title>
    <priority>high</priority>
    <estimated_effort>4-6 hours</estimated_effort>
    <created_from>auth-feature.md</created_from>
    <created_at>2024-01-15T10:30:00Z</created_at>
  </metadata>
  
  <!-- 🎯 Context: Why this task exists and its business value -->
  <context>
    <description>
      Implement secure user authentication system with JWT tokens,
      password hashing, and session management for the web application.
    </description>
    
    <business_value>
      Enables user account creation, secure login, and personalized
      experiences. Foundation for all user-specific features.
    </business_value>
    
    <user_impact>
      Users can create accounts, log in securely, and maintain
      sessions across browser restarts.
    </user_impact>
  </context>
  
  <!-- ✅ Requirements: What needs to be built -->
  <requirements>
    <functional>
      <requirement>User registration with email and password</requirement>
      <requirement>Secure password hashing using bcrypt</requirement>
      <requirement>JWT token generation and validation</requirement>
      <requirement>Login endpoint with rate limiting</requirement>
      <requirement>Password reset via email</requirement>
      <requirement>User profile management</requirement>
    </functional>
    
    <technical>
      <requirement>RESTful API design following OpenAPI spec</requirement>
      <requirement>Input validation and sanitization</requirement>
      <requirement>Error handling with appropriate HTTP codes</requirement>
      <requirement>Logging for security events</requirement>
      <requirement>Integration with existing database schema</requirement>
    </technical>
    
    <security>
      <requirement>Password complexity enforcement</requirement>
      <requirement>Rate limiting on auth endpoints</requirement>
      <requirement>Secure token storage recommendations</requirement>
      <requirement>Protection against common attacks (CSRF, XSS)</requirement>
    </security>
  </requirements>
  
  <!-- 🔗 Dependencies: What must exist before this task -->
  <dependencies>
    <technical>
      <dependency type="database">User table schema</dependency>
      <dependency type="service">Email service configuration</dependency>
      <dependency type="library">JWT library installation</dependency>
    </technical>
    
    <task>
      <dependency task_id="task_000">Database setup and migrations</dependency>
    </task>
  </dependencies>
  
  <!-- 🎯 Acceptance Criteria: How to know it's done -->
  <acceptance_criteria>
    <criterion>Users can register with valid email/password</criterion>
    <criterion>Login returns valid JWT token</criterion>
    <criterion>Protected routes verify JWT tokens</criterion>
    <criterion>Password reset flow works end-to-end</criterion>
    <criterion>Rate limiting prevents brute force attacks</criterion>
    <criterion>All inputs are properly validated</criterion>
    <criterion>Security logging captures auth events</criterion>
  </acceptance_criteria>
  
  <!-- 💡 Implementation Notes: Best practices and hints -->
  <implementation_notes>
    <note>Use bcrypt with salt rounds of 12 for password hashing</note>
    <note>JWT tokens should expire after 24 hours</note>
    <note>Implement refresh token mechanism for better UX</note>
    <note>Store sensitive config in environment variables</note>
    <note>Consider using middleware for auth route protection</note>
  </implementation_notes>
  
  <!-- 🧪 Testing Strategy: How to verify it works -->
  <testing_strategy>
    <unit_tests>
      <test>Password hashing and verification</test>
      <test>JWT token generation and validation</test>
      <test>Input validation for all fields</test>
      <test>Rate limiting logic</test>
    </unit_tests>
    
    <integration_tests>
      <test>Registration flow end-to-end</test>
      <test>Login flow with database interaction</test>
      <test>Password reset email workflow</test>
      <test>Protected route access with tokens</test>
    </integration_tests>
    
    <security_tests>
      <test>SQL injection attempts on auth endpoints</test>
      <test>Brute force attack simulation</test>
      <test>Token manipulation and validation</test>
    </security_tests>
  </testing_strategy>
  
  <!-- 🏗️ Architecture Hints: Technical guidance -->
  <architecture_hints>
    <pattern>Repository pattern for user data access</pattern>
    <pattern>Service layer for business logic</pattern>
    <pattern>Middleware for authentication checks</pattern>
    <database>Index on email field for fast lookups</database>
    <caching>Cache user sessions for performance</caching>
  </architecture_hints>
</coding_task>
```

---

## 🎯 **Why This Structure Works So Well**

### **AI Coding Assistant Benefits**

=== "🧠 Complete Context"
    **The Problem:** AI tools often lack context about why code exists
    
    **Marvin's Solution:**
    - Business value explanation
    - User impact description  
    - Technical constraints
    - Security considerations
    
    **Result:** AI generates purpose-driven code

=== "📋 Clear Requirements"
    **The Problem:** Ambiguous prompts lead to generic solutions
    
    **Marvin's Solution:**
    - Functional requirements (what it does)
    - Technical requirements (how it works)
    - Security requirements (how it's protected)
    
    **Result:** AI builds exactly what's needed

=== "🔗 Dependency Awareness"
    **The Problem:** AI doesn't know what already exists
    
    **Marvin's Solution:**
    - Technical dependencies listed
    - Related task connections
    - Integration points specified
    
    **Result:** AI builds compatible code

=== "✅ Testable Outcomes"
    **The Problem:** Hard to verify AI-generated code works
    
    **Marvin's Solution:**
    - Specific acceptance criteria
    - Comprehensive testing strategy
    - Security test considerations
    
    **Result:** AI includes proper testing

---

## 🎨 **Template Variations**

### **Output Formats**

Marvin supports multiple output formats for different use cases:

=== "XML (Default)"
    ```xml
    <coding_task>
      <title>Feature Implementation</title>
      <requirements>
        <requirement>Detailed specification</requirement>
      </requirements>
    </coding_task>
    ```
    
    **Best for:** Structured data, complex projects, enterprise use

=== "JSON"
    ```json
    {
      "task": {
        "title": "Feature Implementation",
        "requirements": [
          "Detailed specification"
        ]
      }
    }
    ```
    
    **Best for:** API integration, automation scripts, modern tooling

=== "Markdown"
    ```markdown
    # Feature Implementation
    
    ## Requirements
    - Detailed specification
    
    ## Acceptance Criteria
    - [ ] Criterion 1
    ```
    
    **Best for:** Documentation, GitHub issues, lightweight projects

=== "YAML"
    ```yaml
    task:
      title: "Feature Implementation"
      requirements:
        - "Detailed specification"
      acceptance_criteria:
        - "Criterion 1"
    ```
    
    **Best for:** DevOps workflows, configuration-driven projects

### **Complexity Levels**

Templates adapt to task complexity:

=== "Simple Task"
    ```xml
    <coding_task>
      <title>Add validation to user form</title>
      <requirements>
        <requirement>Email format validation</requirement>
        <requirement>Required field checking</requirement>
      </requirements>
      <acceptance_criteria>
        <criterion>Invalid emails show error</criterion>
        <criterion>Required fields prevent submission</criterion>
      </acceptance_criteria>
    </coding_task>
    ```

=== "Complex Task"
    ```xml
    <coding_task>
      <title>Real-time chat system</title>
      <requirements>
        <functional>
          <requirement>WebSocket connections</requirement>
          <requirement>Message persistence</requirement>
          <requirement>Room management</requirement>
        </functional>
        <technical>
          <requirement>Horizontal scaling support</requirement>
          <requirement>Message encryption</requirement>
          <requirement>Performance monitoring</requirement>
        </technical>
      </requirements>
      <!-- ... extensive details ... -->
    </coding_task>
    ```

---

## 🔧 **Customizing Templates**

### **Custom Template Creation**

Create your own templates to match your workflow:

```xml title="templates/my-custom-task.xml.j2"
<?xml version="1.0" encoding="UTF-8"?>
<{{ company_name|lower }}_task>
  <metadata>
    <id>{{ task.id }}</id>
    <title>{{ task.title }}</title>
    <epic>{{ task.epic }}</epic>
    <sprint>{{ current_sprint }}</sprint>
    <assignee>{{ default_assignee }}</assignee>
  </metadata>
  
  <description>{{ task.description }}</description>
  
  <!-- Company-specific sections -->
  <business_impact>{{ task.business_impact }}</business_impact>
  <risk_assessment>{{ task.risk_level }}</risk_assessment>
  <compliance_notes>{{ task.compliance_requirements }}</compliance_notes>
  
  <requirements>
    {% for req in task.requirements %}
    <requirement priority="{{ req.priority }}">{{ req.text }}</requirement>
    {% endfor %}
  </requirements>
  
  <!-- Custom testing requirements -->
  <testing>
    <unit_test_coverage>{{ company_standards.test_coverage }}%</unit_test_coverage>
    <performance_benchmarks>
      {% for benchmark in task.performance_requirements %}
      <benchmark>{{ benchmark }}</benchmark>
      {% endfor %}
    </performance_benchmarks>
  </testing>
  
  <!-- Deployment considerations -->
  <deployment>
    <environment>{{ target_environment }}</environment>
    <rollback_plan>{{ task.rollback_strategy }}</rollback_plan>
    <monitoring>{{ task.monitoring_requirements }}</monitoring>
  </deployment>
</{{ company_name|lower }}_task>
```

### **Template Variables**

Customize templates with dynamic content:

```toml title="marvin.toml"
[project]
company_name = "TechCorp"
default_assignee = "unassigned" 
current_sprint = "Sprint 23"
target_environment = "staging"

[company_standards]
test_coverage = 85
code_review_required = true
security_scan_required = true

[custom_sections]
include_business_impact = true
include_risk_assessment = true
include_compliance_notes = true
```

### **Conditional Sections**

Show/hide template sections based on task properties:

```xml title="Smart Template with Conditions"
<coding_task>
  <title>{{ task.title }}</title>
  
  {% if task.priority == "high" %}
  <urgency_notes>
    <note>High priority task - coordinate with team lead</note>
    <note>Consider pair programming for faster delivery</note>
  </urgency_notes>
  {% endif %}
  
  {% if task.has_security_requirements %}
  <security_requirements>
    {% for req in task.security_requirements %}
    <requirement>{{ req }}</requirement>
    {% endfor %}
  </security_requirements>
  {% endif %}
  
  {% if task.estimated_effort > "8 hours" %}
  <breakdown_suggestion>
    <note>Consider breaking this task into smaller subtasks</note>
    <note>Implement in phases with intermediate testing</note>
  </breakdown_suggestion>
  {% endif %}
</coding_task>
```

---

## 🚀 **Using Templates with AI Tools**

### **Best Practices for AI Prompts**

=== "❌ Poor AI Prompt"
    ```
    "Build a user authentication system"
    ```
    
    **Problems:**
    - Too vague
    - No context
    - No constraints
    - No testing guidance

=== "✅ Excellent AI Prompt"
    ```
    Please implement this coding task following the XML specification exactly:
    
    [Full XML template content here]
    
    Additional context:
    - This is for a Django REST API project
    - Use the existing User model in models.py
    - Follow our established patterns in auth/views.py
    - Include comprehensive tests as specified
    ```
    
    **Benefits:**
    - Complete context
    - Specific requirements
    - Clear testing strategy
    - Integration guidance

### **AI Tool Optimization**

=== "Cursor Integration"
    ```bash
    # Generate Cursor-optimized templates
    marvin process prd.md --target-ai cursor --output ./tasks/
    ```
    
    **Cursor-specific optimizations:**
    - File structure suggestions
    - Import recommendations  
    - Code context references
    - Maximum 8K context length

=== "Windsurf Integration"
    ```bash
    # Generate Windsurf-optimized templates
    marvin process prd.md --target-ai windsurf --output ./tasks/
    ```
    
    **Windsurf-specific optimizations:**
    - Workflow step breakdown
    - Git commit suggestions
    - Collaboration notes
    - Maximum 12K context length

=== "Claude Code Integration"
    ```bash
    # Generate Claude Code-optimized templates
    marvin process prd.md --target-ai claude-code --output ./tasks/
    ```
    
    **Claude Code-specific optimizations:**
    - Error handling emphasis
    - Testing examples included
    - Documentation generation hints
    - Maximum 15K context length

---

## 📊 **Template Quality Indicators**

### **High-Quality Template Checklist**

✅ **Context & Purpose**
- [ ] Clear business value explanation
- [ ] User impact description
- [ ] Technical context provided

✅ **Requirements Clarity**  
- [ ] Functional requirements are specific
- [ ] Technical constraints are detailed
- [ ] Security considerations included

✅ **Dependency Management**
- [ ] All dependencies identified
- [ ] Task order is logical
- [ ] Integration points specified

✅ **Testability**
- [ ] Acceptance criteria are measurable
- [ ] Testing strategy is comprehensive
- [ ] Security tests included

✅ **Implementation Guidance**
- [ ] Best practices noted
- [ ] Architecture patterns suggested
- [ ] Performance considerations included

### **Quality Metrics**

Marvin tracks template quality:

```json title="Quality Assessment"
{
  "template_quality": {
    "overall_score": 92,
    "completeness": 95,
    "specificity": 89,
    "testability": 94,
    "clarity": 90
  },
  "recommendations": [
    "Add more specific performance requirements",
    "Include error handling scenarios",
    "Consider edge cases in acceptance criteria"
  ],
  "ai_readiness": "excellent"
}
```

---

## 🔍 **Template Analysis Tools**

### **Built-in Analysis**

```bash
# Analyze template quality
marvin analyze-template task_001.xml

# Compare templates
marvin compare-templates task_001.xml task_002.xml

# Validate template structure
marvin validate-template task_001.xml
```

### **Template Metrics**

```bash
$ marvin analyze-template task_001.xml

📊 Template Analysis: task_001.xml

Quality Score: 92/100 (Excellent)

📋 Content Analysis:
   ├── Requirements: 12 (specific and actionable)
   ├── Dependencies: 4 (all identified)
   ├── Acceptance Criteria: 8 (measurable)
   ├── Implementation Notes: 6 (helpful)
   └── Test Coverage: 15 test cases

🎯 AI Readiness: Excellent
   ├── Context completeness: 95%
   ├── Requirement specificity: 89%
   ├── Testability score: 94%
   └── Implementation guidance: 92%

💡 Recommendations:
   ├── Add error handling scenarios
   ├── Include performance benchmarks
   └── Consider mobile-specific requirements

✅ Ready for AI coding assistants!
```

---

## 🚨 **Common Template Issues**

### **Fixing Poor Templates**

??? question "Template is too generic"
    **Problem:** Requirements are vague and non-specific
    
    **Solution:**
    - Include specific metrics and constraints
    - Add technical implementation details
    - Provide concrete examples
    - Use quantifiable acceptance criteria

??? question "Missing context"
    **Problem:** AI doesn't understand the purpose
    
    **Solution:**
    - Add business value explanation
    - Include user impact description
    - Provide technical background
    - Explain integration requirements

??? question "No testing guidance"
    **Problem:** Generated code lacks proper tests
    
    **Solution:**
    - Include comprehensive testing strategy
    - Specify test types needed
    - Add security testing requirements
    - Provide test case examples

### **Template Validation**

```bash
# Check template structure
marvin validate-template task.xml

# Common validation errors:
# ❌ Missing required sections
# ❌ Invalid XML syntax
# ❌ Empty requirement lists
# ❌ Circular dependencies
# ❌ Unmeasurable acceptance criteria
```

---

## 📚 **Template Library**

### **Built-in Templates**

Marvin includes templates for common scenarios:

- **🔐 Authentication Systems** - Login, registration, password reset
- **📊 Data Management** - CRUD operations, APIs, database models  
- **🎨 UI Components** - Forms, tables, modals, responsive layouts
- **⚡ Real-time Features** - WebSockets, notifications, live updates
- **🔌 Integrations** - Third-party APIs, payment systems, email services
- **🧪 Testing Infrastructure** - Unit tests, integration tests, E2E tests

### **Community Templates**

Share and discover templates:

```bash
# Browse community templates
marvin templates browse

# Install community template
marvin templates install auth-system-advanced

# Share your template
marvin templates publish my-custom-template
```

---

**Next:** [CLI Usage Guide →](cli-usage.md)