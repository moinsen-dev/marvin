# Quick Start: Your First PRD-to-Tasks Transformation

Get Marvin working in under 5 minutes and see the magic of automated task generation!

## 🚀 **What You'll Accomplish**

By the end of this guide, you'll have:

- ✅ Installed Marvin on your system
- ✅ Processed a real PRD into AI-ready tasks  
- ✅ Seen the power of structured, dependency-aware task generation
- ✅ Ready to use the output with your AI coding assistant

**Time Required:** 5 minutes

---

## 📋 **Prerequisites**

Make sure you have:

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **uv package manager** - [Install guide](https://docs.astral.sh/uv/getting-started/installation/)
- **Git** - [Download here](https://git-scm.com/downloads)

---

## 🛠️ **Step 1: Install Marvin**

=== "macOS/Linux"
    ```bash
    # Clone the repository
    git clone https://github.com/moinsen-dev/marvin.git
    cd marvin
    
    # Create virtual environment and install
    uv venv
    source .venv/bin/activate
    uv pip install -e .
    
    # Verify installation
    marvin --version
    ```

=== "Windows"
    ```powershell
    # Clone the repository
    git clone https://github.com/moinsen-dev/marvin.git
    cd marvin
    
    # Create virtual environment and install
    uv venv
    .venv\Scripts\activate
    uv pip install -e .
    
    # Verify installation
    marvin --version
    ```

!!! success "✅ Installation Complete!"
    You should see Marvin's version number. If not, check the [Installation Troubleshooting](installation.md#troubleshooting).

---

## 📄 **Step 2: Create Your First PRD**

Let's start with a real-world example. Create a file called `social-feed.md`:

```markdown title="social-feed.md"
# Social Media Feed Feature

## Product Overview
We need to build a social media feed that allows users to post updates, 
like content, and comment on posts in real-time.

## Core Requirements

### User Posts
- Users can create text posts (max 280 characters)
- Posts support image attachments (PNG, JPG)
- Posts have timestamps and author information
- Users can edit their own posts within 5 minutes

### Engagement Features  
- Like/unlike posts with real-time counter updates
- Comment on posts with threaded replies
- Share posts with other users
- Real-time notifications for interactions

### Feed Display
- Chronological feed of posts from followed users
- Infinite scroll pagination
- Real-time updates when new posts are available
- Filter options (all posts, friends only, trending)

## Technical Requirements
- RESTful API backend
- Real-time updates via WebSocket
- Mobile-responsive design
- Database optimization for fast feed generation
- Content moderation hooks

## Acceptance Criteria
- [ ] Users can create and edit posts
- [ ] Real-time like counters work correctly
- [ ] Comments display in threaded format
- [ ] Feed loads quickly (< 2 seconds)
- [ ] Mobile layout works on all screen sizes
- [ ] Notifications appear instantly
```

---

## ⚡ **Step 3: Transform with Marvin**

Now let's see Marvin in action:

```bash
# Process the PRD
marvin process social-feed.md --output ./tasks/

# Check what was generated
ls -la ./tasks/
```

**Expected Output:**
```
./tasks/
├── task_001_user_posts_data_model.xml
├── task_002_user_posts_api_endpoints.xml  
├── task_003_post_creation_ui.xml
├── task_004_engagement_system.xml
├── task_005_real_time_updates.xml
├── task_006_feed_display_logic.xml
├── task_007_mobile_responsive_design.xml
└── task_summary.json
```

---

## 🔍 **Step 4: Examine the Generated Tasks**

Let's look at one of the generated tasks:

<details>
<summary>**📋 Click to see: task_001_user_posts_data_model.xml**</summary>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<coding_task>
  <metadata>
    <task_id>task_001</task_id>
    <title>User Posts Data Model Implementation</title>
    <priority>high</priority>
    <estimated_effort>3-4 hours</estimated_effort>
    <created_from>social-feed.md</created_from>
  </metadata>
  
  <context>
    <description>
      Implement the core data model for user posts in the social media feed.
      This includes the database schema, model classes, and basic validation
      for post creation and management.
    </description>
    
    <business_value>
      Foundation for all post-related functionality. Must handle text content,
      image attachments, timestamps, and author relationships efficiently.
    </business_value>
  </context>
  
  <requirements>
    <functional>
      <requirement>Post model with text content (280 char limit)</requirement>
      <requirement>Image attachment support (PNG, JPG formats)</requirement>
      <requirement>Author relationship to User model</requirement>
      <requirement>Created/updated timestamp tracking</requirement>
      <requirement>Edit window validation (5 minute limit)</requirement>
    </functional>
    
    <technical>
      <requirement>Database migration scripts</requirement>
      <requirement>Model validation and constraints</requirement>
      <requirement>Efficient indexing for feed queries</requirement>
      <requirement>Image upload and storage handling</requirement>
    </technical>
  </requirements>
  
  <dependencies>
    <dependency type="model">User authentication system</dependency>
    <dependency type="infrastructure">Database setup</dependency>
    <dependency type="service">File storage service</dependency>
  </dependencies>
  
  <acceptance_criteria>
    <criterion>Posts can be created with text content up to 280 characters</criterion>
    <criterion>Image attachments are properly validated and stored</criterion>
    <criterion>Author information is correctly associated</criterion>
    <criterion>Edit window enforcement works (5 minutes)</criterion>
    <criterion>Database queries are optimized for feed performance</criterion>
    <criterion>All model validations prevent invalid data</criterion>
  </acceptance_criteria>
  
  <implementation_notes>
    <note>Consider using a composite index on (author_id, created_at) for feed queries</note>
    <note>Implement soft delete for posts to maintain data integrity</note>
    <note>Use database-level constraints for character limits</note>
    <note>Consider image processing pipeline for different sizes</note>
  </implementation_notes>
  
  <testing_strategy>
    <test_case>Valid post creation with text only</test_case>
    <test_case>Valid post creation with image attachment</test_case>
    <test_case>Character limit enforcement (280 chars)</test_case>
    <test_case>Edit window validation after 5 minutes</test_case>
    <test_case>Invalid image format rejection</test_case>
    <test_case>Database constraint violations</test_case>
  </testing_strategy>
</coding_task>
```

</details>

**🤯 Look at that detail!** Marvin automatically:

- ✅ **Broke down requirements** into specific, actionable tasks
- ✅ **Identified dependencies** between different components
- ✅ **Provided technical context** for better AI understanding
- ✅ **Included testing strategy** for comprehensive coverage
- ✅ **Added implementation notes** with best practices

---

## 🤖 **Step 5: Use with Your AI Coding Assistant**

Now you're ready to supercharge your development with AI tools!

=== "Cursor"
    ```bash
    # Copy the task content
    cat tasks/task_001_user_posts_data_model.xml
    
    # Paste into Cursor with this prompt:
    # "Implement this task following the specifications exactly"
    ```

=== "Windsurf"
    ```bash
    # Open the task file in Windsurf
    windsurf tasks/task_001_user_posts_data_model.xml
    
    # Use the task content as your AI prompt
    ```

=== "Claude Code"
    ```bash
    # Share the task with Claude Code:
    # "Please implement the following coding task: [paste XML content]"
    ```

### 🎯 **Pro Tips for AI Integration**

!!! tip "Get Better AI Results"
    
    **Perfect Prompt Formula:**
    ```
    Please implement this coding task following the XML specification exactly:
    
    [Paste the entire XML task here]
    
    Additional context:
    - Use [your preferred framework/language]
    - Follow [your coding standards]
    - Include comprehensive tests
    ```

!!! success "Why This Works So Well"
    
    - **Structured Context**: AI gets all the information it needs
    - **Clear Requirements**: No ambiguity about what to build
    - **Dependency Awareness**: AI understands what needs to exist first
    - **Testing Strategy**: AI can write tests alongside code
    - **Implementation Notes**: AI follows best practices automatically

---

## 📈 **Step 6: See the Results**

Here's what you can expect when using Marvin-generated tasks with AI:

### ❌ **Before Marvin (Typical AI Prompt)**
```
"Build a social media feed with posts, likes, and comments"
```

**AI Output:** Generic code, missing edge cases, no tests, unclear structure

### ✅ **After Marvin (Structured Task)**
```xml
<coding_task>
  <title>User Posts Data Model Implementation</title>
  <requirements>
    <requirement>Post model with text content (280 char limit)</requirement>
    <!-- ... detailed specifications ... -->
  </requirements>
</coding_task>
```

**AI Output:** Production-ready code, comprehensive tests, proper validation, optimized queries!

---

## 🚀 **Next Steps**

Congratulations! You've successfully used Marvin to transform a PRD into AI-ready tasks. Here's what to explore next:

<div class="next-steps" markdown>

### 📚 **Dive Deeper**
- [Processing Different PRD Formats](../user-guide/processing-prds.md)
- [Understanding Template Structure](../user-guide/templates.md)
- [Advanced CLI Usage](../user-guide/cli-usage.md)

### 🛠️ **Advanced Features**
- [Codebase Analysis Integration](../user-guide/cli-usage.md#codebase-analysis)
- [Custom Template Configuration](../user-guide/templates.md#customization)
- [API Server for Team Workflows](../user-guide/api-usage.md)

### 🎯 **Real-World Examples**
- [E-commerce Platform PRD](../examples/ecommerce-platform.md)
- [Dashboard Analytics System](../examples/dashboard-analytics.md)
- [User Authentication Flow](../examples/auth-system.md)

</div>

---

## 💡 **Pro Tips for Maximum Impact**

<div class="pro-tips" markdown>

### 🎯 **Writing Better PRDs for Marvin**

!!! tip "Structure Your PRDs"
    
    **Include These Sections:**
    - Clear feature overview
    - Detailed requirements with specifics
    - Technical constraints
    - Acceptance criteria
    - User stories or scenarios

### ⚡ **Optimizing AI Results**

!!! success "Best Practices"
    
    1. **Use the full XML task** - don't just copy the title
    2. **Add your project context** - mention your tech stack
    3. **Reference existing code** - help AI understand your patterns
    4. **Iterate on outputs** - refine tasks based on results

### 🔄 **Iterative Development**

!!! info "Continuous Improvement"
    
    - Start with one task at a time
    - Build dependencies first (follow task order)
    - Test each component before moving on
    - Use task acceptance criteria for validation

</div>

---

## 🤝 **Join the Community**

You're now part of the Marvin ecosystem! Connect with other users:

- 💬 **[Discord Community](https://discord.gg/marvin)** - Get help and share examples
- 🐙 **[GitHub Repository](https://github.com/moinsen-dev/marvin)** - Report issues and contribute
- 🐦 **[Twitter Updates](https://twitter.com/marvin_tool)** - Latest tips and features

---

## ❓ **Having Issues?**

<div class="troubleshooting" markdown>

### Common Problems

??? question "Tasks seem too generic"
    **Solution:** Add more detail to your PRD. Include specific technical requirements, constraints, and examples.

??? question "Dependencies are unclear"
    **Solution:** Use `marvin process --codebase ./src` to analyze your existing code structure.

??? question "AI doesn't understand the context"
    **Solution:** Include the full XML task AND add project-specific context in your prompt.

### Get Help

- 📖 **[Troubleshooting Guide](../troubleshooting.md)**
- 💬 **[Discord Support](https://discord.gg/marvin)**
- 🐙 **[GitHub Issues](https://github.com/moinsen-dev/marvin/issues)**

</div>

**Ready to transform your development workflow? [Explore more features →](../user-guide/cli-usage.md)**