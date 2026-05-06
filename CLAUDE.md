# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **青阳云 (Qingyang Cloud)** HRO (Human Resources Outsourcing) system project — a SaaS HR management platform. The codebase is a **prototype and design system repository** (no build process, no package.json):

1. **HTML Prototypes** (`prototype/`) — 42 HTML prototype pages for the HRO system
2. **Design System** (`styles/`) — CSS/SCSS component library with 25+ components
3. **Design Documentation** — Specs, plans, SQL drafts, and code wiki
4. **Claude Skills** (`.claude/skills/`) — Browser automation for the live HRO system
5. **Scripts** (`scripts/`) — Utility scripts for PDF conversion, memory management, git hooks

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `prototype/` | HTML prototype pages (42 files) — open directly in browser |
| `styles/` | Design system CSS/SCSS files |
| `docs/` | Code Wiki, specs, plans, and SQL drafts |
| `docs/superpowers/specs/` | Design specifications |
| `docs/superpowers/plans/` | Implementation plans |
| `docs/superpowers/sql/` | Database migration drafts |
| `scripts/` | Utility scripts (PDF conversion, git hooks, memory update) |
| `.claude/skills/` | Automation skills for Qingyang Cloud |
| `.claude/memory/` | Persistent session memory |

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

Key HTML prototypes in `prototype/`:

| Page | Description |
|------|-------------|
| `qingyang-policy-optimized.html` | Social insurance policy page |
| `qingyang-reconciliation-summary.html` | Reconciliation rule summary list |
| `qingyang-reconciliation-unified.html` | Reconciliation detail (system/ledger bills) |
| `settlement-plan-optimized.html` | Settlement plan management |
| `settlement-detail-optimized.html` | Settlement detail page |
| `employee-detail-redesign.html` | Employee detail redesign |
| `social-insurance-rule-stepper.html` | Insurance rule stepper wizard |
| `insurance-cost-allocation.html` | Insurance cost allocation |
| `field-collection-config-demo.html` | Field collection config |
| `approval-template-management.html` | Approval template management |
| `sys-log.html` | System log viewer |

**Versioning pattern:** Files with `-v2`, `-v3`, `-approach3`, `-approach4`, `-redesign` suffixes are iterative explorations. The latest/current version usually has no suffix or `-optimized`.

## Claude Skills

Skills in `.claude/skills/` automate interactions with the live Qingyang HRO system.

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

### Viewing Prototypes
Open HTML files directly in browser:
```bash
open prototype/qingyang-policy-optimized.html
```

Or serve via Python HTTP server:
```bash
# IMPORTANT: Serve from project root so ../styles/ CSS paths resolve correctly
python3 -m http.server 8080
# Then navigate to http://localhost:8080/prototype/<page>.html
```

**GOTCHA:** Serving from `prototype/` directory (e.g. `cd prototype && python3 -m http.server 8000`) causes CSS 404 errors because prototypes reference `../styles/` with relative paths. Always serve from project root.

### Browser Testing with Playwright MCP

Playwright MCP is configured for browser automation. Key tools:
- `browser_navigate` — Navigate to a URL
- `browser_snapshot` — Capture accessibility snapshot (better than screenshot for interaction)
- `browser_click` — Click on elements by reference
- `browser_take_screenshot` — Take a PNG/JPEG screenshot

Example test flow:
```
1. python3 -m http.server 8080  (from project root)
2. browser_navigate http://localhost:8080/prototype/qingyang-reconciliation-summary.html
3. browser_snapshot  (get element refs)
4. browser_click on specific elements
5. browser_take_screenshot  (capture visual result)
```

**Test artifacts:** `.playwright-mcp/` contains screenshots, logs, and snapshots — safe to clean up.

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

## Important Notes

1. **Playwright MCP** is configured for browser automation (see `.claude/settings.local.json`)
2. **No package.json** — Pure HTML/CSS/Python, no build process
3. **Prototypes are static HTML** — Open directly in browser or serve with `python3 -m http.server`
4. **Skills require Playwright MCP** — Ensure plugin is enabled for automation
5. **`.claude/worktrees/` and `.worktrees/`** are git worktree snapshots — not part of main source
6. **Post-commit memory update** — After each commit, `update-memory.sh` auto-generates a changelog in `.claude/memory/changes/` and updates `MEMORY.md`
