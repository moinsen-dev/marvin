# Processing PRDs

Learn how to convert your Product Requirement Documents into AI-ready coding tasks with Marvin.

## 📋 **Supported PRD Formats**

Marvin can process PRDs in various formats:

### ✅ **Markdown (.md)**
Most common format, excellent structure support:

```markdown title="feature-request.md"
# Feature Name

## Overview
Brief description of the feature

## Requirements
- Functional requirement 1
- Functional requirement 2

## Technical Constraints
- Performance requirements
- Security considerations

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

### ✅ **Plain Text (.txt)**
Simple format, good for quick notes:

```text title="feature-request.txt"
Feature: User Authentication

Requirements:
- Login with email/password
- Password reset functionality
- Session management
- Two-factor authentication

Technical:
- JWT tokens
- BCrypt password hashing
- Rate limiting
```

### ✅ **Rich Text (.rtf)**
Formatted documents from word processors:

```rtf
{\rtf1\ansi\deff0 {\fonttbl {\f0 Times New Roman;}}
\f0\fs24 Feature: Dashboard Analytics\par
Requirements:\par
- Real-time data visualization\par
- Export capabilities\par
}
```

### ✅ **Microsoft Word (.docx)**
Corporate standard format:

- Full formatting support
- Tables and lists preserved
- Images and diagrams extracted
- Comments and tracked changes processed

---

## 🎯 **PRD Quality Guidelines**

### **Excellent PRD Structure**

```markdown title="excellent-prd.md"
# Feature Name: Real-time Chat System

## Business Context
Why this feature matters and its expected impact.

## User Stories
- As a user, I want to send messages instantly
- As a moderator, I need to monitor chat content
- As an admin, I want to manage chat rooms

## Functional Requirements
### Core Messaging
- Send/receive text messages in real-time
- Support for emoji and basic formatting
- Message history persistence (30 days)
- Typing indicators

### Room Management  
- Create public/private chat rooms
- Invite users to private rooms
- Room moderation controls
- User presence indicators

## Technical Requirements
- WebSocket connections for real-time updates
- Message encryption in transit
- Database optimization for message history
- Rate limiting (10 messages/minute per user)
- Mobile-responsive design

## Non-Functional Requirements
- Response time: < 100ms for message delivery
- Concurrent users: Support 10,000 simultaneous connections
- Uptime: 99.9% availability
- Scalability: Horizontal scaling support

## Security Considerations
- Message content encryption
- User authentication required
- Anti-spam mechanisms
- Content moderation hooks

## Acceptance Criteria
- [ ] Users can join/leave rooms instantly
- [ ] Messages appear in real-time (< 100ms)
- [ ] Message history loads quickly (< 2s)
- [ ] Typing indicators work correctly
- [ ] Rate limiting prevents spam
- [ ] Mobile layout works on all devices
- [ ] Encrypted message transmission
```

### **What Makes This Excellent:**

✅ **Clear Structure** - Easy to parse sections
✅ **Specific Requirements** - Detailed, measurable criteria  
✅ **Technical Details** - Performance and security specs
✅ **User Perspective** - Stories explain the "why"
✅ **Acceptance Criteria** - Testable outcomes

---

## 🚀 **Processing Commands**

### **Basic Processing**

```bash
# Process single PRD
marvin process feature-request.md

# Specify output directory
marvin process feature-request.md --output ./tasks/

# Process multiple PRDs
marvin process *.md --output ./all-tasks/
```

### **Advanced Processing**

```bash
# Include codebase analysis
marvin process feature-request.md --codebase ./src/ --output ./tasks/

# Use custom configuration
marvin process feature-request.md --config ./team-config.toml

# Specify output format
marvin process feature-request.md --format json --output ./tasks/

# Dry run (no files created)
marvin process feature-request.md --dry-run --verbose
```

### **Batch Processing**

```bash
# Process all PRDs in directory
marvin process ./prds/ --output ./tasks/ --recursive

# Process specific file types
marvin process ./docs/ --include "*.md" --include "*.txt" --output ./tasks/

# Exclude certain files
marvin process ./docs/ --exclude "*draft*" --exclude "*template*"
```

---

## 📊 **Understanding Analysis Output**

When you process a PRD, Marvin provides detailed analysis:

### **Console Output**
```bash
$ marvin process social-feed.md --output ./tasks/

🔍 Analyzing PRD: social-feed.md
📋 Extracted 12 requirements across 4 feature areas
🔗 Identified 7 task dependencies
⚡ Generated 6 optimized tasks
📁 Output saved to: ./tasks/

📈 Analysis Summary:
   ├── Features identified: 4
   ├── Technical requirements: 8  
   ├── Business requirements: 4
   ├── Tasks generated: 6
   ├── Dependencies resolved: 7
   └── Estimated total effort: 18-24 hours

📋 Generated Tasks:
   ├── task_001_user_posts_data_model.xml (4h)
   ├── task_002_engagement_system.xml (3h)
   ├── task_003_real_time_updates.xml (5h)
   ├── task_004_feed_display_logic.xml (4h)
   ├── task_005_mobile_responsive_design.xml (2h)
   └── task_summary.json

✅ Ready for AI coding assistants!
```

### **Summary File**
Marvin generates a `task_summary.json` with analysis details:

```json title="task_summary.json"
{
  "prd_analysis": {
    "source_file": "social-feed.md",
    "processed_at": "2024-01-15T10:30:00Z",
    "total_features": 4,
    "total_requirements": 12,
    "estimated_effort": "18-24 hours"
  },
  "tasks": [
    {
      "id": "task_001",
      "title": "User Posts Data Model",
      "priority": "high",
      "effort": "3-4 hours",
      "dependencies": ["user_auth", "database_setup"]
    }
  ],
  "dependency_graph": {
    "task_001": [],
    "task_002": ["task_001"],
    "task_003": ["task_001", "task_002"]
  },
  "recommendations": [
    "Implement tasks in dependency order",
    "Consider API rate limiting for engagement features",
    "Optimize database queries for feed performance"
  ]
}
```

---

## 🔧 **Codebase Integration**

### **Analyzing Existing Code**

When you include `--codebase`, Marvin analyzes your existing code structure:

```bash
marvin process new-feature.md --codebase ./src/ --output ./tasks/
```

**What Marvin Analyzes:**
- 🏗️ **Architecture patterns** (MVC, microservices, etc.)
- 📁 **File structure** and organization
- 🔌 **Frameworks and libraries** in use
- 🗃️ **Database models** and schemas
- 🛠️ **API patterns** and conventions
- 🧪 **Testing approaches** and frameworks

### **Enhanced Task Generation**

With codebase analysis, tasks become more specific:

```xml title="Without codebase analysis"
<requirement>Create user authentication API</requirement>
```

```xml title="With codebase analysis"
<requirement>
  Extend existing FastAPI auth module at src/auth/
  following the established JWT pattern used in 
  src/auth/models.py and src/auth/routes.py
</requirement>
```

### **Architecture Alignment**

Marvin ensures new tasks fit your existing architecture:

!!! example "Django Project Detection"
    ```xml
    <implementation_notes>
      <note>Use Django models extending AbstractUser</note>
      <note>Follow existing serializer patterns in api/serializers/</note>
      <note>Add tests to tests/test_auth.py following pytest conventions</note>
      <note>Use Django REST framework viewsets for consistency</note>
    </implementation_notes>
    ```

!!! example "React Project Detection"
    ```xml
    <implementation_notes>
      <note>Create components in src/components/ following existing structure</note>
      <note>Use existing Redux store pattern for state management</note>
      <note>Follow TypeScript interfaces defined in src/types/</note>
      <note>Add tests using existing Jest + React Testing Library setup</note>
    </implementation_notes>
    ```

---

## 📈 **Optimization Tips**

### **Better Requirements = Better Tasks**

=== "❌ Vague Requirements"
    ```markdown
    ## Requirements
    - Users should be able to interact with content
    - The system should be fast
    - Make it secure
    ```
    
    **Result:** Generic, non-actionable tasks

=== "✅ Specific Requirements"
    ```markdown
    ## Requirements
    - Users can like posts with real-time counter updates
    - Feed loads in < 2 seconds for 1000+ posts
    - All API endpoints require JWT authentication
    - Rate limiting: 100 requests/minute per user
    ```
    
    **Result:** Detailed, implementation-ready tasks

### **Include Context and Constraints**

```markdown
## Technical Constraints
- Must integrate with existing PostgreSQL database
- Frontend uses React 18+ with TypeScript
- Backend API follows OpenAPI 3.0 specification
- All changes must maintain backward compatibility
- Performance budget: < 200ms API response time

## Business Constraints  
- Feature must launch before Q2 deadline
- Budget allows for 40 development hours
- Must support 10,000 concurrent users
- Compliance with GDPR requirements
```

### **Effective User Stories**

```markdown
## User Stories

### Primary Users (End Customers)
- As a shopper, I want to save items for later so I can purchase them when ready
- As a return customer, I want my cart to persist across devices
- As a mobile user, I want the cart to work seamlessly on my phone

### Secondary Users (Business Stakeholders)
- As a product manager, I need cart abandonment analytics
- As a marketing team member, I want to send cart reminder emails
- As a customer service rep, I need to view customer cart contents

### System Stories (Technical)
- As the system, I need to sync cart data across user sessions
- As the database, I need efficient queries for cart retrieval
- As the API, I need to handle concurrent cart modifications
```

---

## 🚨 **Common Issues and Solutions**

### **Poor Task Generation**

??? question "Tasks are too generic"
    **Problem:** PRD lacks specific details
    
    **Solution:**
    - Add technical constraints and requirements
    - Include specific metrics and performance criteria
    - Provide examples of desired behavior
    - Specify integration points with existing systems

??? question "Missing dependencies"
    **Problem:** Tasks seem disconnected
    
    **Solution:**
    - Use `--codebase` flag to analyze existing code
    - Include system architecture in PRD
    - Specify data flow and component interactions
    - Add integration requirements

??? question "Wrong technology assumptions"
    **Problem:** Tasks suggest wrong frameworks
    
    **Solution:**
    - Include current tech stack in PRD
    - Use `--codebase` analysis
    - Add technical constraints section
    - Specify required tools and frameworks

### **Processing Errors**

??? question "Unable to parse PRD"
    **Problem:** File format or encoding issues
    
    **Solution:**
    ```bash
    # Check file encoding
    file social-feed.md
    
    # Convert if needed
    iconv -f ISO-8859-1 -t UTF-8 input.md > output.md
    
    # Use verbose mode for debugging
    marvin process input.md --verbose
    ```

??? question "Empty or minimal output"
    **Problem:** PRD doesn't contain enough structured information
    
    **Solution:**
    - Ensure PRD has clear headings and sections
    - Add more detailed requirements
    - Include acceptance criteria
    - Use markdown formatting for better parsing

---

## 📚 **Best Practices Summary**

### ✅ **Do This**
- Use clear, descriptive headings
- Include specific, measurable requirements
- Add technical constraints and performance criteria
- Provide user stories for context
- Include acceptance criteria
- Use bullet points and lists for clarity
- Analyze your codebase with `--codebase` flag

### ❌ **Avoid This**
- Vague or generic requirements
- Missing technical details
- No acceptance criteria
- Unclear business context
- Mixing multiple features in one PRD
- Inconsistent formatting
- Ignoring existing code architecture

---

**Next:** [Understanding Generated Templates →](templates.md)