# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dual Agent Support

This repository is intentionally set up to support both **Claude Code** and **Codex** from the same project root.

- `CLAUDE.md` is the Claude Code entry file
- `AGENTS.md` is the Codex entry file
- Shared repository guidance should stay aligned in both files
- Claude-specific local config lives in `.claude/`
- Codex-specific local config lives in `.codex/`
- Codex project skills live in `.agents/skills/`

## Project Overview

This is the **青阳云 (Qingyang Cloud)** HRO (Human Resources Outsourcing) system project — a SaaS HR management platform. The codebase is a **prototype and design system repository** (no build process, no package.json):

1. **HTML Prototypes** (`prototype/`) — 41 HTML prototype pages organized by business module
2. **Design System** (`styles/`) — CSS/SCSS component library with 25+ components
3. **Design Documentation** — Specs, plans, SQL drafts, and code wiki
4. **Claude Skills** (`.claude/skills/`) — Browser automation for the live HRO system
5. **Scripts** (`scripts/`) — Utility scripts for PDF conversion, memory management, git hooks

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `prototype/` | HTML prototype pages (41 files in 7 modules) — serve from project root |
| `styles/` | Design system CSS/SCSS files |
| `docs/` | Code Wiki, specs, plans, and SQL drafts |
| `docs/superpowers/specs/` | Design specs (7 modules: reconciliation, calculator, employee, settlement, insurance-config, approval, system) |
| `docs/superpowers/plans/` | Implementation plans (same 7-module structure) |
| `docs/superpowers/sql/` | Database migration drafts |
| `scripts/` | Utility scripts (PDF conversion, git hooks, memory update) |
| `.claude/skills/` | Automation skills for Qingyang Cloud |
| `.agents/skills/` | Codex project skills for Qingyang Cloud |
| `.claude/memory/` | Persistent session memory |
| `.codex/` | Codex local configuration (machine-local, do not commit secrets) |

## Design System

The design system is documented in two key files:
- **`qingyang-hro-design-system.md`** — Full component handbook (v2.0, merged guidelines + design-system)
- **`styles/README.md`** — Extensive component documentation (1000+ lines)

### Key Design Tokens (v2.0)
- **Primary Color**: `--qy-primary-500` = `#2563EB`
- **Background**: `--qy-bg-secondary` = `#F8FAFC`
- **Text Primary**: `--qy-text-primary` = `#1E293B` (11.5:1 contrast)
- **Text Secondary**: `--qy-text-secondary` = `#64748B` (5.7:1 contrast)
- **Border**: `--qy-border-light` = `#E2E8F0`
- **Font**: Plus Jakarta Sans, Inter, system-ui, sans-serif
- **Body Size**: 14px (upgraded from 12px in v1.x)

### CSS Files in `styles/`
- `qingyang-variables.css` — CSS variables / design tokens
- `qingyang-base.css` — Base styles and utilities
- `qingyang-components.css` — 25+ UI components
- `qingyang-forms.css` — 15+ form controls
- `qingyang-design-system.css` — Combined design system
- `qingyang-variables.scss` — SCSS version with mixins

### Component Classes
Components use the `qy-` prefix (BEM-style):
- `qy-btn` — Buttons (variants: `--primary`, `--secondary`, `--text`, `--danger`)
- `qy-card` — Cards with `__header`, `__body`, `__footer`
- `qy-input` — Input fields
- `qy-table` — Data tables
- `qy-tag` — Tags/badges

## Prototype Pages

Prototypes organized by business module under `prototype/`. Serve from project root: `python3 -m http.server 8080`, then navigate to `http://localhost:8080/prototype/<module>/<page>.html`.

| Module | Directory | Active Pages |
|--------|-----------|-------------|
| **对账复核** | `reconciliation/` | `summary.html` (汇总列表), `unified.html` (明细核对) |
| **社保计算** | `calculator/` | `index.html` (计算器), `policy.html` (政策), `region-rules.html`, `sub-account.html`, `formula-recognition.html` |
| **员工管理** | `employee/` | `detail.html` (员工详情), `change-field.html` (异动采集), `cost-detail.html`, `archive-version.html` |
| **结算方案** | `settlement/` | `plan.html` (结算列表), `detail.html` (结算详情), `cost-attribution.html`, `cost-allocation.html` |
| **参保配置** | `insurance-config/` | `stepper.html` (规则向导), `field-collection.html`, `global-field.html` |
| **审批管理** | `approval/` | `template-management.html` |
| **系统** | `system/` | `log-viewer.html`, `sys-log.html` |

**Versioning:** Old iterations kept alongside active pages (e.g., `calculator/v2.html`, `v3.html`; `employee/detail-v2.html`, `detail-old.html`; `reconciliation/approach3.html`).

## Claude Skills

Skills in `.claude/skills/` automate interactions with the live Qingyang HRO system.

## Codex Compatibility

Codex reads the root-level `AGENTS.md`. Keep shared project facts synchronized between `CLAUDE.md` and `AGENTS.md`, store Codex project skills in `.agents/skills/`, and keep Codex machine-local environment settings in `.codex/config.toml`.

### Available Skills

**1. qingyang-login** — Login to Qingyang Cloud
- URL: `https://qingyangyun.com.cn/#/login`
- Credentials from `.claude/settings.local.json` env vars
- Triggers: "登录青阳云", "打开HRO", "进入系统"

**2. qingyang-switch-hro** — Switch from EHR to HRO dimension
- Via user avatar dropdown → "切换客户组织"
- Triggers: "切换到HRO", "进入客户组织", "HRO维度"

### Environment Variables (in `.claude/settings.local.json`)
```json
{
  "QINGYANG_LOGIN_URL": "https://qingyangyun.com.cn/#/login",
  "QINGYANG_TENANT": "zjhcrl",
  "QINGYANG_USERNAME": "admin",
  "QINGYANG_PASSWORD": "<redacted>"
}
```

## Development Workflow

This project follows a **brainstorming → spec → plan → implement** cycle:

1. **Brainstorming** — explore context, ask clarifying questions, present design in sections
2. **Spec** — write validated design to `docs/superpowers/specs/<module>/<name>.md`； commit
3. **Plan** — break spec into bite-sized implementation tasks in `docs/superpowers/plans/<module>/<name>.md`
4. **Implement** — execute tasks, test in browser, commit incrementally

### Viewing Prototypes
Serve via Python HTTP server from project root (required for CSS paths to resolve):
```bash
python3 -m http.server 8080
# Navigate to http://localhost:8080/prototype/<module>/<page>.html
# Example: http://localhost:8080/prototype/reconciliation/summary.html
```

**GOTCHA:** Prototypes are one level deeper now (`prototype/<module>/`), CSS references use `../../styles/`. Always serve from project root.

### Browser Testing with Playwright MCP

Playwright MCP is configured for browser automation. Key tools:
- `browser_navigate` — Navigate to a URL
- `browser_snapshot` — Capture accessibility snapshot (better than screenshot for interaction)
- `browser_click` — Click on elements by reference
- `browser_take_screenshot` — Take a PNG/JPEG screenshot

Example test flow:
```
1. python3 -m http.server 8080  (from project root)
2. browser_navigate http://localhost:8080/prototype/reconciliation/summary.html
3. browser_snapshot  (get element refs)
4. browser_click on specific elements
5. browser_take_screenshot  (capture visual result)
```

**Test artifacts:** `.playwright-mcp/` contains playwright screenshots, logs, and snapshots. Manual test screenshots go to `screenshots/` directory. Both are gitignored — safe to clean up.

### Using Claude Skills
Skills auto-trigger on keywords. To manually invoke:
```
/skill qingyang-login
/skill qingyang-switch-hro
```

### Working with the Design System

**Add new styles:**
1. CSS variables go in `qingyang-variables.css`
2. Components go in `qingyang-components.css`
3. Form elements go in `qingyang-forms.css`

**Using SCSS:**
```scss
@import 'styles/qingyang-variables';

.my-component {
  background: $primary-500;
  padding: space(4);
  border-radius: radius('md');
}
```

## Scripts

Utility scripts in `scripts/`:

| Script | Purpose |
|--------|---------|
| `md_to_pdf.py` | Convert Markdown spec docs to PDF (uses reportlab, Chinese font STHeiti) |
| `update-memory.sh` | Post-commit hook: analyzes git changes, generates changelog, updates MEMORY.md |
| `post-commit-hook.sh` | Git hook installer — copies itself to `.git/hooks/post-commit` |

## System Architecture

### Qingyang Cloud HRO System
- **Two dimensions**: EHR (core HR) and HRO (outsourcing/dispatch)
- **Default after login**: EHR dimension
- **Switch to HRO**: Via user avatar → "切换客户组织"
- **HRO Features**: Upstream/downstream management (上下游管理), settlement plans, insurance rules

### Architecture Notes
- Prototypes use inline `<script>` with vanilla DOM APIs — no framework dependencies
- Design system referenced via `<link>` tags in prototype HTML
- Backend/API is mocked in prototypes; real backend only documented in `docs/superpowers/`
- `API_BASE` constants in prototypes point to mock endpoints
- User's preferred tech stack for production: Vue 3 + TypeScript + Vite (Composition API)

### Reconciliation System Architecture

The reconciliation module is the most complex part of the codebase. Key concepts:

**Data flow**: Summary page (`reconciliation/summary.html`) → detail page (`reconciliation/unified.html`) via URL params (`?ruleName=X&month=Y` or `?groupId=Z`).

**Core data structures** in unified.html:
- `systemRecords[]` — system-side fee records (23 demo records S001-S023)
- `ledgerRecords[]` — imported ledger records
- `matchingResults { matched, pending, diffs, executed }` — matching engine output
- `archiveBatches[]` — archive batch metadata (B001, B002...)
- Each record has `matchStatus` (UNMATCHED/MATCHED/PENDING/DIFF/PAID), `archived` (boolean), `archiveBatchId`

**Key interactions**: Tab switching (system/ledger) → status/type filters → single/batch operations → confirmation dialogs → right-side drawers (pairing, detail, archive). Archive batches use a separate drawer, with batch filtering via dropdown selects that drive `getFilteredSystemRecords()` / `getFilteredLedgerRecords()`.

## Important Notes

1. **Playwright MCP** is configured for browser automation
2. **No package.json** — Pure HTML/CSS/Python, no build process
3. **`.claude/settings.local.json`** — local credentials file (gitignored, never commit)
4. **Prototypes are static HTML** — serve with `python3 -m http.server` from project root
5. **Skills require Playwright MCP** — Ensure plugin is enabled for automation
6. **`.claude/worktrees/` and `.worktrees/`** are git worktree snapshots — not part of main source
7. **Test screenshots go to `screenshots/`** — Never save screenshots to project root. Both `screenshots/` and `*.png` are gitignored.
8. **File organization** — New features follow the 7-module structure. Prototypes → `prototype/<module>/`, specs → `docs/superpowers/specs/<module>/`, plans → `docs/superpowers/plans/<module>/`. Short business-meaningful filenames, no date prefixes.
