# Writing Effective PRDs for Marvin

## 🎯 The Foundation of AI-Powered Development

A well-written PRD is the difference between AI generating mediocre code and production-ready solutions. This guide teaches you how to write PRDs that unlock the full potential of AI coding assistants.

## The PRD Transformation

| PRD Quality | AI Output Quality | Development Time | Bug Rate |
|-------------|-------------------|------------------|----------|
| Poor | Generic, incomplete | 2-3 weeks | High |
| Good | Functional, basic | 1 week | Medium |
| **Excellent** | **Production-ready** | **2-3 days** | **Low** |

## 📝 Anatomy of an Effective PRD

### 1. Clear Vision Statement

**❌ Poor:**
```markdown
We need a chat app.
```

**✅ Excellent:**
```markdown
# SecureChat - Enterprise Team Communication Platform

## Vision
A Slack alternative focused on security and compliance for financial institutions,
featuring end-to-end encryption, audit trails, and regulatory compliance tools.

## Target Users
- Financial analysts requiring secure communication
- Compliance officers needing audit trails
- IT administrators managing data sovereignty
```

### 2. Structured Feature Breakdown

**❌ Poor:**
```markdown
- Messages
- Files
- Users
```

**✅ Excellent:**
```markdown
## Core Features

### 1. Secure Messaging
#### Requirements
- End-to-end encryption using Signal protocol
- Message retention policies (30, 90, 365 days)
- Edit/delete with audit trail
- Threading support for conversations
- Rich text formatting (Markdown)
- Code syntax highlighting
- Message search with encryption

#### Constraints
- Messages encrypted at rest
- No message content in logs
- Compliance with GDPR Article 17 (right to erasure)

### 2. File Sharing
#### Requirements  
- File upload up to 100MB
- Automatic virus scanning
- Encryption before storage
- Preview generation for images/PDFs
- Version control for documents
- Expiring download links

#### Technical Specifications
- S3-compatible storage backend
- Client-side encryption before upload
- Thumbnail generation service
- DLP (Data Loss Prevention) scanning
```

### 3. Technical Requirements

**❌ Poor:**
```markdown
Should be fast and secure.
```

**✅ Excellent:**
```markdown
## Technical Requirements

### Performance
- API response time < 200ms (p95)
- Message delivery < 100ms
- Support 10,000 concurrent users
- 99.95% uptime SLA
- Message search < 1 second

### Security
- SOC2 Type II compliance
- HIPAA compliant infrastructure
- Zero-knowledge encryption
- Biometric authentication support
- Hardware security key (FIDO2) support
- IP allowlisting per organization

### Scalability
- Horizontal scaling for API servers
- Read replicas for database
- Multi-region deployment capability
- CDN for static assets
- Message queue for async operations
```

### 4. Specific Acceptance Criteria

**❌ Poor:**
```markdown
It should work well.
```

**✅ Excellent:**
```markdown
## Acceptance Criteria

### User Registration
- [ ] Email verification required within 24 hours
- [ ] Password must meet: 12+ chars, uppercase, lowercase, number, symbol
- [ ] MFA setup prompted after first login
- [ ] Account lockout after 5 failed attempts
- [ ] Password reset requires email + SMS verification

### Message Sending
- [ ] Messages deliver in under 100ms
- [ ] Typing indicators show within 50ms
- [ ] Failed messages retry 3 times with exponential backoff
- [ ] Offline messages queue and send when reconnected
- [ ] Read receipts can be disabled per user

### Compliance
- [ ] All actions logged with timestamp and user ID
- [ ] Audit log retention for 7 years
- [ ] Data export available within 48 hours of request
- [ ] Right to erasure executable within 30 days
- [ ] Compliance dashboard shows real-time status
```

## 🔑 Key Principles for Effective PRDs

### 1. Be Specific, Not Vague

```markdown
❌ "Good error handling"

✅ "Return HTTP 400 for validation errors with field-level details:
{
  'errors': {
    'email': 'Invalid email format',
    'password': 'Must be at least 12 characters'
  }
}"
```

### 2. Include Edge Cases

```markdown
## Edge Cases to Handle

### Concurrent Editing
- When two users edit the same message simultaneously
- Resolution: Last write wins with conflict notification
- Both versions saved in edit history

### Network Interruption  
- Message sending interrupted mid-flight
- Resolution: Client-side retry with idempotency key
- Duplicate prevention on server side

### Storage Quota Exceeded
- User attempts upload beyond quota
- Resolution: Clear error message with upgrade option
- Graceful degradation for essential features
```

### 3. Define Integration Points

```markdown
## External Integrations

### Authentication
- SAML 2.0 for enterprise SSO
- OAuth2 for Google Workspace
- LDAP/AD sync for user provisioning
- SCIM protocol for user lifecycle

### Monitoring
- Prometheus metrics endpoint
- OpenTelemetry tracing
- Structured logs to Elasticsearch
- Error reporting to Sentry

### Compliance
- SIEM integration via syslog
- DLP tool webhooks
- Audit log streaming to Splunk
```

### 4. Specify Data Models

```markdown
## Data Architecture

### User Model
- id: UUID (primary key)
- email: string (unique, encrypted)
- name: string (encrypted) 
- role: enum (admin, user, guest)
- mfa_enabled: boolean
- last_login: timestamp
- created_at: timestamp
- organization_id: UUID (foreign key)

### Message Model  
- id: UUID (primary key)
- content: text (encrypted)
- author_id: UUID (foreign key)
- channel_id: UUID (foreign key)
- thread_id: UUID (nullable)
- edited: boolean
- deleted: boolean
- created_at: timestamp
- updated_at: timestamp

### Indexes
- messages.channel_id, created_at (compound)
- messages.author_id
- users.email (unique)
- users.organization_id
```

## 📋 PRD Templates by Project Type

### SaaS Application PRD Structure
```markdown
1. Executive Summary
2. User Personas & Use Cases
3. Functional Requirements
   - Core Features
   - User Workflows
   - Admin Features
4. Non-Functional Requirements
   - Performance
   - Security
   - Scalability
5. Technical Architecture
6. Data Models
7. API Specifications
8. UI/UX Requirements
9. Testing Strategy
10. Success Metrics
```

### API PRD Structure
```markdown
1. API Overview & Goals
2. Authentication & Authorization
3. Resource Definitions
4. Endpoint Specifications
   - Request/Response Schemas
   - Error Handling
   - Rate Limiting
5. Webhooks & Events
6. Versioning Strategy
7. Performance Requirements
8. Security Considerations
9. Documentation Requirements
10. Client SDK Requirements
```

### Mobile App PRD Structure
```markdown
1. App Vision & Goals
2. Target Platforms & Versions
3. User Journey Maps
4. Screen-by-Screen Specifications
5. Offline Functionality
6. Push Notifications
7. Device Permissions
8. Performance Requirements
9. Security & Privacy
10. App Store Requirements
```

## 🚀 Advanced PRD Techniques

### 1. Scenario-Based Requirements

```markdown
## User Scenarios

### Scenario: First-Time Setup
**Given**: New user with admin role
**When**: They log in for the first time
**Then**: 
1. Show interactive setup wizard
2. Guide through organization settings
3. Prompt to invite team members
4. Configure security policies
5. Set up integrations
6. Show success dashboard

### Scenario: Compliance Audit
**Given**: Compliance officer needs audit trail
**When**: They request report for date range
**Then**:
1. Generate PDF within 30 seconds
2. Include all user actions
3. Highlight policy violations
4. Export in SIEM-compatible format
```

### 2. Progressive Disclosure

```markdown
## Feature Rollout Phases

### Phase 1: MVP (Weeks 1-4)
- Basic messaging
- User authentication
- Simple file sharing

### Phase 2: Enhanced (Weeks 5-8)
- End-to-end encryption
- Advanced search
- Admin dashboard

### Phase 3: Enterprise (Weeks 9-12)
- SSO integration
- Compliance tools
- API access
```

### 3. Constraint Documentation

```markdown
## Constraints & Limitations

### Technical Constraints
- Must run on Kubernetes
- PostgreSQL 14+ required
- Node.js 18+ for backend
- React 18+ for frontend

### Business Constraints
- Budget: $50K for infrastructure/month
- Timeline: MVP in 3 months
- Team: 4 developers, 1 designer

### Regulatory Constraints
- GDPR compliance required
- Data residency in EU
- Financial conduct regulations
```

## ✅ PRD Quality Checklist

Before running Marvin, ensure your PRD includes:

### Completeness
- [ ] Clear vision and goals
- [ ] All user personas defined
- [ ] Complete feature list
- [ ] Technical requirements
- [ ] Performance targets
- [ ] Security requirements

### Specificity
- [ ] Concrete examples for each feature
- [ ] Exact error messages defined
- [ ] Specific UI/UX requirements
- [ ] Precise acceptance criteria
- [ ] Clear data models

### Edge Cases
- [ ] Error scenarios documented
- [ ] Concurrency issues addressed
- [ ] Scale limitations defined
- [ ] Failure recovery specified
- [ ] Migration paths included

### Technical Details
- [ ] API specifications
- [ ] Database schemas
- [ ] Integration points
- [ ] Deployment requirements
- [ ] Monitoring needs

## 💡 Common PRD Mistakes to Avoid

### 1. Assuming Context
**Wrong**: "Implement standard authentication"  
**Right**: "JWT-based auth with 15-minute access tokens, 7-day refresh tokens, stored in httpOnly cookies"

### 2. Missing Dependencies
**Wrong**: "Add payment processing"  
**Right**: "Stripe integration for payments, requiring PCI compliance, webhook handling, and reconciliation system"

### 3. Vague Performance Requirements
**Wrong**: "Should be fast"  
**Right**: "Page load < 2s, API response < 200ms (p95), support 1000 concurrent users"

### 4. Incomplete Error Handling
**Wrong**: "Handle errors appropriately"  
**Right**: "Return specific error codes, log to Sentry, show user-friendly messages, implement retry logic"

## 📊 Real PRD Examples

### Example 1: E-commerce Checkout
[View Full PRD](../examples/ecommerce-checkout-prd.md)

### Example 2: Real-time Analytics Dashboard  
[View Full PRD](../examples/analytics-dashboard-prd.md)

### Example 3: Mobile Banking App
[View Full PRD](../examples/mobile-banking-prd.md)

## 🎯 PRD Writing Workflow

1. **Start with Why**
   - Problem statement
   - User needs
   - Business goals

2. **Define What**
   - Features
   - Requirements
   - Constraints

3. **Specify How**
   - Technical approach
   - Architecture
   - Integrations

4. **Clarify Success**
   - Acceptance criteria
   - Metrics
   - Testing strategy

5. **Review & Refine**
   - Get stakeholder input
   - Add missing details
   - Clarify ambiguities

## 🚀 From PRD to Production

```bash
# 1. Write comprehensive PRD
vim my-feature-prd.md

# 2. Generate tasks with Marvin
marvin process my-feature-prd.md --output ./tasks/

# 3. Review generated tasks
ls -la ./tasks/

# 4. Feed to AI assistant
# Get production-ready code!
```

## 📚 Resources

- [PRD Template Library](../templates/)
- [Industry-Specific PRDs](../examples/industry/)
- [PRD Review Checklist](../guides/prd-review.md)
- [Stakeholder Communication](../guides/stakeholder-prds.md)

---

**Ready to write PRDs that produce exceptional AI-generated code?** Start with our templates and watch your development velocity soar →