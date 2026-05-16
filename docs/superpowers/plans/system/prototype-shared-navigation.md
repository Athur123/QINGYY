---
title: Prototype Shared Navigation Implementation Plan
module: system
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# Prototype Shared Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a shared navigation source for Qingyang HRO static prototypes and connect the current mainline prototype pages to it.

**Architecture:** Add `prototype/shared/prototype-nav.js` as the single source of navigation data and rendering behavior, plus `prototype/shared/prototype-nav.css` for shared navigation styles. Keep pages as static HTML; each mainline page opts in with a mount element and normal `<script>` tags.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Python HTTP server for local preview, shell commands for link verification.

---

## File Structure

- Create: `prototype/shared/prototype-nav.js`
  - Owns module/page data, link path resolution, index rendering, and sidebar rendering.
- Create: `prototype/shared/prototype-nav.css`
  - Owns shared prototype navigation styles only.
- Modify: `prototype/index.html`
  - Keeps page shell and visual design, but renders module cards from shared data.
- Modify first-stage mainline pages:
  - `prototype/reconciliation/summary.html`
  - `prototype/reconciliation/unified.html`
  - `prototype/calculator/index.html`
  - `prototype/calculator/policy.html`
  - `prototype/calculator/region-rules.html`
  - `prototype/calculator/sub-account.html`
  - `prototype/employee/detail.html`
  - `prototype/employee/change-field.html`
  - `prototype/employee/cost-detail.html`
  - `prototype/insurance-config/stepper.html`
  - `prototype/insurance-config/field-collection.html`
  - `prototype/settlement/plan.html`
  - `prototype/settlement/detail.html`
  - `prototype/settlement/cost-allocation.html`
  - `prototype/approval/template-management.html`
  - `prototype/system/log-viewer.html`
  - `prototype/system/sys-log.html`
- Modify: `docs/superpowers/specs/system/prototype-index.md`
  - Note that index data now comes from the shared navigation source.

## Task 1: Create Shared Navigation Data And Renderer

**Files:**
- Create: `prototype/shared/prototype-nav.js`
- Create: `prototype/shared/prototype-nav.css`

- [ ] **Step 1: Create `prototype/shared/` directory**

Run:

```bash
mkdir -p prototype/shared
```

Expected: command exits with code `0`.

- [ ] **Step 2: Add shared navigation JavaScript**

Create `prototype/shared/prototype-nav.js` with:

```javascript
(function () {
  const modules = [
    { id: 'reconciliation', name: '对账复核', mark: '对', description: '社保对账复核当前主线，包括规则汇总和统一明细核对。' },
    { id: 'calculator', name: '社保计算', mark: '算', description: '覆盖费用计算器、地区规则、政策库、二级户、参保档案和智能识别等原型。' },
    { id: 'employee', name: '员工管理', mark: '员', description: '员工档案、社保异动、费用明细和档案版本相关页面。' },
    { id: 'insurance-config', name: '参保配置', mark: '配', description: '参保规则配置和字段配置相关页面。' },
    { id: 'settlement', name: '结算方案', mark: '结', description: '结算计划、账单明细、费用分摊、费用归属和垫付相关页面。' },
    { id: 'approval', name: '审批管理', mark: '审', description: '审批模板配置和同步管理页面。' },
    { id: 'system', name: '系统', mark: '系', description: '日志查看、系统操作日志和汇总统计组件演示。' }
  ];

  const pages = [
    { id: 'reconciliation.summary', moduleId: 'reconciliation', title: '规则汇总', path: 'reconciliation/summary.html', status: 'main', isMain: true, description: '按规则、月度和状态汇总对账结果，支持进入明细核对。' },
    { id: 'reconciliation.unified', moduleId: 'reconciliation', title: '明细核对', path: 'reconciliation/unified.html', status: 'main', isMain: true, description: '统一承载系统账单、台账导入、自动匹配和人工确认流程。' },
    { id: 'reconciliation.obsolete', moduleId: 'reconciliation', title: '旧版三账单探索', path: 'reconciliation/obsolete/index.html', status: 'obsolete', isMain: false, description: '历史探索版本，仅保留参考，不作为当前对账复核原型入口。' },
    { id: 'calculator.index', moduleId: 'calculator', title: '费用计算器', path: 'calculator/index.html', status: 'main', isMain: true, description: '社保公积金费用测算入口，包含筛选和计算结果展示。' },
    { id: 'calculator.policy', moduleId: 'calculator', title: '政策库', path: 'calculator/policy.html', status: 'main', isMain: true, description: '社保公积金政策维护和查看页面。' },
    { id: 'calculator.regionRules', moduleId: 'calculator', title: '地区规则配置', path: 'calculator/region-rules.html', status: 'main', isMain: true, description: '按地区维护社保公积金规则配置。' },
    { id: 'calculator.subAccount', moduleId: 'calculator', title: '二级户管理', path: 'calculator/sub-account.html', status: 'main', isMain: true, description: '参保规则编辑中的二级户维护页面。' },
    { id: 'calculator.addInsuranceV2', moduleId: 'calculator', title: '社保增员 V2', path: 'calculator/add-insurance-v2.html', status: 'iteration', isMain: false, description: '社保增员流程的新版本原型。' },
    { id: 'calculator.addInsurance', moduleId: 'calculator', title: '社保增员旧版', path: 'calculator/add-insurance.html', status: 'iteration', isMain: false, description: '社保增员早期重设计页面。' },
    { id: 'calculator.formulaRecognitionV2', moduleId: 'calculator', title: '智能公式识别 V2', path: 'calculator/formula-recognition-v2.html', status: 'iteration', isMain: false, description: '公式识别交互的新版探索。' },
    { id: 'calculator.formulaRecognition', moduleId: 'calculator', title: '智能公式识别', path: 'calculator/formula-recognition.html', status: 'iteration', isMain: false, description: '公式识别能力的早期页面。' },
    { id: 'calculator.insuranceArchiveV2', moduleId: 'calculator', title: '参保档案 V2', path: 'calculator/insurance-archive-v2.html', status: 'iteration', isMain: false, description: '参保档案新版设计页面。' },
    { id: 'calculator.insuranceArchive', moduleId: 'calculator', title: '参保档案', path: 'calculator/insurance-archive.html', status: 'iteration', isMain: false, description: '参保档案优化设计页面。' },
    { id: 'calculator.redesign', moduleId: 'calculator', title: '计算器重设计', path: 'calculator/redesign.html', status: 'iteration', isMain: false, description: '社保公积金计算器重设计稿。' },
    { id: 'calculator.redesigned', moduleId: 'calculator', title: '费用计算器改版', path: 'calculator/redesigned.html', status: 'iteration', isMain: false, description: '费用计算器改版后的候选页面。' },
    { id: 'calculator.v2', moduleId: 'calculator', title: '计算器 V2', path: 'calculator/v2.html', status: 'iteration', isMain: false, description: '计算器第二版历史迭代。' },
    { id: 'calculator.v3', moduleId: 'calculator', title: '计算器 V3', path: 'calculator/v3.html', status: 'iteration', isMain: false, description: '计算器第三版历史迭代。' },
    { id: 'employee.detail', moduleId: 'employee', title: '员工档案', path: 'employee/detail.html', status: 'main', isMain: true, description: '员工档案详情的当前重设计页面。' },
    { id: 'employee.changeField', moduleId: 'employee', title: '异动字段采集', path: 'employee/change-field.html', status: 'main', isMain: true, description: '社保异动操作中的增员字段采集页面。' },
    { id: 'employee.costDetail', moduleId: 'employee', title: '员工费用明细', path: 'employee/cost-detail.html', status: 'main', isMain: true, description: '单员工费用明细查看页面。' },
    { id: 'employee.transactionList', moduleId: 'employee', title: '社保异动列表', path: 'employee/transaction-list.html', status: 'iteration', isMain: false, description: '社保异动列表优化设计页面。' },
    { id: 'employee.archiveVersion', moduleId: 'employee', title: '档案版本管理', path: 'employee/archive-version.html', status: 'iteration', isMain: false, description: '员工档案版本管理页面。' },
    { id: 'employee.detailV3', moduleId: 'employee', title: '员工详情 V3', path: 'employee/detail-v3.html', status: 'iteration', isMain: false, description: '员工详情第三版历史迭代。' },
    { id: 'employee.detailV2', moduleId: 'employee', title: '员工详情 V2', path: 'employee/detail-v2.html', status: 'iteration', isMain: false, description: '员工详情第二版历史迭代。' },
    { id: 'employee.detailOld', moduleId: 'employee', title: '员工详情旧版', path: 'employee/detail-old.html', status: 'iteration', isMain: false, description: '员工详情早期版本。' },
    { id: 'insuranceConfig.stepper', moduleId: 'insurance-config', title: '参保规则配置向导', path: 'insurance-config/stepper.html', status: 'main', isMain: true, description: '使用分步向导配置社保参保规则。' },
    { id: 'insuranceConfig.fieldCollection', moduleId: 'insurance-config', title: '字段采集配置', path: 'insurance-config/field-collection.html', status: 'main', isMain: true, description: '全局字段采集配置页面。' },
    { id: 'insuranceConfig.globalField', moduleId: 'insurance-config', title: '全局字段配置', path: 'insurance-config/global-field.html', status: 'iteration', isMain: false, description: '全局字段配置早期或备选页面。' },
    { id: 'insuranceConfig.fieldOnboarding', moduleId: 'insurance-config', title: '入职字段配置', path: 'insurance-config/field-onboarding.html', status: 'iteration', isMain: false, description: '入职管理场景字段配置页面。' },
    { id: 'insuranceConfig.fieldSettlement', moduleId: 'insurance-config', title: '结算字段配置', path: 'insurance-config/field-settlement.html', status: 'iteration', isMain: false, description: '结算明细场景字段配置页面。' },
    { id: 'settlement.plan', moduleId: 'settlement', title: '办理结算计划', path: 'settlement/plan.html', status: 'main', isMain: true, description: '结算方案列表和办理计划页面。' },
    { id: 'settlement.detail', moduleId: 'settlement', title: '账单明细', path: 'settlement/detail.html', status: 'main', isMain: true, description: '结算方案中的账单明细优化页面。' },
    { id: 'settlement.costAllocation', moduleId: 'settlement', title: '保险福利核算', path: 'settlement/cost-allocation.html', status: 'main', isMain: true, description: '保险福利费用核算和分摊页面。' },
    { id: 'settlement.advancePayment', moduleId: 'settlement', title: '申请垫付', path: 'settlement/advance-payment.html', status: 'iteration', isMain: false, description: '结算相关垫付申请页面。' },
    { id: 'settlement.costAttribution', moduleId: 'settlement', title: '费用归属固化', path: 'settlement/cost-attribution.html', status: 'demo', isMain: false, description: '调动和费用归属固化规则演示页面。' },
    { id: 'approval.templateManagement', moduleId: 'approval', title: '审批模板管理', path: 'approval/template-management.html', status: 'main', isMain: true, description: '审批模板列表、配置、同步状态和抽屉详情页面。' },
    { id: 'system.logViewer', moduleId: 'system', title: '日志查看', path: 'system/log-viewer.html', status: 'main', isMain: true, description: 'HRO 系统日志查看页面。' },
    { id: 'system.sysLog', moduleId: 'system', title: '系统操作日志', path: 'system/sys-log.html', status: 'main', isMain: true, description: '系统操作日志查询和浏览页面。' },
    { id: 'system.summaryDemo', moduleId: 'system', title: '汇总统计项演示', path: 'system/summary-demo.html', status: 'demo', isMain: false, description: '3 到 4 项汇总统计组件效果演示。' }
  ];

  const statusLabels = {
    main: '主线',
    iteration: '迭代',
    demo: '演示',
    obsolete: '已废弃'
  };

  function getRelativePrefix() {
    const marker = document.querySelector('[data-prototype-nav-root]');
    if (marker) return marker.getAttribute('data-prototype-nav-root') || '';
    return document.body.getAttribute('data-prototype-root') || '';
  }

  function resolvePath(path, rootPrefix) {
    return `${rootPrefix || ''}${path}`;
  }

  function renderSidebar(target) {
    const current = target.getAttribute('data-current') || '';
    const rootPrefix = target.getAttribute('data-root') || getRelativePrefix();
    const moduleBlocks = modules.map((module) => {
      const modulePages = pages.filter((page) => page.moduleId === module.id && page.isMain);
      if (!modulePages.length) return '';
      const pageLinks = modulePages.map((page) => {
        const active = page.id === current ? ' is-active' : '';
        const ariaCurrent = page.id === current ? ' aria-current="page"' : '';
        return `<a class="prototype-nav__item${active}" href="${resolvePath(page.path, rootPrefix)}"${ariaCurrent}>${page.title}</a>`;
      }).join('');
      return `<section class="prototype-nav__group"><h3 class="prototype-nav__group-title">${module.name}</h3>${pageLinks}</section>`;
    }).join('');

    target.innerHTML = `
      <aside class="prototype-nav" aria-label="原型导航">
        <div class="prototype-nav__brand">
          <strong>青阳云 HRO</strong>
          <span>Prototype</span>
        </div>
        <a class="prototype-nav__home" href="${rootPrefix || ''}index.html">返回原型入口</a>
        <nav class="prototype-nav__body">${moduleBlocks}</nav>
      </aside>
    `;
  }

  function renderIndex(target) {
    const rootPrefix = target.getAttribute('data-root') || '';
    const moduleCards = modules.map((module) => {
      const modulePages = pages.filter((page) => page.moduleId === module.id);
      const cards = modulePages.map((page) => `
        <a class="page-card${page.status === 'obsolete' ? ' page-card--obsolete' : ''}" href="${resolvePath(page.path, rootPrefix)}">
          <div>
            <div class="page-card__top">
              <h3 class="page-card__title">${page.title}</h3>
              <span class="badge badge--${page.status}">${statusLabels[page.status]}</span>
            </div>
            <p class="page-card__desc">${page.description}</p>
          </div>
          <span class="page-card__path">${page.path}</span>
        </a>
      `).join('');

      return `
        <section class="module" id="${module.id}">
          <div class="module__header">
            <div>
              <h2 class="module__title"><span class="module__mark">${module.mark}</span>${module.name}</h2>
              <p class="module__desc">${module.description}</p>
            </div>
            <span class="module__meta">${modulePages.length} 个页面</span>
          </div>
          <div class="page-grid">${cards}</div>
        </section>
      `;
    }).join('');

    target.innerHTML = moduleCards;
  }

  function init() {
    document.querySelectorAll('[data-prototype-nav]').forEach(renderSidebar);
    document.querySelectorAll('[data-prototype-index]').forEach(renderIndex);
  }

  window.QYPrototypeNav = {
    modules,
    pages,
    statusLabels,
    renderSidebar,
    renderIndex,
    init
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
```

- [ ] **Step 3: Add shared navigation CSS**

Create `prototype/shared/prototype-nav.css` with:

```css
.prototype-nav {
  width: 192px;
  min-height: 100vh;
  background: var(--qy-bg-primary, #fff);
  border-right: 1px solid var(--qy-border-light, #e2e8f0);
  color: var(--qy-text-primary, #1e293b);
}

.prototype-nav__brand {
  padding: 18px 16px 14px;
  border-bottom: 1px solid var(--qy-border-light, #e2e8f0);
}

.prototype-nav__brand strong {
  display: block;
  color: var(--qy-primary-600, #2563eb);
  font-size: 15px;
  line-height: 1.2;
}

.prototype-nav__brand span {
  display: block;
  margin-top: 4px;
  color: var(--qy-text-muted, #94a3b8);
  font-size: 11px;
}

.prototype-nav__home {
  display: flex;
  align-items: center;
  height: 34px;
  margin: 12px 10px 8px;
  padding: 0 10px;
  border-radius: 8px;
  background: var(--qy-primary-50, #eff6ff);
  color: var(--qy-primary-600, #2563eb);
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
}

.prototype-nav__body {
  padding: 6px 10px 18px;
}

.prototype-nav__group {
  margin-top: 12px;
}

.prototype-nav__group-title {
  margin: 0 0 5px;
  padding: 0 6px;
  color: var(--qy-text-muted, #94a3b8);
  font-size: 11px;
  font-weight: 700;
}

.prototype-nav__item {
  display: flex;
  align-items: center;
  min-height: 30px;
  padding: 6px 8px;
  border-radius: 8px;
  color: var(--qy-text-secondary, #64748b);
  font-size: 12px;
  line-height: 1.35;
  text-decoration: none;
}

.prototype-nav__item:hover {
  background: var(--qy-bg-secondary, #f8fafc);
  color: var(--qy-text-primary, #1e293b);
}

.prototype-nav__item.is-active {
  background: var(--qy-primary-50, #eff6ff);
  color: var(--qy-primary-600, #2563eb);
  font-weight: 700;
}

@media (max-width: 900px) {
  .prototype-nav {
    width: 100%;
    min-height: auto;
    border-right: 0;
    border-bottom: 1px solid var(--qy-border-light, #e2e8f0);
  }

  .prototype-nav__body {
    display: flex;
    gap: 12px;
    overflow-x: auto;
    padding-bottom: 12px;
  }

  .prototype-nav__group {
    flex: 0 0 150px;
    margin-top: 0;
  }
}
```

- [ ] **Step 4: Verify shared files exist**

Run:

```bash
test -f prototype/shared/prototype-nav.js && test -f prototype/shared/prototype-nav.css
```

Expected: command exits with code `0`.

## Task 2: Convert Index To Shared Data Rendering

**Files:**
- Modify: `prototype/index.html`

- [ ] **Step 1: Add shared script to `prototype/index.html`**

In `<head>`, keep existing CSS references. Before `</body>`, add:

```html
    <script src="shared/prototype-nav.js"></script>
```

- [ ] **Step 2: Replace hardcoded module sections**

Replace all hardcoded module `<section class="module" ...>` blocks with:

```html
        <div data-prototype-index></div>
```

Keep the existing hero, stats, toolbar, footer note, and all CSS classes used by rendered cards.

- [ ] **Step 3: Update badge CSS class names**

Ensure `prototype/index.html` has badge styles for the shared status keys:

```css
.badge--main { background: var(--qy-primary-50); color: var(--qy-primary-600); }
.badge--iteration { background: #F1F5F9; color: #475569; }
.badge--demo { background: #ECFDF5; color: #047857; }
.badge--obsolete { background: #FEF2F2; color: #B91C1C; }
```

- [ ] **Step 4: Verify index still references shared renderer**

Run:

```bash
rg -n "data-prototype-index|shared/prototype-nav.js" prototype/index.html
```

Expected: output includes both `data-prototype-index` and `shared/prototype-nav.js`.

## Task 3: Connect Mainline Pages With Existing Main Sidebars

**Files:**
- Modify: `prototype/reconciliation/summary.html`
- Modify: `prototype/reconciliation/unified.html`
- Modify: `prototype/calculator/index.html`
- Modify: `prototype/calculator/policy.html`
- Modify: `prototype/calculator/region-rules.html`
- Modify: `prototype/calculator/sub-account.html`
- Modify: `prototype/insurance-config/stepper.html`
- Modify: `prototype/insurance-config/field-collection.html`
- Modify: `prototype/settlement/cost-allocation.html`
- Modify: `prototype/system/log-viewer.html`
- Modify: `prototype/system/sys-log.html`
- Modify: `prototype/approval/template-management.html`

- [ ] **Step 1: Add shared CSS and script references**

For each file in this task, add this stylesheet after the existing Qingyang CSS links:

```html
    <link rel="stylesheet" href="../shared/prototype-nav.css">
```

Before `</body>`, add:

```html
    <script src="../shared/prototype-nav.js"></script>
```

- [ ] **Step 2: Replace the main sidebar markup**

For each file in this task, replace the existing project-level main sidebar with the exact matching mount:

```html
        <div data-prototype-nav data-root="../" data-current="reconciliation.summary"></div>
        <div data-prototype-nav data-root="../" data-current="reconciliation.unified"></div>
        <div data-prototype-nav data-root="../" data-current="calculator.index"></div>
        <div data-prototype-nav data-root="../" data-current="calculator.policy"></div>
        <div data-prototype-nav data-root="../" data-current="calculator.regionRules"></div>
        <div data-prototype-nav data-root="../" data-current="calculator.subAccount"></div>
        <div data-prototype-nav data-root="../" data-current="insuranceConfig.stepper"></div>
        <div data-prototype-nav data-root="../" data-current="insuranceConfig.fieldCollection"></div>
        <div data-prototype-nav data-root="../" data-current="settlement.costAllocation"></div>
        <div data-prototype-nav data-root="../" data-current="system.logViewer"></div>
        <div data-prototype-nav data-root="../" data-current="system.sysLog"></div>
        <div data-prototype-nav data-root="../" data-current="approval.templateManagement"></div>
```

Apply one mount per file using this map:

| File | `PAGE_ID` |
| --- | --- |
| `prototype/reconciliation/summary.html` | `reconciliation.summary` |
| `prototype/reconciliation/unified.html` | `reconciliation.unified` |
| `prototype/calculator/index.html` | `calculator.index` |
| `prototype/calculator/policy.html` | `calculator.policy` |
| `prototype/calculator/region-rules.html` | `calculator.regionRules` |
| `prototype/calculator/sub-account.html` | `calculator.subAccount` |
| `prototype/insurance-config/stepper.html` | `insuranceConfig.stepper` |
| `prototype/insurance-config/field-collection.html` | `insuranceConfig.fieldCollection` |
| `prototype/settlement/cost-allocation.html` | `settlement.costAllocation` |
| `prototype/system/log-viewer.html` | `system.logViewer` |
| `prototype/system/sys-log.html` | `system.sysLog` |
| `prototype/approval/template-management.html` | `approval.templateManagement` |

The replacement target is only the project navigation sidebar. Do not replace employee information panels, filter sidebars, right sidebars, or page-local quick navigation.

- [ ] **Step 3: Preserve layout offsets**

If a page uses `margin-left: var(--qy-sidebar-width)` or a fixed width matching its old sidebar, update only the sidebar width variable or wrapper class so the content still starts after the shared navigation. Do not rewrite page content layout.

Use this CSS override near that page's existing sidebar CSS when needed:

```css
:root { --qy-sidebar-width: 192px; }
```

- [ ] **Step 4: Verify mounted page IDs**

Run:

```bash
rg -n "data-prototype-nav|prototype-nav.css|prototype-nav.js" prototype/reconciliation/summary.html prototype/reconciliation/unified.html prototype/calculator/index.html prototype/calculator/policy.html prototype/calculator/region-rules.html prototype/calculator/sub-account.html prototype/insurance-config/stepper.html prototype/insurance-config/field-collection.html prototype/settlement/cost-allocation.html prototype/system/log-viewer.html prototype/system/sys-log.html prototype/approval/template-management.html
```

Expected: every listed file has one `data-prototype-nav`, one `prototype-nav.css`, and one `prototype-nav.js`.

## Task 4: Add Lightweight Entry Links For Mainline Pages Without Safe Sidebar Replacement

**Files:**
- Modify: `prototype/employee/detail.html`
- Modify: `prototype/employee/change-field.html`
- Modify: `prototype/employee/cost-detail.html`
- Modify: `prototype/settlement/plan.html`
- Modify: `prototype/settlement/detail.html`

- [ ] **Step 1: Add shared navigation stylesheet and script**

For each file in this task, add:

```html
    <link rel="stylesheet" href="../shared/prototype-nav.css">
```

Before `</body>`, add:

```html
    <script src="../shared/prototype-nav.js"></script>
```

- [ ] **Step 2: Add a compact shared navigation mount near the top of the page body**

Insert the exact matching compact mount near the start of `<body>`, before the page's main content wrapper:

```html
    <div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="employee.detail"></div>
    <div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="employee.changeField"></div>
    <div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="employee.costDetail"></div>
    <div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="settlement.plan"></div>
    <div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="settlement.detail"></div>
```

Apply one mount per file using this map:

| File | `PAGE_ID` |
| --- | --- |
| `prototype/employee/detail.html` | `employee.detail` |
| `prototype/employee/change-field.html` | `employee.changeField` |
| `prototype/employee/cost-detail.html` | `employee.costDetail` |
| `prototype/settlement/plan.html` | `settlement.plan` |
| `prototype/settlement/detail.html` | `settlement.detail` |

- [ ] **Step 3: Add compact mode CSS to shared stylesheet**

Extend `prototype/shared/prototype-nav.css` with:

```css
.prototype-nav-compact .prototype-nav {
  width: 100%;
  min-height: auto;
  border-right: 0;
  border-bottom: 1px solid var(--qy-border-light, #e2e8f0);
}

.prototype-nav-compact .prototype-nav__body {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  padding-bottom: 12px;
}

.prototype-nav-compact .prototype-nav__group {
  flex: 0 0 150px;
  margin-top: 0;
}
```

- [ ] **Step 4: Verify compact mounts**

Run:

```bash
rg -n "prototype-nav-compact|data-prototype-nav|prototype-nav.css|prototype-nav.js" prototype/employee/detail.html prototype/employee/change-field.html prototype/employee/cost-detail.html prototype/settlement/plan.html prototype/settlement/detail.html
```

Expected: every listed file has compact mount, shared CSS, and shared JS.

## Task 5: Update Documentation

**Files:**
- Modify: `docs/superpowers/specs/system/prototype-index.md`
- Modify: `docs/superpowers/specs/system/prototype-shared-navigation.md`

- [ ] **Step 1: Update prototype index spec**

Add this note under `## 交互要求` in `docs/superpowers/specs/system/prototype-index.md`:

```markdown
- 页面清单和状态标签应优先来自 `prototype/shared/prototype-nav.js`，避免入口页与主线页面导航分叉。
```

- [ ] **Step 2: Update shared navigation spec with implemented file names**

If implementation changes any file names from the spec, update `docs/superpowers/specs/system/prototype-shared-navigation.md` so it matches the final files.

- [ ] **Step 3: Verify documentation references**

Run:

```bash
rg -n "prototype-nav.js|prototype-nav.css|prototype/index.html" docs/superpowers/specs/system/prototype-index.md docs/superpowers/specs/system/prototype-shared-navigation.md
```

Expected: output references shared JS, shared CSS, and prototype index.

## Task 6: Link And Coverage Verification

**Files:**
- Verify: `prototype/shared/prototype-nav.js`
- Verify: `prototype/index.html`
- Verify: first-stage mainline pages

- [ ] **Step 1: Verify every shared-data page path exists**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re

source = Path('prototype/shared/prototype-nav.js').read_text()
paths = re.findall(r"path: '([^']+)'", source)
missing = [path for path in paths if not Path('prototype', path).is_file()]
if missing:
    print('\n'.join(missing))
    raise SystemExit(1)
print(f'checked {len(paths)} paths')
PY
```

Expected: `checked 39 paths`.

- [ ] **Step 2: Verify all first-stage page IDs exist in shared data**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import re

source = Path('prototype/shared/prototype-nav.js').read_text()
ids = set(re.findall(r"id: '([^']+)'", source))
expected = {
    'reconciliation.summary',
    'reconciliation.unified',
    'calculator.index',
    'calculator.policy',
    'calculator.regionRules',
    'calculator.subAccount',
    'employee.detail',
    'employee.changeField',
    'employee.costDetail',
    'insuranceConfig.stepper',
    'insuranceConfig.fieldCollection',
    'settlement.plan',
    'settlement.detail',
    'settlement.costAllocation',
    'approval.templateManagement',
    'system.logViewer',
    'system.sysLog',
}
missing = sorted(expected - ids)
if missing:
    print('\n'.join(missing))
    raise SystemExit(1)
print(f'checked {len(expected)} first-stage ids')
PY
```

Expected: `checked 17 first-stage ids`.

- [ ] **Step 3: Verify all first-stage pages are connected**

Run:

```bash
python3 - <<'PY'
from pathlib import Path

files = [
    'prototype/reconciliation/summary.html',
    'prototype/reconciliation/unified.html',
    'prototype/calculator/index.html',
    'prototype/calculator/policy.html',
    'prototype/calculator/region-rules.html',
    'prototype/calculator/sub-account.html',
    'prototype/employee/detail.html',
    'prototype/employee/change-field.html',
    'prototype/employee/cost-detail.html',
    'prototype/insurance-config/stepper.html',
    'prototype/insurance-config/field-collection.html',
    'prototype/settlement/plan.html',
    'prototype/settlement/detail.html',
    'prototype/settlement/cost-allocation.html',
    'prototype/approval/template-management.html',
    'prototype/system/log-viewer.html',
    'prototype/system/sys-log.html',
]

missing = []
for file in files:
    text = Path(file).read_text()
    required = ['prototype-nav.css', 'data-prototype-nav', 'prototype-nav.js']
    for token in required:
        if token not in text:
            missing.append(f'{file}: {token}')

if missing:
    print('\n'.join(missing))
    raise SystemExit(1)
print(f'checked {len(files)} connected pages')
PY
```

Expected: `checked 17 connected pages`.

- [ ] **Step 4: Preview with local server**

Run:

```bash
python3 -m http.server 8080
```

Open:

```text
http://localhost:8080/prototype/
http://localhost:8080/prototype/reconciliation/summary.html
http://localhost:8080/prototype/calculator/index.html
http://localhost:8080/prototype/settlement/plan.html
```

Expected:

- Index renders module cards.
- Mainline pages show shared prototype navigation.
- Current page is highlighted.
- “返回原型入口” returns to `prototype/index.html`.
