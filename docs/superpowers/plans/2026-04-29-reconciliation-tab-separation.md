# 对账复核 Tab 切换实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `qingyang-reconciliation-unified.html` 中的统一表格（`#unifiedTable`）替换为系统侧/台账侧两个独立 Tab，每个 Tab 有独立的筛选、统计和表格。

**Architecture:** 数据模型（systemRecords、ledgerRecords、matchingResults）不变，仅改造渲染层。新增 `getSystemDisplayRecords()` 和 `getLedgerDisplayRecords()` 分别生成两侧渲染数据，各自维护独立的 filter 状态。

**Tech Stack:** HTML/CSS/JS 单文件原型（`prototype/qingyang-reconciliation-unified.html`）

---

### Task 1: 新增 Tab 相关 CSS 样式

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:342` (在 `</style>` 前插入新 CSS)

- [ ] **Step 1: 添加 Tab 和面板 CSS**

在 `</style>` 前（约第 342 行之前）插入以下 CSS：

```css
/* ===== Bill Tabs ===== */
.bill-tabs { display: flex; gap: 0; border-bottom: 2px solid #E2E8F0; margin-bottom: 16px; }
.bill-tab { padding: 10px 24px; font-size: 14px; font-weight: 500; color: #64748B; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; user-select: none; }
.bill-tab:hover { color: #1E293B; }
.bill-tab.is-active { color: #2563EB; border-bottom-color: #2563EB; }
.bill-tab .tab-count { font-size: 11px; font-weight: 600; margin-left: 6px; padding: 1px 6px; border-radius: 10px; }
.bill-tab--system.is-active .tab-count { background: #DBEAFE; color: #1E40AF; }
.bill-tab--ledger.is-active .tab-count { background: #FEF3C7; color: #854D0E; }
.bill-tab:not(.is-active) .tab-count { background: #F1F5F9; color: #94A3B8; }

.bill-tab-panel { display: none; }
.bill-tab-panel.is-active { display: block; }

/* Summary strip per tab */
.summary-strip { display: flex; gap: 12px; margin-bottom: 16px; }
.summary-chip { padding: 8px 16px; background: #fff; border: 1px solid #E2E8F0; border-radius: 8px; font-size: 12px; }
.summary-chip__label { color: #64748B; }
.summary-chip__value { font-weight: 700; margin-left: 4px; }

/* Cross-reference link */
.cross-ref { display: inline-flex; align-items: center; gap: 3px; padding: 1px 5px; border-radius: 3px; font-size: 10px; background: #F1F5F9; color: #64748B; }
```

- [ ] **Step 2: 验证 CSS 已添加**

打开 `prototype/qingyang-reconciliation-unified.html` 确认 `.bill-tabs`、`.bill-tab`、`.bill-tab-panel`、`.summary-strip`、`.cross-ref` 样式存在于 `<style>` 标签内。

### Task 2: 替换 HTML 结构 — 统一表格 → Tab 面板

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:443-509` (替换整个 filter-bar + unifiedTable 区域)

- [ ] **Step 1: 替换 filter-bar + unifiedTable 为 Tab 结构**

将第 443 行到第 509 行（从 `<!-- Match Status Filter -->` 到 `</div>` 即 `#unifiedTable` 的闭合标签）替换为：

```html
<!-- Bill Tabs -->
<div class="bill-tabs" id="billTabs">
    <div class="bill-tab bill-tab--system is-active" onclick="switchBillTab('system')">
        🖥 系统侧账单 <span class="tab-count" id="systemTabCount">0</span>
    </div>
    <div class="bill-tab bill-tab--ledger" onclick="switchBillTab('ledger')">
        📋 台账侧账单 <span class="tab-count" id="ledgerTabCount">0</span>
    </div>
</div>

<!-- System Tab Panel -->
<div class="bill-tab-panel is-active" id="panel-system">
    <div class="summary-strip" id="systemSummaryStrip">
        <div class="summary-chip"><span class="summary-chip__label">汇总</span><span class="summary-chip__value" id="sysTotalAmount">¥0.00</span></div>
        <div class="summary-chip"><span class="summary-chip__label">已匹配</span><span class="summary-chip__value" id="sysMatched" style="color:#16A34A">0</span></div>
        <div class="summary-chip"><span class="summary-chip__label">待确认</span><span class="summary-chip__value" id="sysPending" style="color:#CA8A04">0</span></div>
        <div class="summary-chip"><span class="summary-chip__label">差异</span><span class="summary-chip__value" id="sysDiff" style="color:#DC2626">0</span></div>
    </div>

    <div class="filter-bar" id="systemFilterBar">
        <span class="filter-bar__label">匹配状态</span>
        <div class="filter-bar__group">
            <div class="filter-bar__item filter-bar__item--match-all is-active" data-match="all" onclick="toggleSystemMatchFilter('all')">
                全部 <span class="filter-bar__count" id="sysMatchCountAll">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--matched" data-match="matched" onclick="toggleSystemMatchFilter('matched')">
                已匹配 <span class="filter-bar__count" id="sysMatchCountMatched">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--pending" data-match="pending" onclick="toggleSystemMatchFilter('pending')">
                待确认 <span class="filter-bar__count" id="sysMatchCountPending">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--diff" data-match="diff" onclick="toggleSystemMatchFilter('diff')">
                差异 <span class="filter-bar__count" id="sysMatchCountDiff">0</span>
            </div>
        </div>
        <div class="filter-bar__divider"></div>
        <span class="filter-bar__label">账单类型</span>
        <div class="filter-bar__group">
            <div class="filter-bar__item filter-bar__item--type-all is-active" data-type="all" onclick="toggleSystemTypeFilter('all')">
                全部
            </div>
            <div class="filter-bar__item filter-bar__item--huijiao" data-type="huijiao" onclick="toggleSystemTypeFilter('huijiao')">
                汇缴
            </div>
            <div class="filter-bar__item filter-bar__item--bujiao" data-type="bujiao" onclick="toggleSystemTypeFilter('bujiao')">
                补缴
            </div>
            <div class="filter-bar__item filter-bar__item--tiaoji" data-type="tiaoji" onclick="toggleSystemTypeFilter('tiaoji')">
                调基补差
            </div>
        </div>
    </div>

    <div class="data-table">
        <table class="qy-table">
            <thead>
                <tr>
                    <th><input type="checkbox" onchange="toggleSystemSelectAll()"></th>
                    <th>匹配状态</th>
                    <th>账单类型</th>
                    <th>姓名</th>
                    <th>身份证号</th>
                    <th>险种</th>
                    <th>应缴月份</th>
                    <th>费款所属期</th>
                    <th>系统金额</th>
                    <th>台账金额</th>
                    <th>差异</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody id="systemTableBody"></tbody>
        </table>
    </div>
    <div class="table-footer">
        <div class="table-footer__left">
            <button class="qy-btn qy-btn--secondary" id="sysSelectAllBtn" onclick="toggleSystemSelectAll()">全选</button>
            <button class="qy-btn qy-btn--primary" disabled id="sysBatchConfirmBtn" onclick="systemBatchConfirm()">确认所选</button>
            <button class="qy-btn qy-btn--secondary" disabled id="sysBatchCancelBtn" onclick="systemBatchCancel()">取消确认</button>
        </div>
        <div class="table-footer__right" id="systemFooterInfo">共 <strong>0</strong> 条 / 1页</div>
    </div>
</div>

<!-- Ledger Tab Panel -->
<div class="bill-tab-panel" id="panel-ledger">
    <div class="summary-strip" id="ledgerSummaryStrip">
        <div class="summary-chip"><span class="summary-chip__label">汇总</span><span class="summary-chip__value" id="ledgerTotalAmount">¥0.00</span></div>
        <div class="summary-chip"><span class="summary-chip__label">已匹配</span><span class="summary-chip__value" id="ledgerMatched" style="color:#16A34A">0</span></div>
        <div class="summary-chip"><span class="summary-chip__label">待确认</span><span class="summary-chip__value" id="ledgerPending" style="color:#CA8A04">0</span></div>
        <div class="summary-chip"><span class="summary-chip__label">差异</span><span class="summary-chip__value" id="ledgerDiff" style="color:#DC2626">0</span></div>
    </div>

    <div class="filter-bar" id="ledgerFilterBar">
        <span class="filter-bar__label">匹配状态</span>
        <div class="filter-bar__group">
            <div class="filter-bar__item filter-bar__item--match-all is-active" data-match="all" onclick="toggleLedgerMatchFilter('all')">
                全部 <span class="filter-bar__count" id="ledgerMatchCountAll">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--matched" data-match="matched" onclick="toggleLedgerMatchFilter('matched')">
                已匹配 <span class="filter-bar__count" id="ledgerMatchCountMatched">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--pending" data-match="pending" onclick="toggleLedgerMatchFilter('pending')">
                待确认 <span class="filter-bar__count" id="ledgerMatchCountPending">0</span>
            </div>
            <div class="filter-bar__item filter-bar__item--diff" data-match="diff" onclick="toggleLedgerMatchFilter('diff')">
                差异 <span class="filter-bar__count" id="ledgerMatchCountDiff">0</span>
            </div>
        </div>
        <div class="filter-bar__divider"></div>
        <span class="filter-bar__label">账单类型</span>
        <div class="filter-bar__group">
            <div class="filter-bar__item filter-bar__item--type-all is-active" data-type="all" onclick="toggleLedgerTypeFilter('all')">
                全部
            </div>
            <div class="filter-bar__item filter-bar__item--huijiao" data-type="huijiao" onclick="toggleLedgerTypeFilter('huijiao')">
                汇缴
            </div>
            <div class="filter-bar__item filter-bar__item--bujiao" data-type="bujiao" onclick="toggleLedgerTypeFilter('bujiao')">
                补缴
            </div>
            <div class="filter-bar__item filter-bar__item--tiaoji" data-type="tiaoji" onclick="toggleLedgerTypeFilter('tiaoji')">
                调基补差
            </div>
        </div>
    </div>

    <div class="data-table">
        <table class="qy-table">
            <thead>
                <tr>
                    <th><input type="checkbox" onchange="toggleLedgerSelectAll()"></th>
                    <th>匹配状态</th>
                    <th>账单类型</th>
                    <th>姓名</th>
                    <th>身份证号</th>
                    <th>险种</th>
                    <th>应缴月份</th>
                    <th>费款所属期</th>
                    <th>台账金额</th>
                    <th>系统金额</th>
                    <th>差异</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody id="ledgerTableBody"></tbody>
        </table>
    </div>
    <div class="table-footer">
        <div class="table-footer__left">
            <button class="qy-btn qy-btn--secondary" id="ledgerSelectAllBtn" onclick="toggleLedgerSelectAll()">全选</button>
            <button class="qy-btn qy-btn--primary" disabled id="ledgerBatchConfirmBtn" onclick="ledgerBatchConfirm()">确认所选</button>
            <button class="qy-btn qy-btn--secondary" disabled id="ledgerBatchCancelBtn" onclick="ledgerBatchCancel()">取消确认</button>
        </div>
        <div class="table-footer__right" id="ledgerFooterInfo">共 <strong>0</strong> 条 / 1页</div>
    </div>
</div>
```

- [ ] **Step 2: 删除旧的 #statsGrid 和 #matchFilterBar**

在上面的替换中，原有的 `#statsGrid`（第 420-441 行）和旧的 `.filter-bar`（第 444-476 行）以及 `#unifiedTable`（第 479-509 行）全部被新结构替代。注意保留 `#statsGrid` 区域用于全局统计（可选保留），但 filter-bar 和 table 必须移除。

**保留 `#statsGrid`** 作为全局统计卡片，它始终可见不受 Tab 切换影响。只替换 filter-bar + table 区域。

### Task 3: 新增 JS 状态变量和 Tab 切换函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:703-707` (在现有 filter state 后新增)

- [ ] **Step 1: 新增 Tab 和独立 filter 状态变量**

在 `let currentTypeFilter = 'all';`（约第 705 行）之后添加：

```javascript
// Tab state
let currentBillTab = 'system';

// System tab filter states
let currentSystemMatchFilter = 'all';
let currentSystemTypeFilter = 'all';

// Ledger tab filter states
let currentLedgerMatchFilter = 'all';
let currentLedgerTypeFilter = 'all';
```

- [ ] **Step 2: 添加 Tab 切换函数**

在新增变量之后添加：

```javascript
function switchBillTab(tab) {
    currentBillTab = tab;
    document.querySelectorAll('.bill-tab').forEach(t => t.classList.remove('is-active'));
    document.querySelectorAll('.bill-tab-panel').forEach(p => p.classList.remove('is-active'));
    if (tab === 'system') {
        document.querySelector('.bill-tab--system').classList.add('is-active');
        document.getElementById('panel-system').classList.add('is-active');
    } else {
        document.querySelector('.bill-tab--ledger').classList.add('is-active');
        document.getElementById('panel-ledger').classList.add('is-active');
    }
    renderAllTables();
}
```

### Task 4: 新增独立 filter 切换函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:946` (在现有 `toggleTypeFilter` 之后)

- [ ] **Step 1: 添加系统侧 filter 切换函数**

在 `toggleTypeFilter` 函数之后添加：

```javascript
// System tab filters
function toggleSystemMatchFilter(filterType) {
    currentSystemMatchFilter = filterType;
    document.querySelectorAll('#systemFilterBar .filter-bar__item[data-match]').forEach(item => {
        item.classList.toggle('is-active', item.dataset.match === filterType);
    });
    renderSystemTable();
}

function toggleSystemTypeFilter(type) {
    currentSystemTypeFilter = type;
    document.querySelectorAll('#systemFilterBar .filter-bar__item[data-type]').forEach(item => {
        item.classList.toggle('is-active', item.dataset.type === type);
    });
    renderSystemTable();
}

// Ledger tab filters
function toggleLedgerMatchFilter(filterType) {
    currentLedgerMatchFilter = filterType;
    document.querySelectorAll('#ledgerFilterBar .filter-bar__item[data-match]').forEach(item => {
        item.classList.toggle('is-active', item.dataset.match === filterType);
    });
    renderLedgerTable();
}

function toggleLedgerTypeFilter(type) {
    currentLedgerTypeFilter = type;
    document.querySelectorAll('#ledgerFilterBar .filter-bar__item[data-type]').forEach(item => {
        item.classList.toggle('is-active', item.dataset.type === type);
    });
    renderLedgerTable();
}
```

### Task 5: 新增 getSystemDisplayRecords 和 getLedgerDisplayRecords

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:946` (在 `getAllDisplayRecords` 之后)

- [ ] **Step 1: 添加 getSystemDisplayRecords**

在 `getAllDisplayRecords()` 函数之后添加：

```javascript
function getSystemDisplayRecords() {
    const records = [];
    for (const sysRec of systemRecords) {
        const ledRec = sysRec.matchedLedgerId
            ? ledgerRecords.find(r => r.id === sysRec.matchedLedgerId)
            : null;

        records.push({
            id: sysRec.id,
            name: sysRec.name,
            idCard: sysRec.idCard,
            insuranceType: sysRec.insuranceType,
            billingMonth: sysRec.billingMonth,
            feeType: sysRec.feeType,
            feePeriod: sysRec.feePeriod || null,
            payableMonth: sysRec.payableMonth,
            sysAmount: sysRec.amount,
            ledgerAmount: ledRec ? ledRec.amount : null,
            matchedLedgerId: ledRec ? ledRec.id : null,
            matchStatus: sysRec.matchStatus,
            diffType: sysRec.diffType,
            diffAmount: sysRec.diffAmount,
            record: sysRec,
            ledgerRecord: ledRec,
        });
    }
    return records;
}
```

- [ ] **Step 2: 添加 getLedgerDisplayRecords**

紧接着添加：

```javascript
function getLedgerDisplayRecords() {
    const records = [];
    for (const ledRec of ledgerRecords) {
        const sysRec = ledRec.matchedSystemId
            ? systemRecords.find(r => r.id === ledRec.matchedSystemId)
            : null;

        records.push({
            id: ledRec.id,
            name: ledRec.name,
            idCard: ledRec.idCard,
            insuranceType: ledRec.insuranceType,
            billingMonth: ledRec.billingMonth,
            feeType: ledRec.feeTypeInferred || null,
            feePeriod: ledRec.feePeriod || null,
            payableMonth: null,
            sysAmount: sysRec ? sysRec.amount : null,
            ledgerAmount: ledRec.amount,
            matchedSystemId: sysRec ? sysRec.id : null,
            matchStatus: ledRec.matchStatus,
            diffType: ledRec.diffType,
            diffAmount: ledRec.diffAmount,
            record: ledRec,
            systemRecord: sysRec,
        });
    }
    return records;
}
```

### Task 6: 新增系统侧表格渲染函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:1028` (在现有 `renderTable` 之前)

- [ ] **Step 1: 添加 getFilteredSystemRecords 辅助函数**

在 `getFilteredRecords()` 之后添加：

```javascript
function getFilteredSystemRecords() {
    let records = getSystemDisplayRecords();

    if (currentSystemMatchFilter !== 'all') {
        if (currentSystemMatchFilter === 'matched') records = records.filter(r => r.matchStatus === MATCH_STATUS.MATCHED);
        else if (currentSystemMatchFilter === 'pending') records = records.filter(r => r.matchStatus === MATCH_STATUS.PENDING);
        else if (currentSystemMatchFilter === 'diff') records = records.filter(r => r.matchStatus === MATCH_STATUS.DIFF);
    }

    if (currentSystemTypeFilter !== 'all') {
        records = records.filter(r => r.feeType === currentSystemTypeFilter);
    }

    const nameVal = document.getElementById('filterName')?.value?.trim();
    if (nameVal) {
        records = records.filter(r => r.name.includes(nameVal) || r.idCard.includes(nameVal));
    }

    return records;
}
```

- [ ] **Step 2: 添加 renderSystemTable 函数**

在 `getFilteredSystemRecords` 之后添加：

```javascript
function renderSystemTable() {
    const tbody = document.getElementById('systemTableBody');
    if (!tbody) return;
    const records = getFilteredSystemRecords();

    tbody.innerHTML = records.map(r => {
        const statusBadge = `<span class="status-badge ${getMatchStatusClass(r.matchStatus)}">${getMatchStatusLabel(r.matchStatus)}</span>`;
        const typeBadge = r.feeType ? `<span class="type-badge type-badge--${r.feeType}">${getBillTypeLabel(r.feeType)}</span>` : '—';

        let diffStr = '—';
        if (r.diffAmount !== null && r.diffAmount !== 0) {
            diffStr = (r.diffAmount > 0 ? '+' : '') + formatMoney(r.diffAmount);
        }

        // 台账金额列：已匹配时显示金额 + 交叉引用
        let ledgerAmountCell = '—';
        if (r.ledgerAmount !== null) {
            ledgerAmountCell = formatMoney(r.ledgerAmount);
            if (r.matchedLedgerId) {
                ledgerAmountCell += ` <span class="cross-ref">↔ ${r.matchedLedgerId}</span>`;
            }
        }

        let actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'system')">详情</button>`;
        if (r.matchStatus === MATCH_STATUS.PENDING) {
            actionBtn = `<button class="btn-action" onclick="openPairingDrawer('${r.id}', 'system')">确认配对</button>`;
        } else if (r.matchStatus === MATCH_STATUS.MATCHED) {
            actionBtn = `<button class="btn-action" onclick="doCancelMatch('${r.id}')">取消</button>`;
        } else if (r.matchStatus === MATCH_STATUS.DIFF) {
            actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'system')">详情</button>`;
        }

        const rowClass = r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
            : r.matchStatus === MATCH_STATUS.PENDING ? 'row-pending'
            : r.matchStatus === MATCH_STATUS.DIFF ? 'row-diff' : '';

        const payableMonthDisplay = r.feeType === 'huijiao' ? (r.payableMonth || '—') : '—';

        return `<tr class="${rowClass}" data-id="${r.id}">
            <td><input type="checkbox" class="system-row-checkbox" data-id="${r.id}" onchange="updateSystemBatchButtons()"></td>
            <td>${statusBadge}</td>
            <td>${typeBadge}</td>
            <td><strong>${r.name}</strong></td>
            <td>${maskIdCard(r.idCard)}</td>
            <td>${r.insuranceType}</td>
            <td>${payableMonthDisplay}</td>
            <td>${r.feePeriod || '—'}</td>
            <td>${formatMoney(r.sysAmount)}</td>
            <td>${ledgerAmountCell}</td>
            <td style="color: ${r.diffAmount && r.diffAmount !== 0 ? '#DC2626' : 'inherit'}; font-weight: ${r.diffAmount && r.diffAmount !== 0 ? '600' : '400'}">${diffStr}</td>
            <td>${actionBtn}</td>
        </tr>`;
    }).join('');

    document.getElementById('systemFooterInfo').innerHTML = `共 <strong>${records.length}</strong> 条 / 1页`;
    updateSystemBatchButtons();
    updateSystemSummary(records);
    updateSystemMatchCounts(records);
}
```

- [ ] **Step 3: 添加 updateSystemSummary 函数**

在 `renderSystemTable` 之后添加：

```javascript
function updateSystemSummary(records) {
    const all = getSystemDisplayRecords();
    const totalAmt = all.reduce((s, r) => s + r.sysAmount, 0);
    const matchedCount = all.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
    const pendingCount = all.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
    const diffCount = all.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;

    document.getElementById('sysTotalAmount').textContent = formatMoney(totalAmt);
    document.getElementById('sysMatched').textContent = matchedCount;
    document.getElementById('sysPending').textContent = pendingCount;
    document.getElementById('sysDiff').textContent = diffCount;
}
```

- [ ] **Step 4: 添加 updateSystemMatchCounts 函数**

在 `updateSystemSummary` 之后添加：

```javascript
function updateSystemMatchCounts(records) {
    const all = records || getSystemDisplayRecords();
    const matchedCount = all.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
    const pendingCount = all.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
    const diffCount = all.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;
    const totalCount = all.length;

    document.getElementById('sysMatchCountAll').textContent = totalCount;
    document.getElementById('sysMatchCountMatched').textContent = matchedCount;
    document.getElementById('sysMatchCountPending').textContent = pendingCount;
    document.getElementById('sysMatchCountDiff').textContent = diffCount;
    document.getElementById('systemTabCount').textContent = totalCount;
}
```

### Task 7: 新增台账侧表格渲染函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (在 `renderSystemTable` 相关函数之后)

- [ ] **Step 1: 添加 getFilteredLedgerRecords 辅助函数**

```javascript
function getFilteredLedgerRecords() {
    let records = getLedgerDisplayRecords();

    if (currentLedgerMatchFilter !== 'all') {
        if (currentLedgerMatchFilter === 'matched') records = records.filter(r => r.matchStatus === MATCH_STATUS.MATCHED);
        else if (currentLedgerMatchFilter === 'pending') records = records.filter(r => r.matchStatus === MATCH_STATUS.PENDING);
        else if (currentLedgerMatchFilter === 'diff') records = records.filter(r => r.matchStatus === MATCH_STATUS.DIFF);
    }

    if (currentLedgerTypeFilter !== 'all') {
        records = records.filter(r => r.feeType === currentLedgerTypeFilter);
    }

    const nameVal = document.getElementById('filterName')?.value?.trim();
    if (nameVal) {
        records = records.filter(r => r.name.includes(nameVal) || r.idCard.includes(nameVal));
    }

    return records;
}
```

- [ ] **Step 2: 添加 renderLedgerTable 函数**

```javascript
function renderLedgerTable() {
    const tbody = document.getElementById('ledgerTableBody');
    if (!tbody) return;
    const records = getFilteredLedgerRecords();

    tbody.innerHTML = records.map(r => {
        const statusBadge = `<span class="status-badge ${getMatchStatusClass(r.matchStatus)}">${getMatchStatusLabel(r.matchStatus)}</span>`;
        const typeBadge = r.feeType ? `<span class="type-badge type-badge--${r.feeType}">${getBillTypeLabel(r.feeType)}</span>` : '—';

        let diffStr = '—';
        if (r.diffAmount !== null && r.diffAmount !== 0) {
            diffStr = (r.diffAmount > 0 ? '+' : '') + formatMoney(r.diffAmount);
        }

        // 系统金额列：已匹配时显示金额 + 交叉引用
        let sysAmountCell = '—';
        if (r.sysAmount !== null) {
            sysAmountCell = formatMoney(r.sysAmount);
            if (r.matchedSystemId) {
                sysAmountCell += ` <span class="cross-ref">↔ ${r.matchedSystemId}</span>`;
            }
        }

        let actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'ledger')">详情</button>`;
        if (r.matchStatus === MATCH_STATUS.PENDING) {
            actionBtn = `<button class="btn-action" onclick="openPairingDrawer('${r.id}', 'ledger')">确认配对</button>`;
        } else if (r.matchStatus === MATCH_STATUS.MATCHED) {
            actionBtn = `<button class="btn-action" onclick="doCancelMatch('${r.id}')">取消</button>`;
        } else if (r.matchStatus === MATCH_STATUS.DIFF) {
            actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'ledger')">详情</button>`;
        }

        const rowClass = r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
            : r.matchStatus === MATCH_STATUS.PENDING ? 'row-pending'
            : r.matchStatus === MATCH_STATUS.DIFF ? 'row-diff' : '';

        return `<tr class="${rowClass}" data-id="${r.id}">
            <td><input type="checkbox" class="ledger-row-checkbox" data-id="${r.id}" onchange="updateLedgerBatchButtons()"></td>
            <td>${statusBadge}</td>
            <td>${typeBadge}</td>
            <td><strong>${r.name}</strong></td>
            <td>${maskIdCard(r.idCard)}</td>
            <td>${r.insuranceType}</td>
            <td>${r.billingMonth || '—'}</td>
            <td>${r.feePeriod || '—'}</td>
            <td>${formatMoney(r.ledgerAmount)}</td>
            <td>${sysAmountCell}</td>
            <td style="color: ${r.diffAmount && r.diffAmount !== 0 ? '#DC2626' : 'inherit'}; font-weight: ${r.diffAmount && r.diffAmount !== 0 ? '600' : '400'}">${diffStr}</td>
            <td>${actionBtn}</td>
        </tr>`;
    }).join('');

    document.getElementById('ledgerFooterInfo').innerHTML = `共 <strong>${records.length}</strong> 条 / 1页`;
    updateLedgerBatchButtons();
    updateLedgerSummary(records);
    updateLedgerMatchCounts(records);
}
```

- [ ] **Step 3: 添加 updateLedgerSummary 函数**

```javascript
function updateLedgerSummary(records) {
    const all = getLedgerDisplayRecords();
    const totalAmt = all.reduce((s, r) => s + r.ledgerAmount, 0);
    const matchedCount = all.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
    const pendingCount = all.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
    const diffCount = all.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;

    document.getElementById('ledgerTotalAmount').textContent = formatMoney(totalAmt);
    document.getElementById('ledgerMatched').textContent = matchedCount;
    document.getElementById('ledgerPending').textContent = pendingCount;
    document.getElementById('ledgerDiff').textContent = diffCount;
}
```

- [ ] **Step 4: 添加 updateLedgerMatchCounts 函数**

```javascript
function updateLedgerMatchCounts(records) {
    const all = records || getLedgerDisplayRecords();
    const matchedCount = all.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
    const pendingCount = all.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
    const diffCount = all.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;
    const totalCount = all.length;

    document.getElementById('ledgerMatchCountAll').textContent = totalCount;
    document.getElementById('ledgerMatchCountMatched').textContent = matchedCount;
    document.getElementById('ledgerMatchCountPending').textContent = pendingCount;
    document.getElementById('ledgerMatchCountDiff').textContent = diffCount;
    document.getElementById('ledgerTabCount').textContent = totalCount;
}
```

### Task 8: 添加 renderAllTables 和批量操作函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (在 `renderLedgerTable` 相关函数之后)

- [ ] **Step 1: 添加 renderAllTables 函数**

```javascript
function renderAllTables() {
    renderSystemTable();
    renderLedgerTable();
    updateStats();
}
```

- [ ] **Step 2: 添加系统侧批量操作函数**

```javascript
function getSelectedSystemIds() {
    return Array.from(document.querySelectorAll('#systemTableBody .system-row-checkbox:checked')).map(cb => cb.dataset.id);
}

function toggleSystemSelectAll() {
    const checkboxes = document.querySelectorAll('#systemTableBody .system-row-checkbox');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    const newChecked = !allChecked;
    checkboxes.forEach(cb => cb.checked = newChecked);
    updateSystemBatchButtons();
}

function updateSystemBatchButtons() {
    const selectedIds = getSelectedSystemIds();
    const hasSelection = selectedIds.length > 0;
    const batchConfirmBtn = document.getElementById('sysBatchConfirmBtn');
    const batchCancelBtn = document.getElementById('sysBatchCancelBtn');
    if (batchConfirmBtn) batchConfirmBtn.disabled = !hasSelection;
    if (batchCancelBtn) batchCancelBtn.disabled = !hasSelection;
    const selectAllBtn = document.getElementById('sysSelectAllBtn');
    if (selectAllBtn) {
        const totalCount = document.querySelectorAll('#systemTableBody .system-row-checkbox').length;
        selectAllBtn.textContent = selectedIds.length === totalCount ? '取消全选' : '全选';
    }
}

function systemBatchConfirm() {
    const selectedIds = getSelectedSystemIds();
    if (selectedIds.length === 0) {
        showToast('请先选择记录', 'warning');
        return;
    }

    let confirmed = 0;
    for (const id of selectedIds) {
        const sysRec = systemRecords.find(r => r.id === id);
        if (sysRec && sysRec.matchStatus === MATCH_STATUS.PENDING) {
            const group = matchingResults.pending.find(g =>
                g.systemRecords.some(r => r.id === id)
            );
            if (group && group.ledgerRecords.length > 0) {
                const idx = group.systemRecords.findIndex(r => r.id === id);
                const ledRec = group.ledgerRecords[idx] || group.ledgerRecords[0];
                if (confirmPendingPairing(id, ledRec.id)) {
                    confirmed++;
                }
            }
        }
    }

    renderAllTables();
    if (confirmed > 0) {
        showToast(`批量确认 ${confirmed} 条`, 'success');
    } else {
        showToast('所选记录中无可确认配对', 'warning');
    }
}

function systemBatchCancel() {
    const selectedIds = getSelectedSystemIds();
    if (selectedIds.length === 0) {
        showToast('请先选择记录', 'warning');
        return;
    }

    let cancelled = 0;
    for (const id of selectedIds) {
        const sysRec = systemRecords.find(r => r.id === id);
        if (sysRec && sysRec.matchStatus === MATCH_STATUS.MATCHED) {
            cancelMatch(id);
            cancelled++;
        }
    }

    renderAllTables();
    if (cancelled > 0) {
        showToast(`批量取消 ${cancelled} 条`, 'success');
    } else {
        showToast('所选记录中无可取消匹配', 'warning');
    }
}
```

- [ ] **Step 3: 添加台账侧批量操作函数**

```javascript
function getSelectedLedgerIds() {
    return Array.from(document.querySelectorAll('#ledgerTableBody .ledger-row-checkbox:checked')).map(cb => cb.dataset.id);
}

function toggleLedgerSelectAll() {
    const checkboxes = document.querySelectorAll('#ledgerTableBody .ledger-row-checkbox');
    const allChecked = Array.from(checkboxes).every(cb => cb.checked);
    const newChecked = !allChecked;
    checkboxes.forEach(cb => cb.checked = newChecked);
    updateLedgerBatchButtons();
}

function updateLedgerBatchButtons() {
    const selectedIds = getSelectedLedgerIds();
    const hasSelection = selectedIds.length > 0;
    const batchConfirmBtn = document.getElementById('ledgerBatchConfirmBtn');
    const batchCancelBtn = document.getElementById('ledgerBatchCancelBtn');
    if (batchConfirmBtn) batchConfirmBtn.disabled = !hasSelection;
    if (batchCancelBtn) batchCancelBtn.disabled = !hasSelection;
    const selectAllBtn = document.getElementById('ledgerSelectAllBtn');
    if (selectAllBtn) {
        const totalCount = document.querySelectorAll('#ledgerTableBody .ledger-row-checkbox').length;
        selectAllBtn.textContent = selectedIds.length === totalCount ? '取消全选' : '全选';
    }
}

function ledgerBatchConfirm() {
    const selectedIds = getSelectedLedgerIds();
    if (selectedIds.length === 0) {
        showToast('请先选择记录', 'warning');
        return;
    }

    let confirmed = 0;
    for (const id of selectedIds) {
        const ledRec = ledgerRecords.find(r => r.id === id);
        if (ledRec && ledRec.matchStatus === MATCH_STATUS.PENDING) {
            const group = matchingResults.pending.find(g =>
                g.ledgerRecords.some(r => r.id === id)
            );
            if (group && group.systemRecords.length > 0) {
                const idx = group.ledgerRecords.findIndex(r => r.id === id);
                const sysRec = group.systemRecords[idx] || group.systemRecords[0];
                if (confirmPendingPairing(sysRec.id, id)) {
                    confirmed++;
                }
            }
        }
    }

    renderAllTables();
    if (confirmed > 0) {
        showToast(`批量确认 ${confirmed} 条`, 'success');
    } else {
        showToast('所选记录中无可确认配对', 'warning');
    }
}

function ledgerBatchCancel() {
    const selectedIds = getSelectedLedgerIds();
    if (selectedIds.length === 0) {
        showToast('请先选择记录', 'warning');
        return;
    }

    let cancelled = 0;
    for (const id of selectedIds) {
        const ledRec = ledgerRecords.find(r => r.id === id);
        if (ledRec && ledRec.matchStatus === MATCH_STATUS.MATCHED) {
            cancelMatch(id);
            cancelled++;
        }
    }

    renderAllTables();
    if (cancelled > 0) {
        showToast(`批量取消 ${cancelled} 条`, 'success');
    } else {
        showToast('所选记录中无可取消匹配', 'warning');
    }
}
```

### Task 9: 修改现有函数调用 renderAllTables 替代 renderTable

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` 中以下函数

- [ ] **Step 1: 修改 toggleMatchFilter 和 toggleTypeFilter（保留旧函数兼容全局搜索）**

旧的全局 filter 函数（`toggleMatchFilter` 和 `toggleTypeFilter`）仍然保留用于全局搜索框联动，但 `renderTable()` 调用替换为 `renderAllTables()`：

在 `toggleMatchFilter`（约第 932 行）中将 `renderTable()` 改为 `renderAllTables()`：
```javascript
function toggleMatchFilter(filterType) {
    currentMatchFilter = filterType;
    document.querySelectorAll('#matchFilterBar .filter-bar__item[data-match]').forEach(item => {
        item.classList.toggle('is-active', item.dataset.match === filterType);
    });
    renderAllTables();
}
```

注意：由于 HTML 中移除了 `#matchFilterBar`，这些旧函数将不再被调用。可以保留或删除。为保持清洁，删除旧的 `toggleMatchFilter`、`toggleTypeFilter`、`getAllDisplayRecords`、`getFilteredRecords`、`renderTable` 函数（第 932-1073 行）。

- [ ] **Step 2: 修改 doCancelMatch（约第 1075 行）**

将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function doCancelMatch(id) {
    cancelMatch(id);
    renderAllTables();
    updateMatchCounts();
    showToast('已取消匹配', 'success');
}
```

- [ ] **Step 3: 修改 confirmPairing（约第 1440 行）**

将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function confirmPairing() {
    // ... existing code ...
    closePairingDrawer();
    renderAllTables();
    updateStats();
    updateMatchCounts();
    // ... existing code ...
}
```

- [ ] **Step 4: 修改 showNewDetail 中的 closeDetailDrawer 回调（约第 1616 行）**

在 `handleDiffRemark`（约第 1616 行）中将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function handleDiffRemark() {
    const remark = document.getElementById('diffRemark')?.value || '';
    if (currentDetailRecord) {
        currentDetailRecord.remark = remark || '已处理';
        markDiffHandled(currentDetailRecord.id);
    }
    closeDetailDrawer();
    renderAllTables();
    updateStats();
    updateMatchCounts();
    showToast('已标记为已处理', 'success');
}
```

- [ ] **Step 5: 修改 doArchive（约第 1649 行）**

将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function doArchive() {
    // ... existing code ...
    renderAllTables();
    updateStats();
    updateMatchCounts();
    // ... existing code ...
}
```

- [ ] **Step 6: 修改 old batchConfirm 和 batchCancel（约第 1745-1804 行）**

将 `renderTable()` 改为 `renderAllTables()` 或直接删除（因为已有新的 `systemBatchConfirm`、`ledgerBatchConfirm` 等）。

为保持清洁，删除旧的 `getSelectedIds`、`toggleSelectAll`、`updateBatchButtons`、`batchConfirm`、`batchCancel` 函数（第 1686-1804 行区域）。

### Task 10: 修改 importNextStep 和 startReconciliation 调用

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [ ] **Step 1: 修改 importNextStep（约第 1184 行）**

将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function importNextStep() {
    // ... existing code ...
    closeImportDialog();
    updateStats();
    updateMatchCounts();
    renderAllTables();
    showToast(`导入成功：${successRows.length} 条记录`, 'success');
}
```

- [ ] **Step 2: 修改 startReconciliation（约第 1245 行）**

将 `renderTable()` 改为 `renderAllTables()`：

```javascript
function startReconciliation() {
    // ... existing code ...
    setTimeout(() => {
        executeMatching();
        document.getElementById('loadingOverlay').classList.remove('is-visible');
        renderAllTables();
        updateStats();
        updateMatchCounts();
        // ... existing code ...
    }, 800);
}
```

### Task 11: 修改 DOMContentLoaded 初始化

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:1806-1812`

- [ ] **Step 1: 修改初始化逻辑**

将原来的：
```javascript
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    updateMatchCounts();
    renderTable();
});
```

改为：
```javascript
document.addEventListener('DOMContentLoaded', () => {
    updateStats();
    updateMatchCounts();
    renderAllTables();
});
```

### Task 12: 更新 updateMatchCounts 兼容新结构

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:1108-1118`

- [ ] **Step 1: 修改 updateMatchCounts 移除对旧 DOM 的依赖**

旧的 `updateMatchCounts` 引用了 `#matchCountAll` 等已不存在的元素。需要更新为不再更新旧 DOM 元素（因为各 Tab 有自己的 `updateSystemMatchCounts` 和 `updateLedgerMatchCounts`）：

```javascript
function updateMatchCounts() {
    // Tab panels have their own count updates via updateSystemMatchCounts / updateLedgerMatchCounts
    // This function is kept for compatibility with non-tab callers
}
```

### Task 13: 打开页面验证 Tab 切换功能

**Files:**
- None (browser verification)

- [ ] **Step 1: 在浏览器中打开原型页面**

```bash
open prototype/qingyang-reconciliation-unified.html
```

- [ ] **Step 2: 验证以下场景**

1. 页面加载时默认显示"系统侧账单"Tab，台账侧 Tab 隐藏
2. 点击"台账侧账单"Tab 切换到台账侧面板，系统侧隐藏
3. 导入台账 → 系统侧 Tab 显示 6 条，台账侧 Tab 显示 7 条，Tab 角标数字正确
4. 开始对账 → 两侧统计卡片更新，行颜色正确
5. 张三汇缴已匹配 → 两侧均显示，系统侧显示 `↔ T001`，台账侧显示类型「汇缴」+ `↔ S001`
6. 李四补缴差异 → 两侧均显示为差异行
7. 系统侧筛选"已匹配"→ 只显示已匹配记录，切换到台账侧后筛选状态独立保留
8. 系统侧筛选"汇缴"→ 只显示汇缴记录
9. 台账侧「确认配对」→ 打开抽屉选择系统记录，确认后两侧同步更新
10. 系统侧批量操作只对系统侧记录生效
11. 取消匹配后两侧同步更新

- [ ] **Step 3: 发现问题则修复**

常见问题检查：
- Tab 切换时 CSS `.is-active` 类是否正确切换
- 筛选器点击是否只影响当前 Tab 的 `is-active` 状态
- 表格行的 checkbox class 是否正确（`system-row-checkbox` / `ledger-row-checkbox`）
- 批量操作按钮 ID 是否与 HTML 中一致
- `formatMoney` 在 `null` 时是否正确显示 `—`
