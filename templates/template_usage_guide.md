# AI Coding Task Template v2.0 – Usage Guide

> **Purpose**  This guide explains **when, why, and how** to fill out the XML template `coding_task_template_v2.xml` so that any AI coding assistant (e.g., OpenAI Codex, Claude Code) can tackle one bite‑sized engineering task at a time. The approach embraces an *incremental* delivery model: you provide **one numbered XML file per task**, the assistant completes it, then you hand it the next file that builds on the previous outcome.

---

## 1  Quick‑Start Checklist

1. **Copy** `coding_task_template_v2.xml` into your project's `/ai-tasks/` folder.
2. **Rename** it using a two‑digit sequence prefix, e.g. `01_frontend_setup.xml`.
3. **Complete** the mandatory blocks below (⚑ marks required fields).
4. **Run** the file through your chosen AI coding tool.
5. **Review & merge** the generated PR / changes.
6. **Fork** the next copy, bump the sequence number (`02_…`, `03_…`) and update `<SequenceInfo>` → `<DependsOn>`.
7. **Repeat** until the feature set is finished.

---

## 2  File‑Naming & Sequencing Convention

| Purpose          | File‑name pattern         | Key XML fields                       |
| ---------------- | ------------------------- | ------------------------------------ |
| Initial scaffold | `01_<area>_init.xml`      | `SequenceNumber=1`, `DependsOn=""`   |
| Next incremental | `02_<area>_<feature>.xml` | `SequenceNumber=2`, `DependsOn="01"` |
| Fix or refactor  | `03_<area>_refactor.xml`  | `SequenceNumber=3`, `DependsOn="02"` |

*Tip:* Match the prefix to your Git branch naming: `feature/02_auth_api`.

---

## 3  Template Block‑by‑Block

### 3.1  `<SequenceInfo>` (⚑)

| Field              | Description                                  | Example       |
| ------------------ | -------------------------------------------- | ------------- |
| `<TaskID>`         | Short unique slug (kebab‑case)               | `auth-api-v1` |
| `<SequenceNumber>` | **Ascending integer** – determines run order | `2`           |
| `<DependsOn>`      | Comma‑separated list of prior TaskIDs        | `ui-scaffold` |

### 3.2  `<Metadata>` (⚑)

Provide author, date (ISO‑8601), and template version.  Helps traceability.

### 3.3  `<Context>`

Business, stakeholders, assumptions, risks, dependencies, constraints.

### 3.4  `<TechnologyStack>`

Languages, frameworks, package managers, DBs, cloud, containerization.

### 3.5  `<Architecture>`

Architecture pattern, ADR links, domain model.

### 3.6  `<Task>` (⚑)

* `TaskName` – imperative verb phrase.
* `UserStories` – INVEST‑compliant stories.
* `Scope` – in/out.
* `AffectedComponents` – list of files & folders.

### 3.7  `<ExpectedOutcome>` (⚑)

Functional + non‑functional requirements and acceptance criteria.

### 3.8  `<Implementation>`

Security, API contract, testing, CI/CD, observability, migrations.

### 3.9  `<References>` & `<Deliverables>`

Link existing code, docs, external resources; checklist & timeframe.

### 3.10  `<Glossary>`

Define project‑specific acronyms to cut ambiguity.

---

## 4  End‑to‑End Example

**Task 01 – `01_ui_scaffold.xml`**

```xml
<SequenceInfo>
  <TaskID>ui-scaffold</TaskID>
  <SequenceNumber>1</SequenceNumber>
  <DependsOn></DependsOn>
</SequenceInfo>
<!-- … rest of template filled … -->
```

*Outcome:* basic React + Tailwind UI renders locally.

**Task 02 – `02_auth_api.xml`**

```xml
<SequenceInfo>
  <TaskID>auth-api-v1</TaskID>
  <SequenceNumber>2</SequenceNumber>
  <DependsOn>ui-scaffold</DependsOn>
</SequenceInfo>
<!-- … implement JWT auth API … -->
```

*Outcome:* backend endpoints for sign‑up / login, no UI wiring yet.

**Task 03 – `03_ui_auth_integration.xml`**
Depends on both previous TaskIDs; merges UI and API.

---

## 5  Best Practices

* **One concern per task** – keep tasks ≤ 250 LOC diff.
* **Increment steadily** – never skip sequence numbers.
* **Validate** the XML against an XSD (optional sample provided).
* **Automate** schema linting and pull‑request creation.
* **Archive** completed tasks to `/ai-tasks/archive/`.

---

## 6  FAQ

**Q: How large can each XML file be?**  → Stay under \~3000 tokens to avoid truncation.

**Q: Can tasks run in parallel?**  → Yes, use different sequence series (`01-A`, `01-B`) and avoid overlaps in `<DependsOn>`.

**Q: How do I handle rollbacks?**  → Create a *reversal* task (`99_revert_<id>.xml`) that depends on the failed TaskID.

---

© 2025 Your Company – Licensed under CC BY‑SA 4.0
