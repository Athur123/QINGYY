# 对账复核归档批次 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 引入归档批次机制支持同一账单月份多次归档，每次归档自动将已核对且未归档记录打包为新批次

**Architecture:** 新增 `archiveBatches` 数组存储批次元数据；记录新增 `archiveBatchId` 字段关联批次；改写 `doArchive()` 创建批次+标记记录；新增批次历史可折叠区域和批次详情抽屉

**Tech Stack:** Vanilla JS, HTML, CSS — single-file prototype

---

## File to modify

- `prototype/qingyang-reconciliation-unified.html` — 所有变更集中在该文件

---

### Task 1: 数据模型 — 新增 archiveBatches 数组和记录字段

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — matchingResults 声明后（line ~820），所有 systemRecords 和 ledgerRecords 记录

- [ ] **Step 1: 在 matchingResults 后新增 archiveBatches 声明**

在 `let matchingResults = { matched: [], pending: [], diffs: [], executed: false };` 之后插入：

```javascript
let archiveBatches = [];
```

- [ ] **Step 2: 为所有 systemRecords 新增 archiveBatchId 字段**

在每条系统侧记录的 `remark: null` 之后增加 `archiveBatchId: null`。例如第一条 S001：

修改前：
```javascript
{ id: 'S001', name: '陶欢欢', idCard: '500382**********08', insuranceType: '养老', billingMonth: '2026-04', feeType: 'huijiao', feePeriod: '2026-04', payableMonth: '2026-04', amountCompany: 986.50, amountPersonal: 246.62, amount: 1233.12, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
```

修改后（在 `remark: null` 后插入 `archiveBatchId: null,`）：
```javascript
{ id: 'S001', name: '陶欢欢', idCard: '500382**********08', insuranceType: '养老', billingMonth: '2026-04', feeType: 'huijiao', feePeriod: '2026-04', payableMonth: '2026-04', amountCompany: 986.50, amountPersonal: 246.62, amount: 1233.12, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null, archiveBatchId: null },
```

对所有 23 条 S001-S023 做同样修改。

- [ ] **Step 3: 确认初始化表头无变更**

当前表头不变，无需新增列。

- [ ] **Step 4: 浏览器验证数据初始化不报错**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/prototype/qingyang-reconciliation-unified.html
# Verify: console no errors, table renders as before
```

---

### Task 2: CSS — 新增归档行样式和批次相关样式

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — `<style>` 块

- [ ] **Step 1: 新增 row-archived 行样式**

在 `.row-diff:hover td`（line ~290）之后新增：

```css
.row-archived td { background: #F1F5F9; opacity: 0.7; }
```

- [ ] **Step 2: 新增 archive-badge 标签样式**

在 `.force-match-dialog__footer` 样式块之后新增：

```css
/* Archive Batch */
.archive-badge { display: inline-block; padding: 1px 6px; font-size: 11px; font-weight: 500; border-radius: var(--qy-radius-sm); background: #E2E8F0; color: #64748B; margin-left: 4px; }

/* Batch History Section */
.archive-batch-section { background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light); border-radius: var(--qy-radius-md); margin-bottom: 16px; overflow: hidden; }
.archive-batch-section__header { display: flex; align-items: center; justify-content: space-between; padding: 10px 16px; cursor: pointer; user-select: none; font-size: 13px; font-weight: 600; color: var(--qy-text-primary); }
.archive-batch-section__header:hover { background: var(--qy-bg-secondary); }
.archive-batch-section__header .collapse-icon { font-size: 11px; color: var(--qy-text-muted); transition: transform 0.2s; }
.archive-batch-section__header .collapse-icon.collapsed { transform: rotate(-90deg); }
.archive-batch-section__body { padding: 0 16px 12px; }
.archive-batch-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.archive-batch-table th { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--qy-border-light); color: var(--qy-text-secondary); font-weight: 500; font-size: 11px; }
.archive-batch-table td { padding: 8px 10px; border-bottom: 1px solid var(--qy-border-light); color: var(--qy-text-primary); }
.archive-batch-table tr:last-child td { border-bottom: none; }
.archive-batch-table .btn-action { font-size: 12px; }

/* Batch Detail Drawer */
.batch-detail-drawer { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 1000; align-items: center; justify-content: center; }
.batch-detail-drawer.is-visible { display: flex; }
.batch-detail-drawer__box { background: var(--qy-bg-primary); border-radius: var(--qy-radius-lg); width: 600px; max-height: 80vh; overflow-y: auto; box-shadow: 0 20px 60px rgba(0,0,0,0.2); }
.batch-detail-drawer__header { display: flex; align-items: center; justify-content: space-between; padding: 16px 20px; border-bottom: 1px solid var(--qy-border-light); }
.batch-detail-drawer__title { font-size: 16px; font-weight: 600; }
.batch-detail-drawer__body { padding: 20px; }
.batch-detail-drawer__body .qy-table { width: 100%; }
.batch-detail-drawer__footer { display: flex; justify-content: flex-end; padding: 12px 20px; border-top: 1px solid var(--qy-border-light); }
```

- [ ] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "style: 新增归档行样式、批次历史区域和批次详情抽屉 CSS

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 3: 重写归档逻辑 — doArchive() 和 archiveResults()

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — `archiveResults()` (line ~2414) 和 `doArchive()` (line ~2434)

- [ ] **Step 1: 替换 archiveResults() 和 doArchive()**

删除现有两个函数（line ~2414-2451），替换为：

```javascript
function archiveResults() {
    if (!matchingResults.executed) {
        showToast('请先执行对账', 'warning');
        return;
    }

    // 筛选待归档：MATCHED 且未归档
    const toArchive = systemRecords.filter(r => r.matchStatus === MATCH_STATUS.MATCHED && !r.archived);
    if (toArchive.length === 0) {
        showToast('无待归档记录', 'warning');
        return;
    }

    // DIFF/PENDING 检查（仅未归档的）
    const pendingCount = systemRecords.filter(r => r.matchStatus === MATCH_STATUS.PENDING && !r.archived).length;
    const diffCount = systemRecords.filter(r => r.matchStatus === MATCH_STATUS.DIFF && !r.remark && !r.archived).length;

    if (pendingCount > 0 || diffCount > 0) {
        showConfirmDialog(
            '归档确认',
            '还有 ' + pendingCount + ' 条待确认和 ' + diffCount + ' 条差异未处理，是否继续归档（仅归档已核对记录）？',
            function(confirmed) { if (confirmed) doArchive(toArchive); }
        );
    } else {
        doArchive(toArchive);
    }
}

function doArchive(toArchive) {
    var batchNum = archiveBatches.length + 1;
    var batchId = 'B' + String(batchNum).padStart(3, '0');
    var totalAmount = toArchive.reduce(function(sum, r) { return sum + r.amount; }, 0);
    var now = new Date().toLocaleString('zh-CN');

    // 创建批次
    archiveBatches.unshift({
        id: batchId,
        label: '第' + batchNum + '批',
        billingMonth: getCurrentBillingMonth(),
        createdAt: now,
        recordCount: toArchive.length,
        totalAmount: totalAmount,
    });

    // 标记系统侧记录
    toArchive.forEach(function(r) {
        r.archived = true;
        r.archivedAt = now;
        r.archiveBatchId = batchId;
    });

    // 标记关联的台账侧记录
    toArchive.forEach(function(sysRec) {
        if (sysRec.matchedLedgerId) {
            var ledRec = ledgerRecords.find(function(r) { return r.id === sysRec.matchedLedgerId; });
            if (ledRec && !ledRec.archived) {
                ledRec.archived = true;
                ledRec.archivedAt = now;
                ledRec.archiveBatchId = batchId;
            }
        }
    });

    renderAllTables();
    renderArchiveBatchHistory();
    updateMatchCounts();
    showToast('归档完成：第' + batchNum + '批，共' + toArchive.length + '条，' + formatMoney(totalAmount), 'success');
}

function getCurrentBillingMonth() {
    var urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('month') || systemRecords[0]?.billingMonth || '';
}
```

- [ ] **Step 2: 浏览器验证**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/prototype/qingyang-reconciliation-unified.html?ruleName=社保规则A&month=2026-04
```

操作流程：
1. 导入台账 → 开始对账 → 全部确认核对（处理 PENDING）
2. 点击「归档结果」→ 应创建第1批，toast 显示归档记录数和金额
3. 再次点击「归档结果」→ 提示"无待归档记录"

- [ ] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 重写归档逻辑支持批次 — 每次归档创建新批次并标记记录

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 4: 批次历史区域 — HTML + 渲染/折叠函数

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — 在系统侧 Tab Panel 的 filter-bar 与 data-table 之间插入 HTML，新增 JS 函数

- [ ] **Step 1: 在系统侧 Tab 的 filter-bar 之后插入批次历史 HTML**

在系统侧 Tab Panel 的 `</div>`（筛选栏结束标签，line ~502）之后、`<div class="data-table">` 之前插入：

```html
<!-- Archive Batch History -->
<div class="archive-batch-section" id="archiveBatchSection" style="display:none;">
    <div class="archive-batch-section__header" onclick="toggleBatchHistory()">
        <span>📦 归档批次</span>
        <span class="collapse-icon" id="batchCollapseIcon">▼</span>
    </div>
    <div class="archive-batch-section__body" id="archiveBatchBody"></div>
</div>
```

- [ ] **Step 2: 新增 renderArchiveBatchHistory() 和 toggleBatchHistory()**

在 `doArchive()` 函数之后新增：

```javascript
function renderArchiveBatchHistory() {
    var section = document.getElementById('archiveBatchSection');
    var body = document.getElementById('archiveBatchBody');
    if (!section || !body) return;

    if (archiveBatches.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    body.innerHTML = '<table class="archive-batch-table"><thead><tr><th>批次</th><th>账单月份</th><th>记录数</th><th>金额</th><th>归档时间</th><th>操作</th></tr></thead><tbody>' +
        archiveBatches.map(function(b) {
            return '<tr><td><strong>' + b.label + '</strong></td><td>' + b.billingMonth + '</td><td>' + b.recordCount + '条</td><td>' + formatMoney(b.totalAmount) + '</td><td>' + b.createdAt + '</td><td><button class="btn-action" onclick="showBatchDetail(\'' + b.id + '\')">详情</button></td></tr>';
        }).join('') +
        '</tbody></table>';
}

function toggleBatchHistory() {
    var body = document.getElementById('archiveBatchBody');
    var icon = document.getElementById('batchCollapseIcon');
    if (!body || !icon) return;
    if (body.style.display === 'none') {
        body.style.display = 'block';
        icon.classList.remove('collapsed');
    } else {
        body.style.display = 'none';
        icon.classList.add('collapsed');
    }
}
```

- [ ] **Step 3: 在渲染流程中调用 renderArchiveBatchHistory()**

在 `renderAllTables()` 函数末尾新增调用：

修改 `renderAllTables()`：
```javascript
function renderAllTables() {
    renderSystemTable();
    renderLedgerTable();
    renderArchiveBatchHistory();  // 新增
}
```

- [ ] **Step 4: 浏览器验证**

1. 完成对账+归档后 → 批次历史区域显示在表格上方
2. 点击标题行 → 展开/收起批次列表
3. 新批次在列表顶部

- [ ] **Step 5: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 新增批次历史区域 — 可折叠展示所有归档批次

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 5: 批次详情抽屉 — HTML + JS

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — 在 forceMatchDialog 之后插入 HTML，新增 JS 函数

- [ ] **Step 1: 在 forceMatchDialog HTML 之后插入批次详情抽屉 HTML**

在 forceMatchDialog 的 `</div>` 之后（最后一个 dialog 之后）插入：

```html
<!-- Batch Detail Drawer -->
<div class="batch-detail-drawer" id="batchDetailDrawer" onclick="closeBatchDetailDrawer(event)">
    <div class="batch-detail-drawer__box" onclick="event.stopPropagation()">
        <div class="batch-detail-drawer__header">
            <h3 class="batch-detail-drawer__title" id="batchDetailTitle">批次详情</h3>
            <button class="drawer__close" onclick="closeBatchDetailDrawer()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </div>
        <div class="batch-detail-drawer__body" id="batchDetailBody"></div>
        <div class="batch-detail-drawer__footer">
            <button class="qy-btn qy-btn--secondary" onclick="closeBatchDetailDrawer()">关闭</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 新增 showBatchDetail() 和 closeBatchDetailDrawer()**

在 `toggleBatchHistory()` 之后新增：

```javascript
function showBatchDetail(batchId) {
    var batch = archiveBatches.find(function(b) { return b.id === batchId; });
    if (!batch) return;

    // 从系统侧查找该批次的记录
    var sysRecs = systemRecords.filter(function(r) { return r.archiveBatchId === batchId; });

    document.getElementById('batchDetailTitle').textContent = batch.label + ' — ' + batch.billingMonth;
    var body = document.getElementById('batchDetailBody');

    var rowsHtml = sysRecs.map(function(r) {
        var ledgerInfo = '—';
        if (r.matchedLedgerId) {
            var ledRec = ledgerRecords.find(function(lr) { return lr.id === r.matchedLedgerId; });
            ledgerInfo = ledRec ? formatMoney(ledRec.amount) + ' <span class="cross-ref">↔ ' + ledRec.id + '</span>' : '—';
        }
        return '<tr><td><strong>' + r.name + '</strong></td>' +
            '<td>' + maskIdCard(r.idCard) + '</td>' +
            '<td>' + r.insuranceType + '</td>' +
            '<td><span class="type-badge type-badge--' + r.feeType + '">' + getBillTypeLabel(r.feeType) + '</span></td>' +
            '<td>' + formatMoney(r.amount) + '</td>' +
            '<td style="font-size:11px;color:var(--qy-text-secondary)">' + ledgerInfo + '</td></tr>';
    }).join('');

    body.innerHTML = '<table class="qy-table"><thead><tr><th>姓名</th><th>身份证</th><th>险种</th><th>类型</th><th>金额</th><th>台账</th></tr></thead><tbody>' + rowsHtml + '</tbody></table>' +
        '<p style="margin-top:12px;font-size:12px;color:var(--qy-text-secondary)">共 <strong>' + sysRecs.length + '</strong> 条，金额合计 <strong>' + formatMoney(batch.totalAmount) + '</strong> · 归档时间 ' + batch.createdAt + '</p>';

    document.getElementById('batchDetailDrawer').classList.add('is-visible');
}

function closeBatchDetailDrawer(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('batchDetailDrawer').classList.remove('is-visible');
}
```

- [ ] **Step 3: 在 Escape 键处理中新增关闭批次详情抽屉**

在全局 keydown 监听器的 forceMatchDialog 处理之后新增：

找到 Escape 键处理中：
```javascript
} else if (document.getElementById('forceMatchDialog').classList.contains('is-visible')) {
    closeForceMatchDialog();
}
```

在之后新增：
```javascript
else if (document.getElementById('batchDetailDrawer').classList.contains('is-visible')) {
    closeBatchDetailDrawer();
}
```

- [ ] **Step 4: 浏览器验证**

1. 归档后 → 批次历史中点击「详情」→ 抽屉打开，显示该批次所有记录
2. 按 Escape → 抽屉关闭
3. 点击遮罩层 → 抽屉关闭

- [ ] **Step 5: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 新增批次详情抽屉 — 展示批次内所有记录明细

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 6: 表格行渲染更新 — 已归档行显示批次标签 + 行样式

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — `renderSystemTable()` (line ~1435-1491) 和 `renderLedgerTable()` (line ~1514+)

- [ ] **Step 1: 修改 renderSystemTable() 中已核对行的渲染**

注意：render 函数处理的 display records 通过 `r.record` 访问原始记录，`archived` 和 `archiveBatchId` 在原始记录上。

在 `renderSystemTable()` 中将：

```javascript
const statusBadge = `<span class="status-badge ${getMatchStatusClass(r.matchStatus)}">${getMatchStatusLabel(r.matchStatus)}</span>`;
```

替换为：

```javascript
var statusLabel = getMatchStatusLabel(r.matchStatus);
var statusClass = getMatchStatusClass(r.matchStatus);
if (r.record.archived && r.record.archiveBatchId) {
    var batch = archiveBatches.find(function(b) { return b.id === r.record.archiveBatchId; });
    statusLabel = '已归档';
    statusClass = 'status-badge--archived';
    if (batch) {
        statusLabel += '<span class="archive-badge">' + batch.label + '</span>';
    }
}
const statusBadge = '<span class="status-badge ' + statusClass + '">' + statusLabel + '</span>';
```

同时修改 actionBtn 中 MATCHED 状态的判断，增加 `!r.record.archived` 条件：

```javascript
} else if (r.matchStatus === MATCH_STATUS.MATCHED && !r.record.archived) {
    actionBtn = `<button class="btn-action" onclick="doCancelMatch('${r.id}')">取消</button>`;
} else if (r.matchStatus === MATCH_STATUS.MATCHED && r.record.archived) {
    actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'system')">详情</button>`;
}
```

修改 rowClass 逻辑，新增 `row-archived`：

```javascript
const rowClass = r.record.archived ? 'row-archived'
    : r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
    : r.matchStatus === MATCH_STATUS.PENDING ? 'row-pending'
    : r.matchStatus === MATCH_STATUS.DIFF ? 'row-diff' : '';
```

- [ ] **Step 2: 修改 renderLedgerTable() 同样逻辑**

在 `renderLedgerTable()` 中做对应修改（通过 `r.record` 访问原始记录）：

statusBadge 替换为：

```javascript
var statusLabel = getMatchStatusLabel(r.matchStatus);
var statusClass = getMatchStatusClass(r.matchStatus);
if (r.record.archived && r.record.archiveBatchId) {
    var batch = archiveBatches.find(function(b) { return b.id === r.record.archiveBatchId; });
    statusLabel = '已归档';
    statusClass = 'status-badge--archived';
    if (batch) {
        statusLabel += '<span class="archive-badge">' + batch.label + '</span>';
    }
}
const statusBadge = '<span class="status-badge ' + statusClass + '">' + statusLabel + '</span>';
```

actionBtn 修改（MATCHED 分支拆分为未归档/已归档）：

```javascript
} else if (r.matchStatus === MATCH_STATUS.MATCHED && !r.record.archived) {
    actionBtn = `<button class="btn-action" onclick="doCancelMatch('${r.id}')">取消</button>`;
} else if (r.matchStatus === MATCH_STATUS.MATCHED && r.record.archived) {
    actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'ledger')">详情</button>`;
}
```

rowClass 修改：

```javascript
const rowClass = r.record.archived ? 'row-archived'
    : r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
    : r.matchStatus === MATCH_STATUS.PENDING ? 'row-pending'
    : r.matchStatus === MATCH_STATUS.DIFF ? 'row-diff' : '';
```

- [ ] **Step 3: 新增 status-badge--archived CSS**

在 `<style>` 块中现有 status-badge 颜色样式之后新增：

```css
.status-badge--archived { background: #E2E8F0; color: #64748B; }
```

- [ ] **Step 4: 浏览器验证**

1. 归档后 → 已核对行背景变灰（#F1F5F9, opacity 0.7）
2. 状态列显示「已归档」+ 「第N批」灰色 tag
3. 操作列从「取消」变为「详情」
4. 未归档的已核对行保持绿色背景和「取消」按钮

- [ ] **Step 5: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 已归档行显示批次标签、灰色背景，操作列改为详情

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 7: 取消核对增加已归档检查

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` — `cancelMatch()` (line ~1138) 和 `doCancelMatch()` 函数

- [ ] **Step 1: 修改 doCancelMatch() 函数增加归档检查**

`doCancelMatch()` 位于 line ~1779，现有代码为：

```javascript
function doCancelMatch(id) {
    cancelMatch(id);
    renderAllTables();
    updateMatchCounts();
    showToast('已取消核对，状态为待确认', 'success');
}
```

替换为：

```javascript
function doCancelMatch(id) {
    var rec = systemRecords.find(function(r) { return r.id === id; });
    if (rec && rec.archived) {
        showToast('已归档记录不可取消核对', 'warning');
        return;
    }
    cancelMatch(id);
    renderAllTables();
    updateMatchCounts();
    showToast('已取消核对，状态为待确认', 'success');
}
```

- [ ] **Step 2: 浏览器验证**

1. 归档一条已核对记录
2. 在未归档的已核对行点击「取消」→ 正常取消
3. 在已归档行（仅有「详情」按钮）→ 不可取消。若有办法触发 cancelMatch（通过控制台），应被拦截

- [ ] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "fix: 已归档记录禁止取消核对

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```

---

### Task 8: 端到端测试 — 多次归档完整流程

- [ ] **Step 1: 启动服务**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/prototype/qingyang-reconciliation-unified.html?ruleName=社保规则A&month=2026-04
```

- [ ] **Step 2: 回合1 — 首次对账+归档**

1. 导入台账 → 开始对账
2. 处理所有 PENDING 记录（确认核对）
3. 处理 DIFF（可选：强制核对）
4. 点击「归档结果」→ 创建「第1批」(toast 显示记录数和金额)
5. 表格行变灰，状态显示「已归档·第1批」
6. 批次历史区域出现，显示第1批信息

- [ ] **Step 3: 回合2 — 模拟新增记录+再次归档**

通过浏览器控制台模拟新增系统侧记录：

```javascript
systemRecords.push({
    id: 'S024', name: '新员工A', idCard: '500382**********99', insuranceType: '养老',
    billingMonth: '2026-04', feeType: 'huijiao', feePeriod: '2026-04', payableMonth: '2026-04',
    amountCompany: 500.00, amountPersonal: 125.00, amount: 625.00,
    matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null,
    remark: null, archiveBatchId: null
});
```

同时追加台账侧记录：

```javascript
ledgerRecords.push({
    id: 'T012', name: '新员工A', idCard: '500382**********99', insuranceType: '养老',
    billingMonth: '2026-04', feePeriod: '2026-04', amount: 625.00,
    matchStatus: MATCH_STATUS.UNMATCHED, matchedSystemId: null, diffType: null, diffAmount: null,
    feeType: null, feeTypeInferred: null, payableMonthInferred: null,
    archived: false, archivedAt: null, archiveBatchId: null,
    importBatchId: 'batch_manual', insuranceSubject: '某科技有限公司', insuranceRule: '社保规则A',
    importedAt: new Date().toLocaleString('zh-CN'), importedBy: 'admin'
});

// 重新对账
executeMatching();
renderAllTables();
updateMatchCounts();
```

3. 表格中：已归档行灰色 + 新记录白色
4. 点击「归档结果」→ 创建「第2批」仅包含新记录(1条)
5. 批次历史：第2批(顶部) + 第1批

- [ ] **Step 4: 验证边界情况**

1. 连续点击「归档结果」→ 第二次提示"无待归档记录"
2. 存在 PENDING/DIFF 时归档 → 弹确认窗
3. 批次详情抽屉 → 只读展示历史批次记录

- [ ] **Step 5: Commit** (如有微调)

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "test: 多次归档端到端流程验证通过

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
```
