# 社保对账复核功能实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建社保对账复核页面原型，实现系统记录与社保局台账的差异核对功能

**Architecture:** 单页HTML应用，依赖青阳云设计系统。页面包含顶部筛选区、三卡片汇总区、Tab切换视图、差异明细表格、详情弹窗。数据使用前端静态模拟，支持Excel导入导出。

**Tech Stack:** HTML5 / CSS3 (CSS Variables) / Vanilla JavaScript / SheetJS (xlsx)

---

## 文件结构

```
prototype/
└── qingyang-reconciliation.html    (新建：对账复核主页面)

styles/
└── [复用现有 qingyang-variables.css / qingyang-components.css / qingyang-forms.css]
```

---

## 数据模型定义（JS）

```javascript
// 系统记录（模拟数据）
const SYSTEM_RECORDS = [
  {
    id: 'sys_001',
    name: '张三',
    idCard: '430105199001011234',
    customer: '某科技有限公司',
    settlement: '结算主体A',
    scheme: '长沙标准方案',
    insuranceType: '养老保险',
    baseAmount: 6000,
    companyFee: 1234,
    personalFee: 480,
    declareStatus: '申报成功',     // 待申报/申报中/申报成功/申报失败
    declareDate: '2026-04-05',
    billingMonth: '2026-04'
  },
  // ...更多记录
];

// 台账记录（导入后存储）
let LEDGER_RECORDS = [];

// 差异记录（计算后生成）
let DIFFERENCE_RECORDS = [];
```

---

## 任务分解

### Task 1: 创建页面骨架和布局

**Files:**
- Create: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 创建基础HTML结构**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>社保对账复核 - 青阳云</title>
    <!-- 引入字体和设计系统 -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-base.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <link rel="stylesheet" href="../styles/qingyang-forms.css">
    <style>/* 页面特有样式 */</style>
</head>
<body>
    <div class="app-container">
        <!-- 侧边栏 -->
        <aside class="sidebar">...</aside>
        <!-- 主内容区 -->
        <main class="main-content">
            <!-- 页面标题 -->
            <!-- 筛选条件栏 -->
            <!-- 汇总卡片区 -->
            <!-- 工具栏 -->
            <!-- Tab视图区 -->
            <!-- 分页器 -->
        </main>
    </div>
    <!-- 详情弹窗 -->
    <!-- 导入弹窗 -->
    <script>/* JS逻辑 */</script>
</body>
</html>
```

- [ ] **Step 2: 实现侧边栏导航**

```html
<aside class="sidebar">
    <div class="logo">
        <h1>青阳云</h1>
        <span>HRO管理系统</span>
    </div>
    <nav class="nav-section">
        <div class="nav-group">智能薪酬</div>
        <ul class="nav-tree">
            <li class="nav-item"><a class="nav-link" href="qingyang-insurance-archive-optimized.html">员工参保档案</a></li>
            <li class="nav-item"><a class="nav-link active">对账复核</a></li>
            <li class="nav-item"><a class="nav-link" href="qingyang-calculator-scheme.html">社保方案计算</a></li>
        </ul>
    </nav>
</aside>
```

- [ ] **Step 3: 实现页面标题区**

```html
<div class="page-header">
    <div class="page-title">
        <h1>社保对账复核</h1>
        <p class="page-subtitle">核对系统应缴明细与社保局台账差异，定位申报遗漏</p>
    </div>
</div>
```

- [ ] **Step 4: 实现筛选条件栏**

```html
<div class="filter-bar">
    <div class="filter-item">
        <label class="filter-label">费用月份</label>
        <select class="qy-input" id="filterBillingMonth">
            <option value="2026-04" selected>2026-04</option>
            <option value="2026-03">2026-03</option>
        </select>
    </div>
    <div class="filter-item">
        <label class="filter-label">参保主体</label>
        <select class="qy-input" id="filterRegion">
            <option value="">全部</option>
            <option value="changsha">长沙市</option>
        </select>
    </div>
    <div class="filter-item">
        <label class="filter-label">结算主体</label>
        <select class="qy-input" id="filterSettlement">
            <option value="">全部</option>
        </select>
    </div>
    <div class="filter-item">
        <label class="filter-label">险种</label>
        <select class="qy-input" id="filterInsuranceType">
            <option value="">全部</option>
            <option value="养老保险">养老保险</option>
            <option value="医疗保险">医疗保险</option>
            <option value="失业保险">失业保险</option>
            <option value="工伤保险">工伤保险</option>
            <option value="生育保险">生育保险</option>
            <option value="住房公积金">住房公积金</option>
        </select>
    </div>
    <div class="filter-item" style="flex: 1;">
        <label class="filter-label">客户搜索</label>
        <input type="text" class="qy-input" id="filterCustomer" placeholder="输入客户名称搜索">
    </div>
</div>
```

- [ ] **Step 5: 实现汇总卡片区**

```html
<div class="summary-cards">
    <div class="summary-card">
        <div class="summary-card-label">系统记录</div>
        <div class="summary-card-value" id="summarySystemCount">1,256</div>
        <div class="summary-card-sub">应缴人数</div>
        <div class="summary-card-amount" id="summarySystemAmount">¥3,456,789</div>
    </div>
    <div class="summary-card">
        <div class="summary-card-label">社保局台账</div>
        <div class="summary-card-value" id="summaryLedgerCount">—</div>
        <div class="summary-card-sub">实缴人数</div>
        <div class="summary-card-amount" id="summaryLedgerAmount">¥—</div>
    </div>
    <div class="summary-card summary-card--highlight">
        <div class="summary-card-label">差异汇总</div>
        <div class="summary-card-value" id="summaryDiffCount">—</div>
        <div class="summary-card-sub">差异条数</div>
        <div class="summary-card-amount" id="summaryDiffAmount">¥—</div>
    </div>
</div>
```

- [ ] **Step 6: 实现差异类型分布区**

```html
<div class="diff-type-bar">
    <span class="diff-type-label">差异类型分布：</span>
    <span class="diff-type-chip" id="diffTypeSystemOnly">
        <span class="diff-type-chip__dot diff-type-chip__dot--system"></span>
        系统有·台账无 <strong id="diffTypeSystemOnlyCount">0</strong>人
    </span>
    <span class="diff-type-chip" id="diffTypeLedgerOnly">
        <span class="diff-type-chip__dot diff-type-chip__dot--ledger"></span>
        系统无·台账有 <strong id="diffTypeLedgerOnlyCount">0</strong>人
    </span>
    <span class="diff-type-chip" id="diffTypeAmountDiff">
        <span class="diff-type-chip__dot diff-type-chip__dot--amount"></span>
        金额差异 <strong id="diffTypeAmountDiffCount">0</strong>人
    </span>
</div>
```

- [ ] **Step 7: 实现工具栏**

```html
<div class="toolbar">
    <div class="toolbar-left">
        <button class="qy-btn qy-btn--primary" id="btnImportLedger">
            <svg>...</svg> 导入台账Excel
        </button>
    </div>
    <div class="toolbar-right">
        <button class="qy-btn qy-btn--secondary" id="btnExportDiff">
            <svg>...</svg> 导出差异明细
        </button>
        <button class="qy-btn qy-btn--secondary" id="btnViewSystem">
            <svg>...</svg> 查看系统全量
        </button>
        <button class="qy-btn qy-btn--secondary" id="btnViewLedger">
            <svg>...</svg> 查看台账全量
        </button>
    </div>
</div>
```

- [ ] **Step 8: 实现Tab视图切换**

```html
<div class="view-tabs">
    <button class="view-tab view-tab--active" data-tab="diff">差异明细</button>
    <button class="view-tab" data-tab="system">系统全量</button>
    <button class="view-tab" data-tab="ledger">台账全量</button>
</div>
```

- [ ] **Step 9: 实现分页器**

```html
<div class="pagination">
    <span class="pagination__info">共 <strong id="pageTotalCount">0</strong> 条</span>
    <div class="pagination__controls">
        <button class="qy-btn qy-btn--text" id="btnPrevPage" disabled>上一页</button>
        <input type="number" class="qy-input pagination__input" id="inputPageNum" value="1" min="1">
        <span>/ <span id="pageTotal">1</span> 页</span>
        <button class="qy-btn qy-btn--text" id="btnNextPage">下一页</button>
    </div>
    <select class="qy-input pagination__size" id="selectPageSize">
        <option value="10">10条/页</option>
        <option value="20">20条/页</option>
        <option value="50">50条/页</option>
    </select>
</div>
```

- [ ] **Step 10: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): create page skeleton with layout and navigation"
```

---

### Task 2: 实现汇总卡片和差异类型分布的CSS样式

**Files:**
- Modify: `prototype/qingyang-reconciliation.html` (添加CSS样式)

- [ ] **Step 1: 添加汇总卡片样式**

```css
.summary-cards {
    display: flex;
    gap: var(--qy-space-4);
    margin-bottom: var(--qy-space-4);
}

.summary-card {
    flex: 1;
    background: var(--qy-bg-primary);
    border: 1px solid var(--qy-border-light);
    border-radius: var(--qy-radius-lg);
    padding: var(--qy-space-5);
    transition: box-shadow var(--qy-transition-fast);
}

.summary-card:hover {
    box-shadow: var(--qy-shadow-md);
}

.summary-card--highlight {
    border-color: var(--qy-warning-200);
    background: linear-gradient(135deg, var(--qy-warning-50), var(--qy-bg-primary));
}

.summary-card-label {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-muted);
    margin-bottom: var(--qy-space-1);
}

.summary-card-value {
    font-size: 32px;
    font-weight: 700;
    color: var(--qy-text-primary);
    line-height: 1.2;
    font-variant-numeric: tabular-nums;
}

.summary-card-sub {
    font-size: var(--qy-font-size-xs);
    color: var(--qy-text-muted);
    margin-top: var(--qy-space-1);
}

.summary-card-amount {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
    margin-top: var(--qy-space-2);
    font-variant-numeric: tabular-nums;
}
```

- [ ] **Step 2: 添加差异类型分布样式**

```css
.diff-type-bar {
    display: flex;
    align-items: center;
    gap: var(--qy-space-4);
    padding: var(--qy-space-3) var(--qy-space-4);
    background: var(--qy-bg-primary);
    border: 1px solid var(--qy-border-light);
    border-radius: var(--qy-radius-md);
    margin-bottom: var(--qy-space-4);
}

.diff-type-label {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-muted);
}

.diff-type-chip {
    display: flex;
    align-items: center;
    gap: var(--qy-space-2);
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
}

.diff-type-chip strong {
    color: var(--qy-text-primary);
    font-weight: 600;
}

.diff-type-chip__dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.diff-type-chip__dot--system { background: var(--qy-error-500); }
.diff-type-chip__dot--ledger { background: var(--qy-warning-500); }
.diff-type-chip__dot--amount { background: var(--qy-primary-500); }
```

- [ ] **Step 3: 添加工具栏样式**

```css
.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--qy-space-3) 0;
    border-bottom: 1px solid var(--qy-border-light);
    margin-bottom: var(--qy-space-3);
}

.toolbar-left,
.toolbar-right {
    display: flex;
    gap: var(--qy-space-2);
}

.toolbar .qy-btn svg {
    width: 16px;
    height: 16px;
    margin-right: var(--qy-space-1);
}
```

- [ ] **Step 4: 添加Tab切换样式**

```css
.view-tabs {
    display: flex;
    gap: var(--qy-space-1);
    border-bottom: 1px solid var(--qy-border-light);
    margin-bottom: var(--qy-space-4);
}

.view-tab {
    padding: var(--qy-space-3) var(--qy-space-4);
    font-size: var(--qy-font-size-sm);
    font-weight: 500;
    color: var(--qy-text-secondary);
    background: none;
    border: none;
    border-bottom: 2px solid transparent;
    cursor: pointer;
    transition: all var(--qy-transition-fast);
    margin-bottom: -1px;
}

.view-tab:hover {
    color: var(--qy-text-primary);
}

.view-tab--active {
    color: var(--qy-primary-600);
    border-bottom-color: var(--qy-primary-500);
}
```

- [ ] **Step 5: 添加分页器样式**

```css
.pagination {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--qy-space-4) 0;
    border-top: 1px solid var(--qy-border-light);
    margin-top: var(--qy-space-4);
}

.pagination__info {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-muted);
}

.pagination__controls {
    display: flex;
    align-items: center;
    gap: var(--qy-space-2);
}

.pagination__input {
    width: 50px;
    text-align: center;
    padding: var(--qy-space-1) var(--qy-space-2);
}

.pagination__size {
    width: 100px;
}
```

- [ ] **Step 6: 添加页面标题和筛选栏样式**

```css
.page-header {
    padding: var(--qy-space-5) var(--qy-space-6);
    background: var(--qy-bg-primary);
    border-bottom: 1px solid var(--qy-border-light);
}

.page-title h1 {
    font-size: var(--qy-font-size-xl);
    font-weight: 600;
    color: var(--qy-text-primary);
}

.page-subtitle {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-muted);
    margin-top: var(--qy-space-1);
}

.filter-bar {
    display: flex;
    flex-wrap: wrap;
    gap: var(--qy-space-4);
    padding: var(--qy-space-4) var(--qy-space-6);
    background: var(--qy-bg-primary);
    border-bottom: 1px solid var(--qy-border-light);
}

.filter-bar .filter-item {
    min-width: 140px;
}

.filter-bar .filter-item:last-child {
    min-width: 200px;
}
```

- [ ] **Step 7: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): add CSS styles for summary cards, tabs, pagination"
```

---

### Task 3: 实现差异明细表格

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加差异明细表格HTML**

```html
<div class="data-table-container">
    <table class="qy-table data-table">
        <thead>
            <tr>
                <th style="width: 90px;">费用月份</th>
                <th style="width: 80px;">姓名</th>
                <th style="width: 150px;">身份证</th>
                <th style="width: 120px;">客户</th>
                <th style="width: 90px;">险种</th>
                <th style="width: 90px;" class="text-right">系统基数</th>
                <th style="width: 100px;" class="text-right">系统金额</th>
                <th style="width: 90px;" class="text-right">台账基数</th>
                <th style="width: 100px;" class="text-right">台账金额</th>
                <th style="width: 80px;" class="text-right">差异额</th>
                <th style="width: 90px;">系统状态</th>
                <th style="width: 80px;">差异类型</th>
                <th style="width: 80px;">操作</th>
            </tr>
        </thead>
        <tbody id="diffTableBody">
            <!-- 动态渲染 -->
        </tbody>
    </table>
</div>
```

- [ ] **Step 2: 添加表格样式**

```css
.data-table-container {
    background: var(--qy-bg-primary);
    border: 1px solid var(--qy-border-light);
    border-radius: var(--qy-radius-lg);
    overflow: hidden;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: var(--qy-space-3) var(--qy-space-4);
    text-align: left;
    font-size: var(--qy-font-size-sm);
    border-bottom: 1px solid var(--qy-border-light);
}

.data-table th {
    background: var(--qy-bg-secondary);
    font-weight: 600;
    color: var(--qy-text-muted);
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.5px;
}

.data-table tbody tr:hover {
    background: var(--qy-bg-secondary);
}

.data-table tbody tr:last-child td {
    border-bottom: none;
}

.text-right {
    text-align: right !important;
}

/* 差异类型标签 */
.diff-type-tag {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: var(--qy-radius-full);
    font-size: var(--qy-font-size-xs);
    font-weight: 500;
}

.diff-type-tag--system {
    background: var(--qy-error-50);
    color: var(--qy-error-600);
}

.diff-type-tag--ledger {
    background: var(--qy-warning-50);
    color: var(--qy-warning-600);
}

.diff-type-tag--amount {
    background: var(--qy-primary-50);
    color: var(--qy-primary-600);
}

/* 金额样式 */
.amount {
    font-variant-numeric: tabular-nums;
}

.amount--positive {
    color: var(--qy-error-600);
}

.amount--negative {
    color: var(--qy-success-600);
}

.amount--zero {
    color: var(--qy-text-muted);
}

/* 操作按钮 */
.action-btn {
    padding: 4px 12px;
    font-size: var(--qy-font-size-xs);
    font-weight: 500;
    border-radius: var(--qy-radius-md);
    border: none;
    cursor: pointer;
    transition: all var(--qy-transition-fast);
}

.action-btn--primary {
    background: var(--qy-primary-50);
    color: var(--qy-primary-600);
}

.action-btn--primary:hover {
    background: var(--qy-primary-100);
}
```

- [ ] **Step 3: 添加系统全量表格HTML**

```html
<div class="data-table-container" id="systemTableContainer" style="display: none;">
    <table class="qy-table data-table">
        <thead>
            <tr>
                <th style="width: 80px;">姓名</th>
                <th style="width: 150px;">身份证</th>
                <th style="width: 120px;">客户</th>
                <th style="width: 90px;">险种</th>
                <th style="width: 90px;" class="text-right">缴费基数</th>
                <th style="width: 100px;" class="text-right">单位缴费</th>
                <th style="width: 100px;" class="text-right">个人缴费</th>
                <th style="width: 90px;">申报状态</th>
                <th style="width: 90px;">申报时间</th>
            </tr>
        </thead>
        <tbody id="systemTableBody">
            <!-- 动态渲染 -->
        </tbody>
    </table>
</div>
```

- [ ] **Step 4: 添加台账全量表格HTML**

```html
<div class="data-table-container" id="ledgerTableContainer" style="display: none;">
    <table class="qy-table data-table">
        <thead>
            <tr>
                <th style="width: 80px;">姓名</th>
                <th style="width: 150px;">身份证</th>
                <th style="width: 90px;">险种</th>
                <th style="width: 90px;" class="text-right">缴费基数</th>
                <th style="width: 100px;" class="text-right">单位缴费</th>
                <th style="width: 100px;" class="text-right">个人缴费</th>
                <th style="width: 90px;">费用月份</th>
            </tr>
        </thead>
        <tbody id="ledgerTableBody">
            <!-- 动态渲染 -->
        </tbody>
    </table>
</div>
```

- [ ] **Step 5: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): add data tables for diff, system, and ledger views"
```

---

### Task 4: 实现差异详情弹窗

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加弹窗HTML**

```html
<div class="modal-overlay" id="detailModal" style="display: none;">
    <div class="modal" style="max-width: 600px;">
        <div class="modal__header">
            <h3 class="modal__title" id="detailModalTitle">差异详情：张三 - 2026年4月 - 养老保险</h3>
            <button class="modal__close" id="detailModalClose">&times;</button>
        </div>
        <div class="modal__body">
            <div class="detail-compare">
                <div class="detail-compare__col">
                    <div class="detail-compare__header">系统记录</div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">客户</span>
                        <span class="detail-compare__value" id="detailCustomer">某科技有限公司</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">参保方案</span>
                        <span class="detail-compare__value" id="detailScheme">长沙标准方案</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">缴费基数</span>
                        <span class="detail-compare__value" id="detailSystemBase">6,000</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">单位缴费</span>
                        <span class="detail-compare__value" id="detailSystemCompany">¥1,234</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">个人缴费</span>
                        <span class="detail-compare__value" id="detailSystemPersonal">¥480</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">申报状态</span>
                        <span class="detail-compare__value" id="detailStatus">申报成功</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">申报时间</span>
                        <span class="detail-compare__value" id="detailDeclareDate">2026-04-05</span>
                    </div>
                </div>
                <div class="detail-compare__col">
                    <div class="detail-compare__header">社保局台账</div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label" style="color: var(--qy-text-muted);">客户</span>
                        <span class="detail-compare__value" style="color: var(--qy-text-muted);">（台账不显示客户）</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label" style="color: var(--qy-text-muted);">参保方案</span>
                        <span class="detail-compare__value" style="color: var(--qy-text-muted);">—</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">缴费基数</span>
                        <span class="detail-compare__value" id="detailLedgerBase">6,000</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">单位缴费</span>
                        <span class="detail-compare__value" id="detailLedgerCompany">¥1,200</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label">个人缴费</span>
                        <span class="detail-compare__value" id="detailLedgerPersonal">¥480</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label" style="color: var(--qy-text-muted);">申报状态</span>
                        <span class="detail-compare__value" style="color: var(--qy-text-muted);">（台账无状态字段）</span>
                    </div>
                    <div class="detail-compare__row">
                        <span class="detail-compare__label" style="color: var(--qy-text-muted);">申报时间</span>
                        <span class="detail-compare__value" style="color: var(--qy-text-muted);">—</span>
                    </div>
                </div>
            </div>
            <div class="detail-analysis">
                <div class="detail-analysis__title">差异分析</div>
                <div class="detail-analysis__content" id="detailAnalysis">
                    金额差异：<strong id="detailDiffAmount">¥34</strong>（单位缴差额）
                </div>
            </div>
        </div>
        <div class="modal__footer">
            <button class="qy-btn qy-btn--secondary" id="btnMarkChecked">标记已核查</button>
            <button class="qy-btn qy-btn--secondary" id="btnAdjustRecord">调整系统记录</button>
            <button class="qy-btn qy-btn--primary" id="btnCloseDetail">关闭</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 添加弹窗样式**

```css
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal {
    background: var(--qy-bg-primary);
    border-radius: var(--qy-radius-lg);
    box-shadow: var(--qy-shadow-xl);
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

.modal__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--qy-space-4) var(--qy-space-5);
    border-bottom: 1px solid var(--qy-border-light);
}

.modal__title {
    font-size: var(--qy-font-size-lg);
    font-weight: 600;
    color: var(--qy-text-primary);
}

.modal__close {
    width: 32px;
    height: 32px;
    border: none;
    background: none;
    font-size: 24px;
    color: var(--qy-text-muted);
    cursor: pointer;
    border-radius: var(--qy-radius-md);
    transition: all var(--qy-transition-fast);
}

.modal__close:hover {
    background: var(--qy-bg-secondary);
    color: var(--qy-text-primary);
}

.modal__body {
    padding: var(--qy-space-5);
    overflow-y: auto;
    flex: 1;
}

.modal__footer {
    display: flex;
    justify-content: flex-end;
    gap: var(--qy-space-2);
    padding: var(--qy-space-4) var(--qy-space-5);
    border-top: 1px solid var(--qy-border-light);
}

/* 对比区域 */
.detail-compare {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--qy-space-4);
    margin-bottom: var(--qy-space-5);
}

.detail-compare__header {
    font-size: var(--qy-font-size-sm);
    font-weight: 600;
    color: var(--qy-text-primary);
    padding-bottom: var(--qy-space-2);
    margin-bottom: var(--qy-space-2);
    border-bottom: 1px solid var(--qy-border-light);
}

.detail-compare__col:first-child .detail-compare__header {
    color: var(--qy-primary-600);
}

.detail-compare__row {
    display: flex;
    justify-content: space-between;
    padding: var(--qy-space-2) 0;
    font-size: var(--qy-font-size-sm);
}

.detail-compare__label {
    color: var(--qy-text-muted);
}

.detail-compare__value {
    color: var(--qy-text-primary);
    font-weight: 500;
}

/* 差异分析 */
.detail-analysis {
    background: var(--qy-bg-secondary);
    border-radius: var(--qy-radius-md);
    padding: var(--qy-space-4);
}

.detail-analysis__title {
    font-size: var(--qy-font-size-sm);
    font-weight: 600;
    color: var(--qy-text-primary);
    margin-bottom: var(--qy-space-2);
}

.detail-analysis__content {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
    line-height: 1.6;
}
```

- [ ] **Step 3: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): add detail modal for viewing record differences"
```

---

### Task 5: 实现导入弹窗和文件上传

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加导入弹窗HTML**

```html
<div class="modal-overlay" id="importModal" style="display: none;">
    <div class="modal" style="max-width: 500px;">
        <div class="modal__header">
            <h3 class="modal__title">导入社保局台账</h3>
            <button class="modal__close" id="importModalClose">&times;</button>
        </div>
        <div class="modal__body">
            <div class="import-info">
                <div class="import-info__icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                        <polyline points="17 8 12 3 7 8"/>
                        <line x1="12" y1="3" x2="12" y2="15"/>
                    </svg>
                </div>
                <div class="import-info__title">上传台账文件</div>
                <div class="import-info__desc">支持 .xlsx、.xls、.csv 格式</div>
                <div class="import-info__format">
                    必填字段：姓名、身份证号、险种、费用月份、<br>
                    缴费基数、单位缴费额、个人缴费额
                </div>
            </div>
            <div class="import-dropzone" id="importDropzone">
                <input type="file" id="importFileInput" accept=".xlsx,.xls,.csv" style="display: none;">
                <div class="import-dropzone__text">
                    拖拽文件到此处，或 <label for="importFileInput" class="import-dropzone__link">点击上传</label>
                </div>
            </div>
            <div class="import-preview" id="importPreview" style="display: none;">
                <div class="import-preview__file">
                    <span class="import-preview__icon">📄</span>
                    <span class="import-preview__name" id="importFileName">台账数据.xlsx</span>
                    <span class="import-preview__size" id="importFileSize">12.5 KB</span>
                </div>
                <div class="import-preview__sheet">
                    <label>请选择工作表：</label>
                    <select class="qy-input" id="importSheetSelect">
                        <!-- 动态填充 -->
                    </select>
                </div>
                <div class="import-preview__count">
                    共 <strong id="importRowCount">0</strong> 条记录
                </div>
            </div>
            <div class="import-error" id="importError" style="display: none;">
                <strong>导入失败：</strong>
                <span id="importErrorMsg"></span>
            </div>
        </div>
        <div class="modal__footer">
            <button class="qy-btn qy-btn--secondary" id="btnCancelImport">取消</button>
            <button class="qy-btn qy-btn--primary" id="btnConfirmImport" disabled>确认导入</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 添加导入弹窗样式**

```css
.import-info {
    text-align: center;
    margin-bottom: var(--qy-space-5);
}

.import-info__icon {
    color: var(--qy-primary-400);
    margin-bottom: var(--qy-space-3);
}

.import-info__title {
    font-size: var(--qy-font-size-lg);
    font-weight: 600;
    color: var(--qy-text-primary);
    margin-bottom: var(--qy-space-1);
}

.import-info__desc {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-muted);
    margin-bottom: var(--qy-space-2);
}

.import-info__format {
    font-size: var(--qy-font-size-xs);
    color: var(--qy-text-muted);
    background: var(--qy-bg-secondary);
    padding: var(--qy-space-2) var(--qy-space-3);
    border-radius: var(--qy-radius-md);
    display: inline-block;
}

.import-dropzone {
    border: 2px dashed var(--qy-border-medium);
    border-radius: var(--qy-radius-lg);
    padding: var(--qy-space-6);
    text-align: center;
    transition: all var(--qy-transition-fast);
    cursor: pointer;
}

.import-dropzone:hover,
.import-dropzone--active {
    border-color: var(--qy-primary-400);
    background: var(--qy-primary-50);
}

.import-dropzone__text {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
}

.import-dropzone__link {
    color: var(--qy-primary-600);
    cursor: pointer;
    text-decoration: underline;
}

.import-preview {
    margin-top: var(--qy-space-4);
}

.import-preview__file {
    display: flex;
    align-items: center;
    gap: var(--qy-space-2);
    padding: var(--qy-space-3);
    background: var(--qy-bg-secondary);
    border-radius: var(--qy-radius-md);
    margin-bottom: var(--qy-space-3);
}

.import-preview__icon {
    font-size: 20px;
}

.import-preview__name {
    flex: 1;
    font-size: var(--qy-font-size-sm);
    font-weight: 500;
    color: var(--qy-text-primary);
}

.import-preview__size {
    font-size: var(--qy-font-size-xs);
    color: var(--qy-text-muted);
}

.import-preview__sheet {
    display: flex;
    align-items: center;
    gap: var(--qy-space-2);
    margin-bottom: var(--qy-space-3);
}

.import-preview__sheet label {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
}

.import-preview__sheet select {
    flex: 1;
}

.import-preview__count {
    font-size: var(--qy-font-size-sm);
    color: var(--qy-text-secondary);
    text-align: center;
}

.import-error {
    margin-top: var(--qy-space-3);
    padding: var(--qy-space-3);
    background: var(--qy-error-50);
    border: 1px solid var(--qy-error-200);
    border-radius: var(--qy-radius-md);
    font-size: var(--qy-font-size-sm);
    color: var(--qy-error-600);
}
```

- [ ] **Step 3: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): add import modal for ledger Excel upload"
```

---

### Task 6: 实现JavaScript核心逻辑

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加模拟数据**

```javascript
// 系统记录模拟数据
const SYSTEM_RECORDS = [
    {
        id: 'sys_001',
        name: '张三',
        idCard: '430105199001011234',
        customer: '某科技有限公司',
        settlement: '结算主体A',
        scheme: '长沙标准方案',
        insuranceType: '养老保险',
        baseAmount: 6000,
        companyFee: 1234,
        personalFee: 480,
        declareStatus: '申报成功',
        declareDate: '2026-04-05',
        billingMonth: '2026-04'
    },
    {
        id: 'sys_002',
        name: '张三',
        idCard: '430105199001011234',
        customer: '某科技有限公司',
        settlement: '结算主体A',
        scheme: '长沙标准方案',
        insuranceType: '医疗保险',
        baseAmount: 6000,
        companyFee: 600,
        personalFee: 200,
        declareStatus: '申报失败',
        declareDate: '',
        billingMonth: '2026-04'
    },
    {
        id: 'sys_003',
        name: '李四',
        idCard: '430106199102022345',
        customer: '某科技有限公司',
        settlement: '结算主体A',
        scheme: '长沙标准方案',
        insuranceType: '养老保险',
        baseAmount: 4500,
        companyFee: 925,
        personalFee: 360,
        declareStatus: '申报成功',
        declareDate: '2026-04-08',
        billingMonth: '2026-04'
    },
    {
        id: 'sys_004',
        name: '王五',
        idCard: '430107199203033456',
        customer: '另一家公司',
        settlement: '结算主体B',
        scheme: '长沙标准方案',
        insuranceType: '住房公积金',
        baseAmount: 3000,
        companyFee: 300,
        personalFee: 300,
        declareStatus: '待申报',
        declareDate: '',
        billingMonth: '2026-04'
    },
    {
        id: 'sys_005',
        name: '赵六',
        idCard: '430108199304044567',
        customer: '第三家公司',
        settlement: '结算主体A',
        scheme: '长沙低收入的方案',
        insuranceType: '养老保险',
        baseAmount: 8000,
        companyFee: 1648,
        personalFee: 640,
        declareStatus: '申报成功',
        declareDate: '2026-04-10',
        billingMonth: '2026-04'
    }
];

// 台账记录（从Excel导入）
let LEDGER_RECORDS = [];

// 差异记录
let DIFFERENCE_RECORDS = [];

// 差异类型枚举
const DIFF_TYPE = {
    SYSTEM_ONLY: 'system',    // 系统有，台账无
    LEDGER_ONLY: 'ledger',    // 台账有，系统无
    AMOUNT_DIFF: 'amount'     // 金额差异
};
```

- [ ] **Step 2: 实现筛选和计算逻辑**

```javascript
// 当前筛选状态
const currentFilters = {
    billingMonth: '2026-04',
    region: '',
    settlement: '',
    insuranceType: '',
    customer: ''
};

// 分页状态
const pagination = {
    page: 1,
    pageSize: 10,
    total: 0
};

// 获取筛选后的系统记录
function getFilteredSystemRecords() {
    return SYSTEM_RECORDS.filter(record => {
        if (currentFilters.billingMonth && record.billingMonth !== currentFilters.billingMonth) return false;
        if (currentFilters.region && record.region !== currentFilters.region) return false;
        if (currentFilters.settlement && record.settlement !== currentFilters.settlement) return false;
        if (currentFilters.insuranceType && record.insuranceType !== currentFilters.insuranceType) return false;
        if (currentFilters.customer && !record.customer.includes(currentFilters.customer)) return false;
        return true;
    });
}

// 计算差异
function calculateDifferences() {
    DIFFERENCE_RECORDS = [];
    
    const systemMap = new Map();
    getFilteredSystemRecords().forEach(record => {
        const key = `${record.idCard}_${record.insuranceType}_${record.billingMonth}`;
        systemMap.set(key, record);
    });
    
    const ledgerMap = new Map();
    LEDGER_RECORDS.forEach(record => {
        const key = `${record.idCard}_${record.insuranceType}_${record.billingMonth}`;
        if (!ledgerMap.has(key)) {
            ledgerMap.set(key, record);
        } else {
            // 同一记录取金额最大
            const existing = ledgerMap.get(key);
            const existingTotal = existing.companyFee + existing.personalFee;
            const newTotal = record.companyFee + record.personalFee;
            if (newTotal > existingTotal) {
                ledgerMap.set(key, record);
            }
        }
    });
    
    // 系统有，台账无
    systemMap.forEach((sysRecord, key) => {
        if (!ledgerMap.has(key)) {
            DIFFERENCE_RECORDS.push({
                id: `diff_${key}`,
                diffType: DIFF_TYPE.SYSTEM_ONLY,
                systemRecord: sysRecord,
                ledgerRecord: null,
                diffAmount: sysRecord.companyFee + sysRecord.personalFee,
                billingMonth: sysRecord.billingMonth
            });
        }
    });
    
    // 台账有，系统无
    ledgerMap.forEach((ledgerRecord, key) => {
        if (!systemMap.has(key)) {
            DIFFERENCE_RECORDS.push({
                id: `diff_${key}`,
                diffType: DIFF_TYPE.LEDGER_ONLY,
                systemRecord: null,
                ledgerRecord: ledgerRecord,
                diffAmount: -(ledgerRecord.companyFee + ledgerRecord.personalFee),
                billingMonth: ledgerRecord.billingMonth
            });
        }
    });
    
    // 金额差异
    systemMap.forEach((sysRecord, key) => {
        if (ledgerMap.has(key)) {
            const ledgerRecord = ledgerMap.get(key);
            const sysTotal = sysRecord.companyFee + sysRecord.personalFee;
            const ledgerTotal = ledgerRecord.companyFee + ledgerRecord.personalFee;
            if (sysTotal !== ledgerTotal) {
                DIFFERENCE_RECORDS.push({
                    id: `diff_${key}`,
                    diffType: DIFF_TYPE.AMOUNT_DIFF,
                    systemRecord: sysRecord,
                    ledgerRecord: ledgerRecord,
                    diffAmount: sysTotal - ledgerTotal,
                    billingMonth: sysRecord.billingMonth
                });
            }
        }
    });
    
    return DIFFERENCE_RECORDS;
}
```

- [ ] **Step 3: 实现渲染逻辑**

```javascript
// 格式化金额
function formatMoney(amount) {
    return '¥' + amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

// 渲染汇总卡片
function renderSummaryCards() {
    const systemRecords = getFilteredSystemRecords();
    const systemCount = new Set(systemRecords.map(r => `${r.idCard}_${r.insuranceType}`)).size;
    const systemAmount = systemRecords.reduce((sum, r) => sum + r.companyFee + r.personalFee, 0);
    
    const ledgerCount = new Set(LEDGER_RECORDS.map(r => `${r.idCard}_${r.insuranceType}`)).size;
    const ledgerAmount = LEDGER_RECORDS.reduce((sum, r) => sum + r.companyFee + r.personalFee, 0);
    
    document.getElementById('summarySystemCount').textContent = systemCount.toLocaleString();
    document.getElementById('summarySystemAmount').textContent = formatMoney(systemAmount);
    
    if (LEDGER_RECORDS.length > 0) {
        document.getElementById('summaryLedgerCount').textContent = ledgerCount.toLocaleString();
        document.getElementById('summaryLedgerAmount').textContent = formatMoney(ledgerAmount);
    }
    
    const diffs = calculateDifferences();
    const diffCount = diffs.length;
    const diffAmount = diffs.reduce((sum, d) => sum + d.diffAmount, 0);
    const diffAmountAbs = Math.abs(diffAmount);
    
    document.getElementById('summaryDiffCount').textContent = diffCount.toLocaleString();
    document.getElementById('summaryDiffAmount').textContent = (diffAmount < 0 ? '-' : '') + formatMoney(diffAmountAbs);
    
    // 差异类型分布
    const systemOnlyCount = diffs.filter(d => d.diffType === DIFF_TYPE.SYSTEM_ONLY).length;
    const ledgerOnlyCount = diffs.filter(d => d.diffType === DIFF_TYPE.LEDGER_ONLY).length;
    const amountDiffCount = diffs.filter(d => d.diffType === DIFF_TYPE.AMOUNT_DIFF).length;
    
    document.getElementById('diffTypeSystemOnlyCount').textContent = systemOnlyCount;
    document.getElementById('diffTypeLedgerOnlyCount').textContent = ledgerOnlyCount;
    document.getElementById('diffTypeAmountDiffCount').textContent = amountDiffCount;
}
```

- [ ] **Step 4: 实现表格渲染**

```javascript
// 当前激活的Tab
let currentTab = 'diff';

// 渲染差异明细表
function renderDiffTable() {
    const tbody = document.getElementById('diffTableBody');
    const diffs = calculateDifferences();
    
    // 分页
    const start = (pagination.page - 1) * pagination.pageSize;
    const end = start + pagination.pageSize;
    const pageData = diffs.slice(start, end);
    
    if (pageData.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="13" style="text-align: center; padding: 40px; color: var(--qy-text-muted);">
                    暂无差异数据，请先导入台账进行比对
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = pageData.map(diff => {
        const sysRecord = diff.systemRecord;
        const ledgerRecord = diff.ledgerRecord;
        const diffTypeLabel = {
            [DIFF_TYPE.SYSTEM_ONLY]: '系统多',
            [DIFF_TYPE.LEDGER_ONLY]: '台账多',
            [DIFF_TYPE.AMOUNT_DIFF]: '金额差'
        }[diff.diffType];
        
        const diffTypeClass = {
            [DIFF_TYPE.SYSTEM_ONLY]: 'diff-type-tag--system',
            [DIFF_TYPE.LEDGER_ONLY]: 'diff-type-tag--ledger',
            [DIFF_TYPE.AMOUNT_DIFF]: 'diff-type-tag--amount'
        }[diff.diffType];
        
        const amountClass = diff.diffAmount > 0 ? 'amount--positive' : diff.diffAmount < 0 ? 'amount--negative' : 'amount--zero';
        
        return `
            <tr>
                <td>${diff.billingMonth}</td>
                <td>${sysRecord ? sysRecord.name : (ledgerRecord ? ledgerRecord.name : '-')}</td>
                <td>${maskIdCard(sysRecord ? sysRecord.idCard : (ledgerRecord ? ledgerRecord.idCard : ''))}</td>
                <td>${sysRecord ? sysRecord.customer : '-'}</td>
                <td>${sysRecord ? sysRecord.insuranceType : (ledgerRecord ? ledgerRecord.insuranceType : '-')}</td>
                <td class="text-right">${sysRecord ? sysRecord.baseAmount.toLocaleString() : '-'}</td>
                <td class="text-right">${sysRecord ? formatMoney(sysRecord.companyFee + sysRecord.personalFee) : '-'}</td>
                <td class="text-right">${ledgerRecord ? ledgerRecord.baseAmount.toLocaleString() : '-'}</td>
                <td class="text-right">${ledgerRecord ? formatMoney(ledgerRecord.companyFee + ledgerRecord.personalFee) : '-'}</td>
                <td class="text-right amount ${amountClass}">${formatMoney(Math.abs(diff.diffAmount))}</td>
                <td>${sysRecord ? sysRecord.declareStatus : '-'}</td>
                <td><span class="diff-type-tag ${diffTypeClass}">${diffTypeLabel}</span></td>
                <td><button class="action-btn action-btn--primary" onclick="showDetail('${diff.id}')">查看详情</button></td>
            </tr>
        `;
    }).join('');
    
    pagination.total = diffs.length;
    renderPagination();
}

// 身份证号脱敏
function maskIdCard(idCard) {
    if (!idCard) return '-';
    return idCard.replace(/(\d{3})\d{11}(\d{4})/, '$1***********$2');
}
```

- [ ] **Step 5: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): implement core JS logic for filtering, diff calculation, and rendering"
```

---

### Task 7: 实现Excel导入功能（使用SheetJS）

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加SheetJS CDN**

```html
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
```

- [ ] **Step 2: 实现文件读取和解析**

```javascript
// 处理文件选择
document.getElementById('importFileInput').addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    try {
        const data = await readFileAsync(file);
        const workbook = XLSX.read(data, { type: 'array' });
        
        // 显示预览
        document.getElementById('importPreview').style.display = 'block';
        document.getElementById('importFileName').textContent = file.name;
        document.getElementById('importFileSize').textContent = formatFileSize(file.size);
        
        // 填充工作表选择
        const sheetSelect = document.getElementById('importSheetSelect');
        sheetSelect.innerHTML = workbook.SheetNames.map(name => 
            `<option value="${name}">${name}</option>`
        ).join('');
        
        // 默认选择第一个工作表
        if (workbook.SheetNames.length > 0) {
            updateRowCount(workbook.Sheets[workbook.SheetNames[0]]);
        }
        
        document.getElementById('btnConfirmImport').disabled = false;
        document.getElementById('importError').style.display = 'none';
        
    } catch (error) {
        showImportError('文件读取失败：' + error.message);
    }
});

// 读取文件为ArrayBuffer
function readFileAsync(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(new Uint8Array(e.target.result));
        reader.onerror = reject;
        reader.readAsArrayBuffer(file);
    });
}

// 更新行数显示
function updateRowCount(sheet) {
    const data = XLSX.utils.sheet_to_json(sheet);
    document.getElementById('importRowCount').textContent = data.length;
}

// 格式化文件大小
function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
```

- [ ] **Step 3: 实现Excel到台账记录的映射**

```javascript
// Excel列名映射
const COLUMN_MAPPING = {
    '姓名': 'name',
    '证件号码': 'idCard',
    '身份证号': 'idCard',
    '险种': 'insuranceType',
    '险种名称': 'insuranceType',
    '费用月份': 'billingMonth',
    '费款所属期': 'billingMonth',
    '申报月份': 'billingMonth',
    '缴费基数': 'baseAmount',
    '申报工资': 'baseAmount',
    '单位缴费额': 'companyFee',
    '单位缴费金额': 'companyFee',
    '单位实缴': 'companyFee',
    '个人缴费额': 'personalFee',
    '个人缴费金额': 'personalFee',
    '个人实缴': 'personalFee'
};

// 标准险种枚举
const INSURANCE_TYPES = ['养老保险', '医疗保险', '失业保险', '工伤保险', '生育保险', '住房公积金'];

// 导入确认
document.getElementById('btnConfirmImport').addEventListener('click', () => {
    const fileInput = document.getElementById('importFileInput');
    if (!fileInput.files[0]) return;
    
    const sheetName = document.getElementById('importSheetSelect').value;
    importLedgerData(fileInput.files[0], sheetName);
});

async function importLedgerData(file, sheetName) {
    try {
        const data = await readFileAsync(file);
        const workbook = XLSX.read(data, { type: 'array' });
        const sheet = workbook.Sheets[sheetName];
        const rawData = XLSX.utils.sheet_to_json(sheet);
        
        // 转换和校验
        LEDGER_RECORDS = [];
        const errors = [];
        
        rawData.forEach((row, index) => {
            const record = normalizeRow(row, index, errors);
            if (record) {
                LEDGER_RECORDS.push(record);
            }
        });
        
        if (errors.length > 0) {
            showImportError(`发现 ${errors.length} 个错误：\n` + errors.slice(0, 5).join('\n'));
            return;
        }
        
        // 关闭弹窗
        closeImportModal();
        
        // 重新渲染
        renderAll();
        
        showToast(`成功导入 ${LEDGER_RECORDS.length} 条记录`);
        
    } catch (error) {
        showImportError('导入失败：' + error.message);
    }
}

// 标准化行数据
function normalizeRow(row, index, errors) {
    // 获取身份证号
    const idCard = findField(row, ['身份证号', '证件号码']);
    if (!idCard) {
        errors.push(`第${index + 2}行：缺少身份证号`);
        return null;
    }
    
    // 获取险种
    const insuranceType = findField(row, ['险种', '险种名称']);
    if (!insuranceType || !INSURANCE_TYPES.includes(insuranceType)) {
        errors.push(`第${index + 2}行：险种"${insuranceType}"不在标准枚举中`);
        return null;
    }
    
    // 获取费用月份
    let billingMonth = findField(row, ['费用月份', '费款所属期', '申报月份']);
    if (!billingMonth) {
        errors.push(`第${index + 2}行：缺少费用月份`);
        return null;
    }
    billingMonth = normalizeBillingMonth(billingMonth);
    
    // 获取金额字段
    const baseAmount = parseFloat(findField(row, ['缴费基数', '申报工资'])) || 0;
    const companyFee = parseFloat(findField(row, ['单位缴费额', '单位缴费金额', '单位实缴'])) || 0;
    const personalFee = parseFloat(findField(row, ['个人缴费额', '个人缴费金额', '个人实缴'])) || 0;
    
    return {
        id: `ledger_${index}`,
        name: findField(row, ['姓名']) || '',
        idCard: String(idCard).trim(),
        insuranceType,
        billingMonth,
        baseAmount,
        companyFee,
        personalFee
    };
}

// 查找字段（兼容多种列名）
function findField(row, fields) {
    for (const field of fields) {
        if (row[field] !== undefined) {
            return String(row[field]).trim();
        }
    }
    return null;
}

// 标准化费用月份格式
function normalizeBillingMonth(value) {
    if (!value) return null;
    // 处理 "2026-04" 或 "2026/04" 或 "202604"
    const str = String(value).replace(/\//, '-');
    if (/^\d{4}-\d{2}$/.test(str)) return str;
    if (/^\d{6}$/.test(str)) return str.slice(0, 4) + '-' + str.slice(4, 6);
    return null;
}
```

- [ ] **Step 4: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): implement Excel import with SheetJS"
```

---

### Task 8: 实现Excel导出功能和弹窗交互

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 实现导出差异明细**

```javascript
document.getElementById('btnExportDiff').addEventListener('click', () => {
    const diffs = calculateDifferences();
    if (diffs.length === 0) {
        showToast('暂无差异数据可导出', 'warning');
        return;
    }
    
    const exportData = diffs.map(diff => {
        const sysRecord = diff.systemRecord;
        const ledgerRecord = diff.ledgerRecord;
        
        return {
            '费用月份': diff.billingMonth,
            '姓名': sysRecord ? sysRecord.name : (ledgerRecord ? ledgerRecord.name : ''),
            '身份证号': sysRecord ? sysRecord.idCard : (ledgerRecord ? ledgerRecord.idCard : ''),
            '客户': sysRecord ? sysRecord.customer : '-',
            '险种': sysRecord ? sysRecord.insuranceType : (ledgerRecord ? ledgerRecord.insuranceType : ''),
            '系统基数': sysRecord ? sysRecord.baseAmount : '-',
            '系统单位缴': sysRecord ? sysRecord.companyFee : '-',
            '系统个人缴': sysRecord ? sysRecord.personalFee : '-',
            '台账基数': ledgerRecord ? ledgerRecord.baseAmount : '-',
            '台账单位缴': ledgerRecord ? ledgerRecord.companyFee : '-',
            '台账个人缴': ledgerRecord ? ledgerRecord.personalFee : '-',
            '差异额': Math.abs(diff.diffAmount),
            '差异类型': {
                [DIFF_TYPE.SYSTEM_ONLY]: '系统多',
                [DIFF_TYPE.LEDGER_ONLY]: '台账多',
                [DIFF_TYPE.AMOUNT_DIFF]: '金额差异'
            }[diff.diffType],
            '系统状态': sysRecord ? sysRecord.declareStatus : '-'
        };
    });
    
    const ws = XLSX.utils.json_to_sheet(exportData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, '差异明细');
    
    const fileName = `社保台账差异_${currentFilters.billingMonth}_${new Date().toISOString().slice(0, 10)}.xlsx`;
    XLSX.writeFile(wb, fileName);
    
    showToast(`已导出 ${exportData.length} 条差异记录`);
});
```

- [ ] **Step 2: 实现Tab切换逻辑**

```javascript
// Tab切换
document.querySelectorAll('.view-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        switchTab(tabName);
    });
});

function switchTab(tabName) {
    currentTab = tabName;
    
    // 更新Tab样式
    document.querySelectorAll('.view-tab').forEach(t => {
        t.classList.toggle('view-tab--active', t.dataset.tab === tabName);
    });
    
    // 显示/隐藏表格
    document.getElementById('diffTableContainer').style.display = tabName === 'diff' ? 'block' : 'none';
    document.getElementById('systemTableContainer').style.display = tabName === 'system' ? 'block' : 'none';
    document.getElementById('ledgerTableContainer').style.display = tabName === 'ledger' ? 'block' : 'none';
    
    // 重置到第一页
    pagination.page = 1;
    
    // 渲染对应表格
    if (tabName === 'diff') {
        renderDiffTable();
    } else if (tabName === 'system') {
        renderSystemTable();
    } else if (tabName === 'ledger') {
        renderLedgerTable();
    }
}
```

- [ ] **Step 3: 实现详情弹窗**

```javascript
// 显示详情弹窗
function showDetail(diffId) {
    const diff = DIFFERENCE_RECORDS.find(d => d.id === diffId);
    if (!diff) return;
    
    const sysRecord = diff.systemRecord;
    const ledgerRecord = diff.ledgerRecord;
    
    // 填充标题
    const name = sysRecord ? sysRecord.name : (ledgerRecord ? ledgerRecord.name : '');
    const insuranceType = sysRecord ? sysRecord.insuranceType : (ledgerRecord ? ledgerRecord.insuranceType : '');
    document.getElementById('detailModalTitle').textContent = `差异详情：${name} - ${diff.billingMonth} - ${insuranceType}`;
    
    // 填充系统记录
    if (sysRecord) {
        document.getElementById('detailCustomer').textContent = sysRecord.customer;
        document.getElementById('detailScheme').textContent = sysRecord.scheme;
        document.getElementById('detailSystemBase').textContent = sysRecord.baseAmount.toLocaleString();
        document.getElementById('detailSystemCompany').textContent = formatMoney(sysRecord.companyFee);
        document.getElementById('detailSystemPersonal').textContent = formatMoney(sysRecord.personalFee);
        document.getElementById('detailStatus').textContent = sysRecord.declareStatus;
        document.getElementById('detailDeclareDate').textContent = sysRecord.declareDate || '-';
    }
    
    // 填充台账记录
    if (ledgerRecord) {
        document.getElementById('detailLedgerBase').textContent = ledgerRecord.baseAmount.toLocaleString();
        document.getElementById('detailLedgerCompany').textContent = formatMoney(ledgerRecord.companyFee);
        document.getElementById('detailLedgerPersonal').textContent = formatMoney(ledgerRecord.personalFee);
    }
    
    // 填充差异分析
    const diffTypeLabels = {
        [DIFF_TYPE.SYSTEM_ONLY]: '系统有记录，台账无记录',
        [DIFF_TYPE.LEDGER_ONLY]: '台账有记录，系统无记录',
        [DIFF_TYPE.AMOUNT_DIFF]: '金额不一致'
    };
    
    let analysisHtml = '';
    if (diff.diffType === DIFF_TYPE.AMOUNT_DIFF) {
        const sysTotal = sysRecord.companyFee + sysRecord.personalFee;
        const ledgerTotal = ledgerRecord.companyFee + ledgerRecord.personalFee;
        const companyDiff = sysRecord.companyFee - ledgerRecord.companyFee;
        const personalDiff = sysRecord.personalFee - ledgerRecord.personalFee;
        
        analysisHtml = `金额差异：<strong id="detailDiffAmount">${formatMoney(Math.abs(diff.diffAmount))}</strong><br>`;
        if (companyDiff !== 0) {
            analysisHtml += `单位缴差额：${formatMoney(Math.abs(companyDiff))}${companyDiff > 0 ? '（系统多）' : '（台账多）'}<br>`;
        }
        if (personalDiff !== 0) {
            analysisHtml += `个人缴差额：${formatMoney(Math.abs(personalDiff))}${personalDiff > 0 ? '（系统多）' : '（台账多）'}`;
        }
    } else {
        analysisHtml = `<strong>${diffTypeLabels[diff.diffType]}</strong>`;
        if (diff.diffType === DIFF_TYPE.SYSTEM_ONLY && sysRecord) {
            analysisHtml += `<br>可能原因：申报失败未通知 / 不该减员被减了 / 漏申报`;
        } else if (diff.diffType === DIFF_TYPE.LEDGER_ONLY && ledgerRecord) {
            analysisHtml += `<br>可能原因：漏采集名单 / 误增员`;
        }
    }
    document.getElementById('detailAnalysis').innerHTML = analysisHtml;
    
    // 显示弹窗
    document.getElementById('detailModal').style.display = 'flex';
}

// 关闭详情弹窗
document.getElementById('detailModalClose').addEventListener('click', () => {
    document.getElementById('detailModal').style.display = 'none';
});

document.getElementById('btnCloseDetail').addEventListener('click', () => {
    document.getElementById('detailModal').style.display = 'none';
});
```

- [ ] **Step 4: 实现导入弹窗的显示/隐藏**

```javascript
// 显示导入弹窗
document.getElementById('btnImportLedger').addEventListener('click', () => {
    document.getElementById('importModal').style.display = 'flex';
});

// 关闭导入弹窗
function closeImportModal() {
    document.getElementById('importModal').style.display = 'none';
    document.getElementById('importPreview').style.display = 'none';
    document.getElementById('importFileInput').value = '';
    document.getElementById('btnConfirmImport').disabled = true;
}

document.getElementById('importModalClose').addEventListener('click', closeImportModal);
document.getElementById('btnCancelImport').addEventListener('click', closeImportModal);
```

- [ ] **Step 5: 实现Toast提示**

```javascript
// Toast提示
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast--${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('toast--show');
    }, 10);
    
    setTimeout(() => {
        toast.classList.remove('toast--show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
```

- [ ] **Step 6: 添加Toast样式**

```css
.toast {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%) translateY(100px);
    padding: 12px 24px;
    border-radius: var(--qy-radius-md);
    font-size: var(--qy-font-size-sm);
    font-weight: 500;
    box-shadow: var(--qy-shadow-lg);
    transition: transform 0.3s ease;
    z-index: 9999;
}

.toast--success {
    background: var(--qy-success-500);
    color: white;
}

.toast--warning {
    background: var(--qy-warning-500);
    color: white;
}

.toast--error {
    background: var(--qy-error-500);
    color: white;
}

.toast--show {
    transform: translateX(-50%) translateY(0);
}
```

- [ ] **Step 7: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): implement export, modal interactions, and toast notifications"
```

---

### Task 9: 添加筛选事件绑定和初始化

**Files:**
- Modify: `prototype/qingyang-reconciliation.html`

- [ ] **Step 1: 添加筛选事件绑定**

```javascript
// 筛选条件变更事件
document.getElementById('filterBillingMonth').addEventListener('change', (e) => {
    currentFilters.billingMonth = e.target.value;
    pagination.page = 1;
    renderAll();
});

document.getElementById('filterRegion').addEventListener('change', (e) => {
    currentFilters.region = e.target.value;
    pagination.page = 1;
    renderAll();
});

document.getElementById('filterSettlement').addEventListener('change', (e) => {
    currentFilters.settlement = e.target.value;
    pagination.page = 1;
    renderAll();
});

document.getElementById('filterInsuranceType').addEventListener('change', (e) => {
    currentFilters.insuranceType = e.target.value;
    pagination.page = 1;
    renderAll();
});

document.getElementById('filterCustomer').addEventListener('input', (e) => {
    currentFilters.customer = e.target.value;
    pagination.page = 1;
    renderAll();
});

// 分页事件
document.getElementById('btnPrevPage').addEventListener('click', () => {
    if (pagination.page > 1) {
        pagination.page--;
        renderCurrentTable();
    }
});

document.getElementById('btnNextPage').addEventListener('click', () => {
    const maxPage = Math.ceil(pagination.total / pagination.pageSize);
    if (pagination.page < maxPage) {
        pagination.page++;
        renderCurrentTable();
    }
});

document.getElementById('inputPageNum').addEventListener('change', (e) => {
    const page = parseInt(e.target.value);
    const maxPage = Math.ceil(pagination.total / pagination.pageSize);
    if (page >= 1 && page <= maxPage) {
        pagination.page = page;
        renderCurrentTable();
    } else {
        e.target.value = pagination.page;
    }
});

document.getElementById('selectPageSize').addEventListener('change', (e) => {
    pagination.pageSize = parseInt(e.target.value);
    pagination.page = 1;
    renderCurrentTable();
});

// 工具栏快捷按钮
document.getElementById('btnViewSystem').addEventListener('click', () => {
    switchTab('system');
});

document.getElementById('btnViewLedger').addEventListener('click', () => {
    switchTab('ledger');
});
```

- [ ] **Step 2: 实现renderAll和分页渲染**

```javascript
// 统一渲染
function renderAll() {
    renderSummaryCards();
    renderCurrentTable();
}

function renderCurrentTable() {
    if (currentTab === 'diff') {
        renderDiffTable();
    } else if (currentTab === 'system') {
        renderSystemTable();
    } else if (currentTab === 'ledger') {
        renderLedgerTable();
    }
}

// 渲染分页器
function renderPagination() {
    const maxPage = Math.max(1, Math.ceil(pagination.total / pagination.pageSize));
    
    document.getElementById('pageTotalCount').textContent = pagination.total;
    document.getElementById('pageTotal').textContent = maxPage;
    document.getElementById('inputPageNum').value = pagination.page;
    
    document.getElementById('btnPrevPage').disabled = pagination.page <= 1;
    document.getElementById('btnNextPage').disabled = pagination.page >= maxPage;
}

// 渲染系统全量表
function renderSystemTable() {
    const tbody = document.getElementById('systemTableBody');
    const records = getFilteredSystemRecords();
    
    const start = (pagination.page - 1) * pagination.pageSize;
    const end = start + pagination.pageSize;
    const pageData = records.slice(start, end);
    
    if (pageData.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" style="text-align: center; padding: 40px; color: var(--qy-text-muted);">
                    暂无系统记录
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = pageData.map(record => `
        <tr>
            <td>${record.name}</td>
            <td>${maskIdCard(record.idCard)}</td>
            <td>${record.customer}</td>
            <td>${record.insuranceType}</td>
            <td class="text-right">${record.baseAmount.toLocaleString()}</td>
            <td class="text-right">${formatMoney(record.companyFee)}</td>
            <td class="text-right">${formatMoney(record.personalFee)}</td>
            <td>${record.declareStatus}</td>
            <td>${record.declareDate || '-'}</td>
        </tr>
    `).join('');
    
    pagination.total = records.length;
    renderPagination();
}

// 渲染台账全量表
function renderLedgerTable() {
    const tbody = document.getElementById('ledgerTableBody');
    
    const start = (pagination.page - 1) * pagination.pageSize;
    const end = start + pagination.pageSize;
    const pageData = LEDGER_RECORDS.slice(start, end);
    
    if (pageData.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" style="text-align: center; padding: 40px; color: var(--qy-text-muted);">
                    暂无台账数据，请先导入Excel
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = pageData.map(record => `
        <tr>
            <td>${record.name}</td>
            <td>${maskIdCard(record.idCard)}</td>
            <td>${record.insuranceType}</td>
            <td class="text-right">${record.baseAmount.toLocaleString()}</td>
            <td class="text-right">${formatMoney(record.companyFee)}</td>
            <td class="text-right">${formatMoney(record.personalFee)}</td>
            <td>${record.billingMonth}</td>
        </tr>
    `).join('');
    
    pagination.total = LEDGER_RECORDS.length;
    renderPagination();
}
```

- [ ] **Step 3: 页面初始化**

```javascript
// 页面初始化
document.addEventListener('DOMContentLoaded', () => {
    // 默认显示当前月份
    const now = new Date();
    const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    currentFilters.billingMonth = currentMonth;
    
    // 设置费用月份下拉选项（最近6个月）
    const monthSelect = document.getElementById('filterBillingMonth');
    monthSelect.innerHTML = '';
    for (let i = 0; i < 6; i++) {
        const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
        const month = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        const option = document.createElement('option');
        option.value = month;
        option.textContent = month;
        if (month === currentMonth) option.selected = true;
        monthSelect.appendChild(option);
    }
    
    // 初始渲染
    renderAll();
});
```

- [ ] **Step 4: 提交**

```bash
git add prototype/qingyang-reconciliation.html
git commit -m "feat(reconciliation): add filter events, initialization, and final integration"
```

---

## 计划自检

### Spec覆盖检查

| 设计文档章节 | 对应任务 |
|------------|---------|
| 2.1 页面入口 | Task 1 (侧边栏导航) |
| 2.2 页面结构 | Task 1 (页面骨架) |
| 2.3 三个视图 | Task 3 (表格) + Task 6 (Tab切换) |
| 3.1 匹配粒度 | Task 6 (calculateDifferences) |
| 3.2 系统记录字段 | Task 6 (SYSTEM_RECORDS) |
| 3.3 台账记录字段 | Task 7 (normalizeRow) |
| 3.4 差异类型 | Task 6 (DIFF_TYPE枚举) |
| 4.1 差异明细表 | Task 3 (表格HTML/CSS) |
| 4.2 差异详情弹窗 | Task 4 (弹窗实现) |
| 4.3 操作按钮 | Task 6, 8 |
| 4.4 筛选条件 | Task 1, 9 |
| 5.1 台账文件格式 | Task 7 (导入逻辑) |
| 5.2 匹配逻辑 | Task 6 (calculateDifferences) |
| 6. 边界情况 | Task 7 (同一记录取金额最大) |

### 类型一致性检查

- `calculateDifferences()` 返回 `DIFFERENCE_RECORDS` 数组，每条包含 `diffType` 字段
- `renderDiffTable()` 使用 `diffType` 渲染差异类型标签
- `showDetail()` 使用 `diff.id` 查询差异记录

### 占位符扫描

无"TBD"、"TODO"、或"类似实现"的占位符。

---

## 执行选择

**Plan complete and saved to `docs/superpowers/plans/2026-04-07-social-insurance-reconciliation-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
