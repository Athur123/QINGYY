---
title: Project Cleanup Roadmap
module: system
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# Project Cleanup Roadmap

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Consolidate the recent repository reorganization so the Qingyang HRO prototype repo is easier to navigate, safer to collaborate in, and less likely to drift between prototypes, specs, plans, and local agent setup.

**Architecture:** Keep the current 7-module structure as the stable source of truth. Focus first on closing reorganization leftovers, then normalize documentation and local-config handling, then improve long-term maintainability with lightweight module indexes and ownership rules.

**Tech Stack:** Static HTML, CSS/SCSS, Markdown docs, Git, local Claude/Codex agent config

---

### Task 1: Close Reorganization Leftovers

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/CLAUDE.md`
- Modify: `/Users/athur/PycharmProjects/qyy/AGENTS.md`
- Modify: `/Users/athur/PycharmProjects/qyy/docs/CODE_WIKI.md`
- Review: `/Users/athur/PycharmProjects/qyy/prototype/`
- Review: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/`
- Review: `/Users/athur/PycharmProjects/qyy/docs/superpowers/plans/`

- [ ] **Step 1: Write the failing checklist**

Create a short checklist in your notes with these failure conditions:

```text
FAIL if any top-level doc still references old flat prototype paths
FAIL if any top-level doc still references date-prefixed spec/plan names as the primary pattern
FAIL if any top-level doc still describes screenshots or local config in a way that conflicts with .gitignore
```

- [ ] **Step 2: Run repo text search to verify failures exist or not**

Run: `rg -n "prototype/[^<]*qingyang-|2026-|screenshots|\\.claude/settings.local.json|\\.codex/config.toml|\\.agents/skills" /Users/athur/PycharmProjects/qyy/CLAUDE.md /Users/athur/PycharmProjects/qyy/AGENTS.md /Users/athur/PycharmProjects/qyy/docs/CODE_WIKI.md`

Expected: Any outdated references are visible and can be corrected in place.

- [ ] **Step 3: Normalize top-level documentation**

Update the docs so they consistently say:

```text
- Prototypes live under prototype/<module>/
- Specs live under docs/superpowers/specs/<module>/
- Plans live under docs/superpowers/plans/<module>/
- Screenshots belong in screenshots/ and are gitignored
- Local agent config is machine-local and not for commit
```

- [ ] **Step 4: Re-run the search to verify consistency**

Run: `rg -n "prototype/[^<]*qingyang-|\\.Codex|settings.local.json|screenshots|prototype/<module>|docs/superpowers/specs/<module>|docs/superpowers/plans/<module>" /Users/athur/PycharmProjects/qyy/CLAUDE.md /Users/athur/PycharmProjects/qyy/AGENTS.md /Users/athur/PycharmProjects/qyy/docs/CODE_WIKI.md`

Expected: No stale `.Codex` references; remaining hits should reflect the current module-based structure.

- [ ] **Step 5: Commit**

```bash
git add CLAUDE.md AGENTS.md docs/CODE_WIKI.md
git commit -m "docs: align top-level docs with module-based repo structure"
```

### Task 2: Formalize Local Config Safety

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/.gitignore`
- Create: `/Users/athur/PycharmProjects/qyy/.claude/settings.local.example.json`
- Create: `/Users/athur/PycharmProjects/qyy/.codex/config.example.toml`
- Modify: `/Users/athur/PycharmProjects/qyy/CLAUDE.md`
- Modify: `/Users/athur/PycharmProjects/qyy/AGENTS.md`

- [ ] **Step 1: Write the failing checklist**

Use this failure definition:

```text
FAIL if a new collaborator cannot discover required env keys without seeing real credentials
FAIL if docs mention local config files but no safe template exists
FAIL if .gitignore protects local config but repo gives no setup example
```

- [ ] **Step 2: Verify templates are missing**

Run: `find /Users/athur/PycharmProjects/qyy/.claude /Users/athur/PycharmProjects/qyy/.codex -maxdepth 1 \\( -name '*.example.*' -o -name 'config.example.toml' \\)`

Expected: No example templates found, confirming the gap.

- [ ] **Step 3: Create safe templates with redacted placeholders**

Create example files with the same required keys but placeholder values, for example:

```json
{
  "env": {
    "QINGYANG_TENANT": "your-tenant",
    "QINGYANG_USERNAME": "your-username",
    "QINGYANG_PASSWORD": "your-password",
    "QINGYANG_LOGIN_URL": "https://qingyangyun.com.cn/#/login"
  }
}
```

```toml
[shell_environment_policy]
inherit = "core"

[shell_environment_policy.set]
QINGYANG_LOGIN_URL = "https://qingyangyun.com.cn/#/login"
QINGYANG_TENANT = "your-tenant"
QINGYANG_USERNAME = "your-username"
QINGYANG_PASSWORD = "your-password"
```

- [ ] **Step 4: Point docs to the templates**

Update top-level docs to say real values belong only in:

```text
.claude/settings.local.json
.codex/config.toml
```

And setup examples live in:

```text
.claude/settings.local.example.json
.codex/config.example.toml
```

- [ ] **Step 5: Verify the safe setup path**

Run: `rg -n "example|your-tenant|your-username|your-password|settings.local.example.json|config.example.toml" /Users/athur/PycharmProjects/qyy/.claude /Users/athur/PycharmProjects/qyy/.codex /Users/athur/PycharmProjects/qyy/CLAUDE.md /Users/athur/PycharmProjects/qyy/AGENTS.md`

Expected: Example files and setup instructions are discoverable without exposing secrets.

- [ ] **Step 6: Commit**

```bash
git add .gitignore .claude/settings.local.example.json .codex/config.example.toml CLAUDE.md AGENTS.md
git commit -m "chore: add safe local config templates for agent setup"
```

### Task 3: Decide What Is First-Class vs Local-Only

**Files:**
- Review: `/Users/athur/PycharmProjects/qyy/.agents/`
- Review: `/Users/athur/PycharmProjects/qyy/scripts/`
- Review: `/Users/athur/PycharmProjects/qyy/docs/CODE_WIKI.md`
- Review: `/Users/athur/PycharmProjects/qyy/fix_indent.py`
- Review: `/Users/athur/PycharmProjects/qyy/update_html.py`

- [ ] **Step 1: Write the classification checklist**

Classify each untracked item into one of:

```text
A = first-class project asset that should be committed
B = local tooling artifact that should stay untracked
C = obsolete file that should be deleted
```

- [ ] **Step 2: Capture the current candidates**

Run: `git status --short | sed -n '1,120p'`

Expected: You can clearly see current untracked candidates such as `.agents/`, `docs/CODE_WIKI.md`, `scripts/`, `fix_indent.py`, and `update_html.py`.

- [ ] **Step 3: Apply the decision rule**

Use this rule:

```text
Commit if the file helps another collaborator understand, run, or maintain the repo.
Ignore if the file only helps one local machine.
Delete if it duplicates replaced structure or has no documented role.
```

- [ ] **Step 4: Update ignore rules or docs based on the decision**

If an item becomes first-class, document it in `CLAUDE.md` / `AGENTS.md`.
If an item stays local-only, add or refine `.gitignore`.
If an item is obsolete, remove it intentionally.

- [ ] **Step 5: Verify there is no ambiguous residue**

Run: `git status --short`

Expected: The remaining untracked items should be intentional and easy to explain.

- [ ] **Step 6: Commit**

```bash
git add .gitignore CLAUDE.md AGENTS.md docs/CODE_WIKI.md scripts .agents
git commit -m "chore: classify repo support files and local-only artifacts"
```

### Task 4: Add Lightweight Module Indexes

**Files:**
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/calculator/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/employee/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/settlement/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/insurance-config/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/approval/README.md`
- Create: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/system/README.md`

- [ ] **Step 1: Write the failing checklist**

Use this failure definition:

```text
FAIL if a new collaborator cannot tell which page is primary for a module
FAIL if a module contains multiple specs with no obvious reading order
FAIL if current/legacy/exploration pages are mixed without explanation
```

- [ ] **Step 2: Verify README indexes do not already exist**

Run: `find /Users/athur/PycharmProjects/qyy/docs/superpowers/specs -maxdepth 2 -name 'README.md'`

Expected: No module README indexes found.

- [ ] **Step 3: Create one README per module**

Each README should include:

```markdown
# <Module> Index

- Primary prototype page(s)
- Main spec(s)
- Main plan(s)
- Legacy / exploration pages
- Current recommended entry point
```

- [ ] **Step 4: Verify discoverability**

Run: `find /Users/athur/PycharmProjects/qyy/docs/superpowers/specs -maxdepth 2 -name 'README.md' | sort`

Expected: All 7 module indexes exist.

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/specs/*/README.md
git commit -m "docs: add module index readmes for prototype and spec navigation"
```

### Task 5: Stabilize the Reconciliation Module as the Reference Standard

**Files:**
- Review: `/Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html`
- Review: `/Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html`
- Review: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/reconciliation-design.md`
- Review: `/Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/type-month-matching.md`
- Review: `/Users/athur/PycharmProjects/qyy/docs/superpowers/plans/reconciliation/archive-batch.md`

- [ ] **Step 1: Write the failing checklist**

Use this failure definition:

```text
FAIL if reconciliation has multiple candidate "main" pages with no explicit winner
FAIL if spec, plan, and current prototype mention different flows or terminology
FAIL if this best-developed module cannot serve as the template for the rest of the repo
```

- [ ] **Step 2: Review prototype/spec/plan alignment**

Run: `rg -n "summary|unified|archive|batch|PAID|匹配|归档" /Users/athur/PycharmProjects/qyy/prototype/reconciliation /Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation /Users/athur/PycharmProjects/qyy/docs/superpowers/plans/reconciliation`

Expected: The dominant terminology and active entry points are easy to identify.

- [ ] **Step 3: Document the reference pattern**

Write a short section into the reconciliation module index that states:

```text
- summary.html is the list-level entry
- unified.html is the detail-level entry
- reconciliation-design.md is the base spec
- archive-batch.md and type-month-matching.md are focused follow-up documents
```

- [ ] **Step 4: Use the same pattern as the model for other modules**

Apply the same “primary page / supporting pages / primary spec / follow-up docs” structure in the other module README files.

- [ ] **Step 5: Verify the module is now a reusable reference**

Run: `sed -n '1,200p' /Users/athur/PycharmProjects/qyy/docs/superpowers/specs/reconciliation/README.md`

Expected: A new collaborator can tell exactly where to start and what is legacy.

- [ ] **Step 6: Commit**

```bash
git add docs/superpowers/specs/reconciliation/README.md docs/superpowers/specs/*/README.md
git commit -m "docs: establish reconciliation module as repo navigation reference"
```

---

## Suggested Execution Order

### Today
- Task 1: Close Reorganization Leftovers
- Task 2: Formalize Local Config Safety

### This Week
- Task 3: Decide What Is First-Class vs Local-Only
- Task 4: Add Lightweight Module Indexes

### Later
- Task 5: Stabilize the Reconciliation Module as the Reference Standard

## Success Criteria

- Top-level docs match the current module-based repository structure
- Local credentials are documented through safe templates rather than real values
- Untracked support files are either intentionally committed, intentionally ignored, or removed
- Each module has a small navigation index that points to primary prototype/spec/plan assets
- Reconciliation becomes the documented reference pattern for future module cleanup
