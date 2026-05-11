# 已付款状态 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现 PAID 已付款状态——从已归档批次发起付款申请，完成付款后将记录 matchStatus 从 MATCHED 变更为 PAID

**Architecture:** 在现有归档批次抽屉中新增「申请付款」入口；新增付款确认弹窗；`doPayment(batchId)` 遍历批次内所有系统侧 MATCHED 记录→ matchStatus 变更为 PAID；已付款行蓝色背景+「已付款」badge，操作列仅「详情」

**Tech Stack:** Vanilla JS, HTML, CSS — single-file prototype

---

## File to modify

- `prototype/reconciliation/unified.html` — 所有变更集中在该文件

---

### Task 1: 数据模型 — 新增 PAID 常量和已付款行样式

- [ ] **Step 1: 新增 MATCH_STATUS.PAID 常量**

在 `const MATCH_STATUS = { UNMATCHED: 'UNMATCHED', MATCHED: 'MATCHED', PENDING: 'PENDING', DIFF: 'DIFF' };` 中新增：

```javascript
const MATCH_STATUS = {
    UNMATCHED: 'UNMATCHED',
    MATCHED: 'MATCHED',
    PENDING: 'PENDING',
    DIFF: 'DIFF',
    PAID: 'PAID'
};
```

- [ ] **Step 2: 新增已付款行 CSS**

在 `<style>` 块中新增：

```css
.row-paid td { background: #EFF6FF; }
.row-paid:hover td { background: #DBEAFE; }
.status-badge--paid { background: #DBEAFE; color: #1E40AF; }
.status-badge--paid::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; margin-right: 4px; }
```

- [ ] **Step 3: 更新 getMatchStatusLabel 和 getMatchStatusClass**

```javascript
function getMatchStatusLabel(status) {
    const labels = {
        [MATCH_STATUS.MATCHED]: '已核对',
        [MATCH_STATUS.PENDING]: '待确认',
        [MATCH_STATUS.DIFF]: '差异',
        [MATCH_STATUS.UNMATCHED]: '未匹配',
        [MATCH_STATUS.PAID]: '已付款',
    };
    return labels[status] || '—';
}

function getMatchStatusClass(status) {
    const classes = {
        [MATCH_STATUS.MATCHED]: 'status-badge--matched',
        [MATCH_STATUS.PENDING]: 'status-badge--pending',
        [MATCH_STATUS.DIFF]: 'status-badge--diff',
        [MATCH_STATUS.UNMATCHED]: 'status-badge--unmatched',
        [MATCH_STATUS.PAID]: 'status-badge--paid',
    };
    return classes[status] || '';
}
```

- [ ] **Step 4: 提交**

```bash
git add prototype/reconciliation/unified.html
git commit -m "feat: 新增 PAID 常量和已付款行样式"
```

---

### Task 2: 归档批次抽屉新增「申请付款」按钮

- [ ] **Step 1: 修改 openArchiveBatchDrawer() 中批次行 HTML**

在批次列表的「查看此批次」按钮旁新增「申请付款」按钮。修改 `archiveBatches.map` 内的渲染：

```javascript
archiveBatches.map(function(b) {
    return '<tr><td><strong>' + b.label + '</strong><br><span style="font-size:11px;color:var(--qy-text-secondary)">' + b.billingMonth + '</span></td><td>' + b.recordCount + '条</td><td>' + formatMoney(b.totalAmount) + '</td><td style="font-size:11px;">' + b.createdAt + '</td><td><button class="btn-action" onclick="viewArchiveBatch(\'' + b.id + '\')">查看此批次</button> <button class="btn-action" style="color:var(--qy-primary-500);" onclick="showPaymentConfirm(\'' + b.id + '\')">申请付款</button></td></tr>';
}).join('') +
```

- [ ] **Step 2: 提交**

```bash
git add prototype/reconciliation/unified.html
git commit -m "feat: 归档批次抽屉新增申请付款按钮"
```

---

### Task 3: 付款确认弹窗 + doPayment()

- [ ] **Step 1: 新增付款确认弹窗 HTML**

在 `</body>` 前，归档批次抽屉之后新增：

```html
<!-- Payment Confirm Dialog -->
<div class="force-match-dialog" id="paymentDialog" onclick="closePaymentDialog(event)">
    <div class="force-match-dialog__box" onclick="event.stopPropagation()">
        <div class="force-match-dialog__header">
            <h3 class="force-match-dialog__title">付款确认</h3>
            <button class="drawer__close" onclick="closePaymentDialog()">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
        </div>
        <div class="force-match-dialog__body" id="paymentDialogBody"></div>
        <div class="force-match-dialog__footer">
            <button class="qy-btn qy-btn--secondary" onclick="closePaymentDialog()">取消</button>
            <button class="qy-btn qy-btn--primary" id="paymentConfirmBtn" onclick="executePayment()">确认付款</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 新增 JS 函数**

```javascript
let pendingPaymentBatchId = null;

function showPaymentConfirm(batchId) {
    var batch = archiveBatches.find(function(b) { return b.id === batchId; });
    if (!batch) return;

    // 检查该批次中是否有已付款记录
    var sysRecs = systemRecords.filter(function(r) { return r.archiveBatchId === batchId && r.matchStatus === MATCH_STATUS.MATCHED && r.archived; });
    if (sysRecs.length === 0) {
        showToast('该批次无可付款记录（可能已全部付款）', 'warning');
        return;
    }

    pendingPaymentBatchId = batchId;
    var totalAmount = sysRecs.reduce(function(sum, r) { return sum + r.amount; }, 0);

    var body = document.getElementById('paymentDialogBody');
    body.innerHTML = '<p style="font-size:14px;margin-bottom:12px;">确认对 <strong>' + batch.label + '</strong>（' + batch.billingMonth + '）发起付款申请？</p>'
        + '<p style="font-size:12px;color:var(--qy-text-secondary);">共 <strong>' + sysRecs.length + '</strong> 条记录，金额合计 <strong>' + formatMoney(totalAmount) + '</strong></p>'
        + '<p style="font-size:12px;color:var(--qy-text-secondary);margin-top:4px;">操作后这些记录的状态将从「已核对」变更为「已付款」</p>';

    document.getElementById('paymentDialog').classList.add('is-visible');
}

function closePaymentDialog(event) {
    if (event && event.target !== event.currentTarget) return;
    document.getElementById('paymentDialog').classList.remove('is-visible');
    pendingPaymentBatchId = null;
}

function executePayment() {
    closePaymentDialog();
    var batchId = pendingPaymentBatchId;
    if (!batchId) return;

    var count = doPayment(batchId);
    if (count > 0) {
        renderAllTables();
        updateMatchCounts();
        showToast('付款完成：' + count + ' 条记录已变更为已付款', 'success');
    } else {
        showToast('无记录需要付款', 'warning');
    }
    pendingPaymentBatchId = null;
}

function doPayment(batchId) {
    var paid = 0;
    systemRecords.forEach(function(r) {
        if (r.archiveBatchId === batchId && r.matchStatus === MATCH_STATUS.MATCHED && r.archived) {
            r.matchStatus = MATCH_STATUS.PAID;
            paid++;
        }
    });
    // 同步更新台账侧
    systemRecords.forEach(function(sysRec) {
        if (sysRec.archiveBatchId === batchId && sysRec.matchStatus === MATCH_STATUS.PAID && sysRec.matchedLedgerId) {
            var ledRec = ledgerRecords.find(function(r) { return r.id === sysRec.matchedLedgerId; });
            if (ledRec) ledRec.matchStatus = MATCH_STATUS.PAID;
        }
    });
    return paid;
}
```

- [ ] **Step 3: Escape 键处理**

在全局 keydown 监听器中新增：

```javascript
} else if (document.getElementById('paymentDialog').classList.contains('is-visible')) {
    closePaymentDialog();
}
```

- [ ] **Step 4: 提交**

```bash
git add prototype/reconciliation/unified.html
git commit -m "feat: 新增付款确认弹窗 + doPayment() 逻辑"
```

---

### Task 4: 表格渲染 — 已付款行显示

- [ ] **Step 1: 修改 renderSystemTable()**

在状态 badge 渲染和行颜色逻辑中增加 PAID 处理：

状态 badge 渲染（在 `if (r.record.archived)` 块之后新增）：

```javascript
if (r.matchStatus === MATCH_STATUS.PAID) {
    statusLabel = '已付款';
    statusClass = 'status-badge--paid';
}
```

行颜色：

```javascript
const rowClass = r.matchStatus === MATCH_STATUS.PAID ? 'row-paid'
    : r.record.archived ? 'row-archived'
    : r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
    : ...
```

操作按钮（在 MATCHED 分支前新增 PAID 判断）：

```javascript
} else if (r.matchStatus === MATCH_STATUS.PAID) {
    actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', 'system')">详情</button>`;
}
```

- [ ] **Step 2: 修改 renderLedgerTable()**

对台账侧做相同处理（同上）。

- [ ] **Step 3: 更新 getFilteredSystemRecords / getFilteredLedgerRecords**

已付款记录在「已核对」筛选状态下也应展示，确保筛选逻辑正确：

在匹配状态筛选的 `matched` 分支中：

```javascript
} else if (currentSystemMatchFilter === 'matched') {
    records = records.filter(r => r.matchStatus === MATCH_STATUS.MATCHED || r.matchStatus === MATCH_STATUS.PAID);
}
```

- [ ] **Step 4: 提交**

```bash
git add prototype/reconciliation/unified.html
git commit -m "feat: 已付款行蓝色背景+已付款badge+操作列详情"
```

---

### Task 5: 端到端测试 — 归档→付款 完整流程

- [ ] **Step 1: 启动服务**

```bash
python3 -m http.server 8080
# Open http://localhost:8080/prototype/reconciliation/unified.html?ruleName=社保规则A&month=2026-04
```

- [ ] **Step 2: 导入→对账→归档**

1. 导入台账 → 开始对账 → 处理 PENDING（确认核对）→ 处理 DIFF（强制核对或忽略）
2. 归档 → 创建第 1 批
3. 打开「归档记录」抽屉 → 验证「申请付款」按钮可见

- [ ] **Step 3: 测试付款**

1. 点击「申请付款」→ 弹窗显示批次信息和金额
2. 确认付款 → 记录状态变「已付款」
3. 表格行变蓝色，操作列为「详情」
4. 再次点击同一批次「申请付款」→ toast "该批次无可付款记录"

- [ ] **Step 4: 验证边界**

1. 已付款记录不可取消核对（操作列只有「详情」）
2. 筛选「已核对」→ 应包含已付款记录
3. 再次归档（新增记录后）→ 第 2 批可正常付款，第 1 批已付款不受影响
4. 已付款记录在台账侧同步显示

- [ ] **Step 5: 提交**

```bash
git add prototype/reconciliation/unified.html
git commit -m "test: 归档→付款端到端流程验证通过"
```
