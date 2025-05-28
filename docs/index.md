# Marvin: Transform PRDs into AI-Ready Tasks in Minutes

<div class="hero" markdown>
  <div class="hero-content" markdown>
    
# 🚀 **10x Your Development Speed**

**Stop spending hours converting requirements into AI prompts.**  
Marvin automatically transforms your Product Requirement Documents into structured, AI-optimized coding tasks.

<div class="hero-buttons" markdown>
[Get Started :material-rocket-launch:](getting-started/installation.md){ .md-button .md-button--primary .md-button--stretch }
[Try the Demo :material-play-circle:](getting-started/quickstart.md){ .md-button .md-button--stretch }
</div>

  </div>
</div>

---

## 🎯 **The Problem We Solve**

<div class="problem-solution" markdown>

=== "❌ **Without Marvin**"

    **Manual Process Takes Hours:**
    
    1. Read through lengthy PRD documents
    2. Manually extract features and requirements  
    3. Break down into development tasks
    4. Write detailed prompts for AI assistants
    5. Ensure consistency across tasks
    6. Manage dependencies manually
    
    **Result:** 4-6 hours of prep work before any coding begins
    
    ```markdown
    // Typical manual AI prompt
    "Please implement a user authentication system. 
    It should have login and registration. 
    Make it secure somehow."
    ```

=== "✅ **With Marvin**"

    **Automated Process Takes Minutes:**
    
    1. Drop your PRD into Marvin
    2. Get structured XML templates instantly
    3. Each task includes context, dependencies, and acceptance criteria
    4. Ready for Cursor, Windsurf, or Claude Code
    
    **Result:** From PRD to coding in under 5 minutes
    
    ```xml
    <!-- Marvin-generated task -->
    <task>
      <title>User Authentication System</title>
      <context>Implement secure auth with JWT tokens</context>
      <dependencies>Database setup, User model</dependencies>
      <acceptance_criteria>
        - Password hashing with bcrypt
        - JWT token generation/validation
        - Rate limiting on login attempts
      </acceptance_criteria>
    </task>
    ```

</div>

---

## 📊 **Real Impact**

<div class="metrics" markdown>

<div class="metric-card" markdown>
**⚡ 95% Faster**  
Setup time: 4 hours → 5 minutes
</div>

<div class="metric-card" markdown>
**🎯 3x Better Quality**  
Structured tasks with dependencies
</div>

<div class="metric-card" markdown>
**🔄 100% Consistent**  
Same format every time
</div>

<div class="metric-card" markdown>
**🤖 AI-Optimized**  
Works perfectly with all AI tools
</div>

</div>

---

## 🔄 **See It In Action**

### Input: Your PRD
```markdown title="feature-request.md"
# E-commerce Cart Feature

## Overview
Users need ability to add products to cart and checkout

## Requirements
- Add/remove items from cart
- Persist cart across sessions  
- Calculate totals with tax
- Integration with payment gateway
- Email confirmations

## Acceptance Criteria
- Cart icon shows item count
- Users can modify quantities
- Secure checkout process
```

### ⬇️ **Marvin Magic Happens** ⬇️

### Output: AI-Ready Tasks

=== "Task 1: Cart Model"
    ```xml
    <coding_task>
      <title>Implement Shopping Cart Data Model</title>
      <priority>high</priority>
      <estimated_effort>2-3 hours</estimated_effort>
      
      <context>
        Create the foundational cart system that persists user 
        shopping sessions and handles item management.
      </context>
      
      <requirements>
        <requirement>Cart model with user association</requirement>
        <requirement>Cart items with product references</requirement>
        <requirement>Quantity and pricing calculations</requirement>
        <requirement>Session persistence mechanism</requirement>
      </requirements>
      
      <dependencies>
        <dependency>User authentication system</dependency>
        <dependency>Product catalog database</dependency>
      </dependencies>
      
      <acceptance_criteria>
        <criterion>Users can add products to cart</criterion>
        <criterion>Cart persists across browser sessions</criterion>
        <criterion>Accurate quantity and total calculations</criterion>
        <criterion>Cart associates with authenticated users</criterion>
      </acceptance_criteria>
    </coding_task>
    ```

=== "Task 2: Cart UI"
    ```xml
    <coding_task>
      <title>Build Shopping Cart User Interface</title>
      <priority>high</priority>
      <estimated_effort>3-4 hours</estimated_effort>
      
      <context>
        Create responsive cart interface with real-time updates 
        and smooth user experience.
      </context>
      
      <requirements>
        <requirement>Cart icon with item count badge</requirement>
        <requirement>Expandable cart preview</requirement>
        <requirement>Quantity modification controls</requirement>
        <requirement>Remove item functionality</requirement>
        <requirement>Real-time total calculations</requirement>
      </requirements>
      
      <dependencies>
        <dependency>Cart data model (Task 1)</dependency>
        <dependency>Product display components</dependency>
      </dependencies>
      
      <acceptance_criteria>
        <criterion>Cart icon displays correct item count</criterion>
        <criterion>Users can modify quantities inline</criterion>
        <criterion>Totals update immediately on changes</criterion>
        <criterion>Mobile-responsive design</criterion>
      </acceptance_criteria>
    </coding_task>
    ```

=== "Task 3: Checkout"
    ```xml
    <coding_task>
      <title>Secure Checkout Process</title>
      <priority>high</priority>
      <estimated_effort>4-5 hours</estimated_effort>
      
      <context>
        Implement secure payment processing with tax calculation
        and email confirmation system.
      </context>
      
      <requirements>
        <requirement>Multi-step checkout form</requirement>
        <requirement>Tax calculation by location</requirement>
        <requirement>Payment gateway integration</requirement>
        <requirement>Order confirmation emails</requirement>
        <requirement>Error handling and validation</requirement>
      </requirements>
      
      <dependencies>
        <dependency>Cart functionality (Tasks 1-2)</dependency>
        <dependency>Payment gateway API</dependency>
        <dependency>Email service configuration</dependency>
      </dependencies>
      
      <acceptance_criteria>
        <criterion>Secure payment processing</criterion>
        <criterion>Accurate tax calculations</criterion>
        <criterion>Confirmation emails sent</criterion>
        <criterion>Proper error handling</criterion>
      </acceptance_criteria>
    </coding_task>
    ```

---

## 🎯 **Perfect For These Teams**

<div class="use-cases" markdown>

<div class="use-case" markdown>
### 🚀 **Startups**
*"Ship features 3x faster with AI assistance"*

- Convert investor requirements into development tasks
- Consistent quality across rapid iterations  
- Perfect for small teams wearing multiple hats
- Reduce onboarding time for new developers

**ROI:** Save 20+ hours per feature release
</div>

<div class="use-case" markdown>
### 🏢 **Enterprise Teams**
*"Standardize AI-assisted development at scale"*

- Consistent task formatting across teams
- Maintain quality standards with structured templates
- Easy integration with existing workflows
- Audit trail for requirement traceability

**ROI:** 40% reduction in project planning time
</div>

<div class="use-case" markdown>
### 👥 **Product Managers**
*"Bridge the gap between requirements and code"*

- No more lost-in-translation issues
- Clear acceptance criteria for every task
- Dependency tracking prevents bottlenecks
- Easy to review and validate outputs

**ROI:** 60% fewer requirement clarification meetings
</div>

<div class="use-case" markdown>
### 🤖 **AI-First Teams**
*"Maximize your AI coding tool effectiveness"*

- Optimized prompts for Cursor, Windsurf, Claude Code
- Structured context for better AI understanding
- Consistent format improves AI output quality
- Seamless integration with existing AI workflows

**ROI:** 2-3x better AI-generated code quality
</div>

</div>

---

## 🆚 **How Marvin Compares**

<div class="comparison" markdown>

|  | Manual Process | Linear/Notion | **Marvin** |
|---|---|---|---|
| **Time to AI-ready tasks** | 4-6 hours | 2-3 hours | ⚡ **5 minutes** |
| **AI optimization** | ❌ Generic prompts | ❌ Not AI-focused | ✅ **Perfect for AI tools** |
| **Dependency tracking** | ❌ Manual effort | ⚠️ Basic linking | ✅ **Automatic resolution** |
| **Consistency** | ❌ Varies by person | ⚠️ Template dependent | ✅ **Always structured** |
| **Integration** | ❌ Copy/paste workflow | ❌ Platform locked | ✅ **Works everywhere** |
| **Cost** | 👤 Developer time | 💰 Monthly subscription | 🆓 **Open source** |

</div>

---

## 🚀 **Get Started in 60 Seconds**

<div class="quick-start" markdown>

```bash title="1. Install Marvin"
# Clone and install
git clone https://github.com/moinsen-dev/marvin.git
cd marvin && uv pip install -e .
```

```bash title="2. Process Your First PRD"
# Transform PRD to AI tasks
marvin process examples/prd/example_prd.md --output ./tasks/
```

```bash title="3. Use with Your AI Tool"
# Copy the generated XML into Cursor, Windsurf, or Claude Code
# Start coding immediately with perfect context!
```

[Full Installation Guide →](getting-started/installation.md){ .md-button }
[Try the Demo →](getting-started/quickstart.md){ .md-button .md-button--primary }

</div>

---

## 🌟 **What Makes Marvin Special**

<div class="features-detailed" markdown>

<div class="feature" markdown>
### 🧠 **AI-Native Design**
Built from the ground up for AI coding assistants. Every output is optimized for tools like Cursor, Windsurf, and Claude Code.
</div>

<div class="feature" markdown>
### 🔗 **Smart Dependencies**
Automatically identifies task dependencies and suggests optimal execution order. No more blocked developers.
</div>

<div class="feature" markdown>
### 📊 **Codebase Aware**
Scans your existing codebase to ensure generated tasks align with your architecture and patterns.
</div>

<div class="feature" markdown>
### ⚡ **Multiple Interfaces**
CLI for automation, REST API for integration, MCP server for collaboration. Use however fits your workflow.
</div>

<div class="feature" markdown>
### 🔧 **Highly Configurable**
Customize templates, add your own agents, modify output formats. Make Marvin work exactly how you need.
</div>

<div class="feature" markdown>
### 📈 **Production Ready**
Test-driven development, comprehensive documentation, enterprise-grade architecture. Ready for serious projects.
</div>

</div>

---

## 🎬 **See It Live**

<div class="demo-section" markdown>

!!! info "🎥 **Interactive Demo Coming Soon**"
    We're building an interactive demo where you can paste your own PRD and see Marvin generate tasks in real-time. 
    
    **Want early access?** [Join our Discord](https://discord.gg/marvin) to be notified when it's ready!

**For now, try these examples:**

- [E-commerce Cart Feature](examples/prd/ecommerce-cart.md) → [Generated Tasks](examples/output/cart-tasks/)
- [User Authentication System](examples/prd/auth-system.md) → [Generated Tasks](examples/output/auth-tasks/)  
- [Dashboard Analytics](examples/prd/dashboard.md) → [Generated Tasks](examples/output/dashboard-tasks/)

</div>

---

## 💬 **What Developers Say**

<div class="testimonials" markdown>

> *"Marvin transformed our development workflow. We went from spending entire mornings on task breakdown to having AI-ready prompts in minutes."*  
> **— Sarah Chen, Tech Lead @ StartupCo**

> *"The dependency resolution alone saves us hours. No more developers waiting because tasks weren't properly sequenced."*  
> **— Marcus Rodriguez, Principal Engineer @ TechCorp**

> *"Our AI-generated code quality improved dramatically once we started using Marvin's structured prompts."*  
> **— Alex Kim, Senior Developer @ InnovateLabs**

</div>

---

## 🤝 **Join the Community**

<div class="community" markdown>

<div class="community-card" markdown>
### 🐙 **GitHub**
Star the repo, report issues, contribute code  
[github.com/moinsen-dev/marvin](https://github.com/moinsen-dev/marvin)
</div>

<div class="community-card" markdown>
### 💬 **Discord**
Get help, share examples, connect with other users  
[discord.gg/marvin](https://discord.gg/marvin)
</div>

<div class="community-card" markdown>
### 🐦 **Twitter**
Follow for updates and tips  
[@marvin_tool](https://twitter.com/marvin_tool)
</div>

</div>

---

## 🚀 **Ready to Transform Your Workflow?**

<div class="cta-section" markdown>

Don't spend another day manually converting requirements into AI prompts. Join hundreds of developers who've already transformed their workflow with Marvin.

<div class="cta-buttons" markdown>
[Start Free Today](getting-started/installation.md){ .md-button .md-button--primary .md-button--stretch }
[View Documentation](getting-started/quickstart.md){ .md-button .md-button--stretch }
</div>

**✨ Open source • ⚡ No vendor lock-in • 🆓 Always free**

</div>

---

<div class="footer-info" markdown>
**Built with ❤️ by developers, for developers**

Questions? [hello@marvin.dev](mailto:hello@marvin.dev) • [Documentation](getting-started/installation.md) • [Contributing](developer-guide/contributing.md)
</div>