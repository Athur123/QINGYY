# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **青阳云 (Qingyang Cloud)** HRO (Human Resources Outsourcing) system project - a SaaS HR management platform. The codebase contains:

1. **HTML Prototypes** (`prototype/`) - UI/UX prototypes for the HRO system pages
2. **Design System** (`styles/`) - CSS/SCSS component library with 25+ components
3. **Resume Parser Scripts** - Python scripts for parsing resumes with OCR
4. **Claude Skills** (`.claude/skills/`) - Automation skills for interacting with the Qingyang HRO system

## Key Directories

| Directory | Purpose |
|-----------|---------|
| `prototype/` | HTML prototype pages for the HRO system (policy pages, dashboard, calculator, etc.) |
| `styles/` | Design system - CSS variables, components, and form elements |
| `scripts/` | Python scripts and tools |
| `scripts/resume-parser/` | Resume parsing scripts with OCR support |
| `.claude/skills/` | Automation skills for Qingyang Cloud operations |
| `.claude/memory/` | Persistent memory storage for Claude sessions |

## Design System

The project uses a custom design system documented in `qingyang-ui-ux-guidelines.md` and implemented in `styles/`.

### Key Design Tokens
- **Primary Color**: `#2563EB` (blue)
- **Background**: `#F8FAFC` (light gray)
- **Text Primary**: `#1E293B`
- **Text Secondary**: `#64748B`
- **Border**: `#E2E8F0`
- **Font**: Inter, system-ui, sans-serif

### CSS Files in `styles/`
- `qingyang-variables.css` - CSS variables/design tokens
- `qingyang-base.css` - Base styles and utility classes
- `qingyang-components.css` - 25+ UI components
- `qingyang-forms.css` - 15+ form controls
- `qingyang-variables.scss` - SCSS version with mixins

### Component Classes
Components use the `qy-` prefix:
- `qy-btn` - Buttons (variants: `--primary`, `--secondary`, `--text`, `--danger`)
- `qy-card` - Cards with `__header`, `__body`, `__footer`
- `qy-input` - Input fields
- `qy-table` - Data tables
- `qy-tag` - Tags/badges

## Claude Skills

Skills are located in `.claude/skills/` and automate interactions with the Qingyang HRO system.

### Available Skills

**1. qingyang-login** - Automates login to the Qingyang Cloud system
- URL: `http://192.168.10.168/#/login`
- Credentials stored in `.claude/settings.local.json` env vars
- Triggers: "登录青阳云", "打开HRO", "进入系统"

**2. qingyang-switch-hro** - Switches from EHR to HRO dimension
- Accessed via user avatar dropdown → "切换客户组织"
- Triggers: "切换到HRO", "进入客户组织", "HRO维度"

### Environment Variables (in `.claude/settings.local.json`)
```json
{
  "QINGYANG_LOGIN_URL": "http://192.168.10.168/#/login",
  "QINGYANG_TENANT": "test",
  "QINGYANG_USERNAME": "admin",
  "QINGYANG_PASSWORD": "123456"
}
```

## Prototype Pages

Key HTML prototypes in `prototype/`:

| File | Description |
|------|-------------|
| `qingyang-policy-optimized.html` | Social insurance policy page (227KB) |
| `qingyang-dashboard-optimized.html` | Dashboard page |
| `qingyang-insurance-archive-optimized.html` | Insurance archive page |
| `qingyang-insurance-rule-optimized.html` | Insurance rules page |
| `calculator-optimized.html` | Calculator tool |

## Resume Parser Scripts

Located in `scripts/resume-parser/` - Python scripts for parsing PDF resumes using OCR and text extraction.

| Script | Purpose |
|--------|---------|
| `parse_resumes.py` | Basic resume parser with regex matching |
| `parse_resumes_v2.py` | Enhanced parser with improved field extraction |
| `parse_resumes_detailed.py` | Detailed parser (Yuque standard structure) |
| `parse_resumes_json.py` | JSON output format |
| `parse_resumes_standard.py` | Standardized output format |
| `extract_he_resume_ocr.py` | OCR-based extraction for scanned PDFs |
| `extract_he_resume_v2.py` | Enhanced OCR with text cleanup |

See `scripts/resume-parser/README.md` for usage instructions.

## Development Workflow

### Viewing Prototypes
Open HTML files directly in browser:
```bash
open prototype/qingyang-policy-optimized.html
```

Or serve via Python HTTP server:
```bash
cd prototype && python3 -m http.server 8000
```

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
  
  @include respond-to('desktop') {
    padding: space(6);
  }
}
```

## System Architecture

### Qingyang Cloud HRO System
- **Two dimensions**: EHR (core HR) and HRO (outsourcing/dispatch)
- **Default after login**: EHR dimension
- **Switch to HRO**: Via user avatar → "切换客户组织"
- **HRO Features**: Upstream/downstream management (上下游管理)

### Design Philosophy
- Enterprise SaaS style - professional and trustworthy
- Soft Elegance design language
- Information density balanced for efficiency
- WCAG 2.1 AA accessibility compliance
- Responsive breakpoints: 768px, 1024px, 1440px

## Important Notes

1. **Playwright MCP** is configured for browser automation (see `.claude/settings.local.json`)
2. **No package.json** - This is not a Node.js project (pure HTML/CSS/Python)
3. **No build process** - Prototypes are static HTML files
4. **Skills require Playwright MCP** - Ensure plugin is enabled for automation
