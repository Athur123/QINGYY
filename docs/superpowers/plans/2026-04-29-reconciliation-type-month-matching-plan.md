# 社保对账复核：类型/月份互推匹配 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** 在现有统一账单模式对账页面基础上，实现台账导入、精确金额匹配、类型/月份双向回填、待确认抽屉、差异处理、归档的完整对账流程。

**Architecture:** 在 `qingyang-reconciliation-unified.html` 基础上扩展，新增台账导入对话框、确认配对抽屉、差异详情抽屉，新增匹配算法（前端 JavaScript），数据模型从单一 `ALL_RECORDS` 扩展为系统侧+台账侧双数组。

**Tech Stack:** Vanilla HTML/CSS/JS, SheetJS (xlsx CDN) for Excel import/export, existing qingyang design system

---

## File Structure

| File | Action | Responsibility |
|------|--------|----------------|
| `prototype/qingyang-reconciliation-unified.html` | Modify | Main prototype file — add import dialog, matching drawer, diff drawer, matching algorithm, new data model |
| `docs/superpowers/specs/2026-04-29-reconciliation-type-month-matching-design.md` | Reference | Design spec (already written) |

All changes stay within the single HTML prototype file. No new files needed — this is a prototype, not production code. The file is ~950 lines; the final version will be ~1800 lines.

## Task Breakdown

### Task 1: 扩展数据模型 — 系统侧+台账侧双数组

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html:473-522` (data model section)

- [x] **Step 1: Replace the existing data model with system + ledger dual arrays**

Replace lines 473-522 (the entire `<script>` opening through filter states) with:

```javascript
    <script>
        // ========== 数据模型 ==========

        const BILL_TYPES = {
            HUIJIAO: 'huijiao',
            BUJIAO: 'bujiao',
            TIAOJI: 'tiaoji'
        };

        const BILL_TYPE_LABELS = {
            huijiao: '汇缴',
            bujiao: '补缴',
            tiaoji: '调基补差'
        };

        const MATCH_STATUS = {
            UNMATCHED: 'UNMATCHED',
            MATCHED: 'MATCHED',
            PENDING: 'PENDING',
            DIFF: 'DIFF'
        };

        const DIFF_TYPE = {
            SYSTEM_MORE: 'system_more',
            LEDGER_MORE: 'ledger_more',
            AMOUNT_MISMATCH: 'amount_mismatch'
        };

        const VERIFY_STATUS = {
            PENDING: 'PENDING',
            VERIFIED: 'VERIFIED'
        };

        // 险种名称映射表
        const INSURANCE_TYPE_ALIAS = {
            '养老': ['养老', '基本养老保险', '养老保险', '基本养老'],
            '医疗': ['医疗', '基本医疗保险', '医疗保险', '基本医疗'],
            '失业': ['失业', '失业保险', '失业保险金'],
            '工伤': ['工伤', '工伤保险', '工伤保险金'],
            '生育': ['生育', '生育保险', '生育保险金'],
            '公积金': ['公积金', '住房公积金', '住房公积'],
        };

        // 系统侧费用记录
        let systemRecords = [
            { id: 'S001', name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', feeType: 'huijiao', payableMonth: '2026-04', amountCompany: 1000, amountPersonal: 500, amount: 1500, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
            { id: 'S002', name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', feeType: 'bujiao', payableMonth: null, amountCompany: 423.50, amountPersonal: 211.75, amount: 635.25, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
            { id: 'S003', name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', feeType: 'bujiao', payableMonth: null, amountCompany: 256, amountPersonal: 128, amount: 384, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
            { id: 'S004', name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', feeType: 'tiaoji', payableMonth: null, amountCompany: 78, amountPersonal: 39, amount: 117, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
            { id: 'S005', name: '李四', idCard: '430106199102022345', insuranceType: '医疗', billingMonth: '2026-04', feeType: 'bujiao', payableMonth: null, amountCompany: 400, amountPersonal: 200, amount: 600, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
            { id: 'S006', name: '王五', idCard: '430107199203033456', insuranceType: '失业', billingMonth: '2026-04', feeType: 'huijiao', payableMonth: '2026-04', amountCompany: 120, amountPersonal: 30, amount: 150, matchStatus: MATCH_STATUS.UNMATCHED, matchedLedgerId: null, diffType: null, diffAmount: null, remark: null },
        ];

        // 台账侧记录（导入后填充）
        let ledgerRecords = [];

        // 导入元数据
        let importMeta = {
            insuranceSubject: '',       // 参保主体
            insuranceRule: '',          // 参保规则
            billingMonth: '',           // 应缴月份
            importBatchId: null,        // 导入批次号
            importedAt: null,           // 导入时间
        };

        // 对账结果
        let matchingResults = {
            matched: [],
            pending: [],
            diffs: [],
            executed: false,
        };

        // Filter states
        let currentMatchFilter = 'all';    // all / matched / pending / diff
        let currentTypeFilter = 'all';     // all / huijiao / bujiao / tiaoji
        let currentDetailRecord = null;
        let currentPendingGroup = null;    // 当前待确认配对的金额组
```

- [x] **Step 2: Verify the page still loads without errors**

Open the file in a browser and confirm the page renders (table will be empty since ledgerRecords is empty — this is expected).

- [x] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 扩展数据模型 — 系统侧+台账侧双数组，新增匹配状态机"
```

---

### Task 2: 新增工具函数 — 标准化、分组、金额统计

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (add before render functions)

- [x] **Step 1: Add utility functions after the data model section**

Add these functions after the filter state declarations (before `toggleDiffFilter`):

```javascript
        // ========== 工具函数 ==========

        function normalizeIdCard(idCard) {
            if (!idCard) return '';
            return idCard.replace(/\s/g, '').toUpperCase().trim();
        }

        function normalizeInsuranceType(name) {
            if (!name) return '未知';
            const trimmed = name.trim();
            for (const [standard, aliases] of Object.entries(INSURANCE_TYPE_ALIAS)) {
                if (aliases.includes(trimmed)) return standard;
            }
            return '未知';
        }

        function roundToCents(amount) {
            if (typeof amount !== 'number') return null;
            return Math.round(amount * 100) / 100;
        }

        function makeGroupKey(record) {
            return `${normalizeIdCard(record.idCard)}|${normalizeInsuranceType(record.insuranceType)}|${record.billingMonth}`;
        }

        function groupByKey(records, keyFn) {
            const groups = new Map();
            for (const record of records) {
                const key = keyFn(record);
                if (!groups.has(key)) groups.set(key, []);
                groups.get(key).push(record);
            }
            return groups;
        }

        function countByAmount(records) {
            const map = new Map();
            for (const record of records) {
                const amount = record.amount;
                if (!map.has(amount)) map.set(amount, []);
                map.get(amount).push(record);
            }
            return map;
        }

        function formatMoney(v) {
            if (v === null || v === undefined) return '—';
            return '¥' + Number(v).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        }

        function maskIdCard(v) {
            if (!v) return '—';
            return v.replace(/(\d{3})\d{11}(\d{4})/, '$1***********$2');
        }

        function getBillTypeLabel(type) {
            return BILL_TYPE_LABELS[type] || '—';
        }

        function getMatchStatusLabel(status) {
            const labels = {
                [MATCH_STATUS.MATCHED]: '已匹配',
                [MATCH_STATUS.PENDING]: '待确认',
                [MATCH_STATUS.DIFF]: '差异',
                [MATCH_STATUS.UNMATCHED]: '未匹配',
            };
            return labels[status] || '—';
        }

        function getMatchStatusClass(status) {
            const classes = {
                [MATCH_STATUS.MATCHED]: 'status-badge--matched',
                [MATCH_STATUS.PENDING]: 'status-badge--pending',
                [MATCH_STATUS.DIFF]: 'status-badge--diff',
                [MATCH_STATUS.UNMATCHED]: '',
            };
            return classes[status] || '';
        }
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 新增工具函数 — 标准化、分组、金额统计、格式化"
```

---

### Task 3: 实现匹配算法 — executeMatching

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (add after utility functions)

- [x] **Step 1: Add the matching algorithm**

Add after the utility functions section:

```javascript
        // ========== 匹配算法 ==========

        function executeMatching() {
            // Reset
            matchingResults = { matched: [], pending: [], diffs: [], executed: false };
            systemRecords.forEach(r => {
                r.matchStatus = MATCH_STATUS.UNMATCHED;
                r.matchedLedgerId = null;
                r.diffType = null;
                r.diffAmount = null;
            });
            ledgerRecords.forEach(r => {
                r.matchStatus = MATCH_STATUS.UNMATCHED;
                r.matchedSystemId = null;
                r.feeTypeInferred = null;
                r.diffType = null;
                r.diffAmount = null;
            });

            // Group by key
            const sysGroups = groupByKey(systemRecords, makeGroupKey);
            const ledGroups = groupByKey(ledgerRecords, makeGroupKey);
            const allKeys = new Set([...sysGroups.keys(), ...ledGroups.keys()]);

            for (const key of allKeys) {
                const sysRecs = sysGroups.get(key) ?? [];
                const ledRecs = ledGroups.get(key) ?? [];

                const sysAmountMap = countByAmount(sysRecs);
                const ledAmountMap = countByAmount(ledRecs);
                const allAmounts = new Set([...sysAmountMap.keys(), ...ledAmountMap.keys()]);

                for (const amount of allAmounts) {
                    const sysForAmount = sysAmountMap.get(amount) ?? [];
                    const ledForAmount = ledAmountMap.get(amount) ?? [];

                    if (sysForAmount.length > 0 && ledForAmount.length === 0) {
                        // 系统多
                        for (const r of sysForAmount) {
                            r.matchStatus = MATCH_STATUS.DIFF;
                            r.diffType = DIFF_TYPE.SYSTEM_MORE;
                            r.diffAmount = r.amount;
                        }
                        for (const r of sysForAmount) {
                            matchingResults.diffs.push({ systemRecord: r, ledgerRecord: null });
                        }

                    } else if (sysForAmount.length === 0 && ledForAmount.length > 0) {
                        // 台账多
                        for (const r of ledForAmount) {
                            r.matchStatus = MATCH_STATUS.DIFF;
                            r.diffType = DIFF_TYPE.LEDGER_MORE;
                            r.diffAmount = -r.amount;
                        }
                        for (const r of ledForAmount) {
                            matchingResults.diffs.push({ systemRecord: null, ledgerRecord: r });
                        }

                    } else if (sysForAmount.length === 1 && ledForAmount.length === 1) {
                        // 唯一配对
                        const sysRec = sysForAmount[0];
                        const ledRec = ledForAmount[0];
                        sysRec.matchStatus = MATCH_STATUS.MATCHED;
                        sysRec.matchedLedgerId = ledRec.id;
                        ledRec.matchStatus = MATCH_STATUS.MATCHED;
                        ledRec.matchedSystemId = sysRec.id;
                        // 回填
                        sysRec.payableMonth = ledRec.billingMonth;
                        ledRec.feeTypeInferred = sysRec.feeType;
                        matchingResults.matched.push({ systemRecord: sysRec, ledgerRecord: ledRec });

                    } else {
                        // 多笔同金额 → 待确认
                        for (const r of sysForAmount) r.matchStatus = MATCH_STATUS.PENDING;
                        for (const r of ledForAmount) r.matchStatus = MATCH_STATUS.PENDING;
                        matchingResults.pending.push({
                            amount,
                            systemRecords: sysForAmount,
                            ledgerRecords: ledForAmount,
                        });
                    }
                }
            }

            matchingResults.executed = true;
            return matchingResults;
        }

        function confirmPendingPairing(systemId, ledgerId) {
            const sysRec = systemRecords.find(r => r.id === systemId);
            const ledRec = ledgerRecords.find(r => r.id === ledgerId);
            if (!sysRec || !ledRec) return false;

            sysRec.matchStatus = MATCH_STATUS.MATCHED;
            sysRec.matchedLedgerId = ledRec.id;
            ledRec.matchStatus = MATCH_STATUS.MATCHED;
            ledRec.matchedSystemId = sysRec.id;
            // 回填
            sysRec.payableMonth = ledRec.billingMonth;
            ledRec.feeTypeInferred = sysRec.feeType;
            matchingResults.matched.push({ systemRecord: sysRec, ledgerRecord: ledRec });

            // 从 pending 中移除
            matchingResults.pending = matchingResults.pending.filter(g =>
                !(g.systemRecords.some(r => r.id === systemId) && g.ledgerRecords.some(r => r.id === ledgerId))
            );
            return true;
        }

        function cancelMatch(recordId) {
            const sysRec = systemRecords.find(r => r.id === recordId);
            const ledRec = ledgerRecords.find(r => r.id === recordId);
            if (sysRec) {
                sysRec.matchStatus = MATCH_STATUS.UNMATCHED;
                sysRec.matchedLedgerId = null;
                sysRec.payableMonth = sysRec.feeType === 'huijiao' ? sysRec.billingMonth : null;
            }
            if (ledRec) {
                ledRec.matchStatus = MATCH_STATUS.UNMATCHED;
                ledRec.matchedSystemId = null;
                ledRec.feeTypeInferred = null;
            }
            matchingResults.matched = matchingResults.matched.filter(
                m => m.systemRecord.id !== recordId && m.ledgerRecord.id !== recordId
            );
        }

        function markDiffHandled(recordId) {
            const sysRec = systemRecords.find(r => r.id === recordId);
            const ledRec = ledgerRecords.find(r => r.id === recordId);
            if (sysRec && sysRec.matchStatus === MATCH_STATUS.DIFF) {
                sysRec.remark = '已处理';
            }
            if (ledRec && ledRec.matchStatus === MATCH_STATUS.DIFF) {
                ledRec.remark = '已处理';
            }
        }
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 实现匹配算法 — executeMatching + confirmPendingPairing + cancelMatch"
```

---

### Task 4: 新增 UI 组件 CSS — 导入对话框、配对抽屉、差异抽屉

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (add CSS in `<style>` block)

- [x] **Step 1: Add new CSS classes before the closing `</style>` tag**

Find the closing `</style>` tag and add these classes before it:

```css
        /* Import Dialog */
        .import-dialog { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.45); z-index: 1001; display: none; align-items: center; justify-content: center; }
        .import-dialog.is-visible { display: flex; }
        .import-dialog__box { background: var(--qy-bg-primary); border-radius: var(--qy-radius-lg); width: 520px; max-width: 90%; box-shadow: var(--qy-shadow-lg); }
        .import-dialog__header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid var(--qy-border-light); }
        .import-dialog__title { font-size: 16px; font-weight: 600; }
        .import-dialog__body { padding: 20px; }
        .import-dialog__footer { display: flex; justify-content: flex-end; gap: 12px; padding: 16px 20px; border-top: 1px solid var(--qy-border-light); }

        .form-group { margin-bottom: 16px; }
        .form-group__label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 6px; }
        .form-group__input, .form-group__select { width: 100%; height: 36px; padding: 0 12px; border: 1px solid var(--qy-border-medium); border-radius: var(--qy-radius-md); font-size: 13px; }
        .form-group__input:focus, .form-group__select:focus { outline: none; border-color: var(--qy-primary-400); box-shadow: var(--qy-shadow-focus); }

        .drop-zone { border: 2px dashed var(--qy-border-medium); border-radius: var(--qy-radius-md); padding: 32px; text-align: center; cursor: pointer; transition: border-color var(--qy-transition-fast); }
        .drop-zone:hover, .drop-zone.is-dragover { border-color: var(--qy-primary-400); background: var(--qy-primary-50); }
        .drop-zone__text { font-size: 14px; color: var(--qy-text-secondary); }
        .drop-zone__hint { font-size: 12px; color: var(--qy-text-muted); margin-top: 8px; }

        .import-preview__error { background: #FEF2F2; border: 1px solid #FECACA; border-radius: var(--qy-radius-md); padding: 12px; margin-bottom: 12px; font-size: 12px; color: #991B1B; }
        .import-preview__table { font-size: 12px; }

        /* Matching Stats */
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px; }
        .stat-card { padding: 14px 16px; border: 1px solid var(--qy-border-light); border-radius: var(--qy-radius-lg); background: var(--qy-bg-primary); }
        .stat-card__label { font-size: 12px; color: var(--qy-text-muted); margin-bottom: 4px; }
        .stat-card__value { font-size: 22px; font-weight: 700; }
        .stat-card__amount { font-size: 13px; color: var(--qy-text-secondary); margin-top: 4px; }
        .stat-card--total { border-left: 3px solid var(--qy-text-muted); }
        .stat-card--total .stat-card__value { color: var(--qy-text-primary); }
        .stat-card--matched { border-left: 3px solid #16A34A; }
        .stat-card--matched .stat-card__value { color: #16A34A; }
        .stat-card--pending { border-left: 3px solid #CA8A04; }
        .stat-card--pending .stat-card__value { color: #CA8A04; }
        .stat-card--diff { border-left: 3px solid #DC2626; }
        .stat-card--diff .stat-card__value { color: #DC2626; }

        /* Match Status Badges */
        .status-badge--matched { background: #DCFCE7; color: #166534; }
        .status-badge--matched::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; margin-right: 4px; }
        .status-badge--pending { background: #FEF3C7; color: #854D0E; }
        .status-badge--pending::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; margin-right: 4px; }
        .status-badge--diff { background: #FEE2E2; color: #991B1B; }
        .status-badge--diff::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; margin-right: 4px; }

        /* Row color variants */
        .row-matched td { background: #F0FDF4; }
        .row-matched:hover td { background: #DCFCE7; }
        .row-pending td { background: #FEFCE8; }
        .row-pending:hover td { background: #FEF3C7; }
        .row-diff td { background: #FEF2F2; }
        .row-diff:hover td { background: #FEE2E2; }

        /* Pairing Drawer */
        .pairing-section { margin-bottom: 16px; }
        .pairing-section__title { font-size: 13px; font-weight: 600; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid var(--qy-border-light); }
        .pairing-recommendation { background: var(--qy-bg-secondary); border-radius: var(--qy-radius-md); padding: 12px; margin-bottom: 12px; }
        .pairing-row { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid var(--qy-border-light); }
        .pairing-row:last-child { border-bottom: none; }
        .pairing-row__check { width: 18px; height: 18px; accent-color: var(--qy-primary-500); }
        .pairing-row__label { font-size: 12px; color: var(--qy-text-secondary); flex-shrink: 0; min-width: 120px; }
        .pairing-row__arrow { color: var(--qy-text-muted); }
        .pairing-row__select { flex: 1; height: 32px; padding: 0 28px 0 10px; border: 1px solid var(--qy-border-medium); border-radius: var(--qy-radius-sm); font-size: 12px; appearance: none; background: var(--qy-bg-primary) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' stroke-width='2'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E") no-repeat right 8px center; }
        .pairing-hint { font-size: 12px; color: var(--qy-text-muted); margin-top: 8px; padding: 8px; background: #EFF6FF; border-radius: var(--qy-radius-sm); }

        /* Diff analysis */
        .diff-analysis { background: var(--qy-bg-secondary); border-radius: var(--qy-radius-md); padding: 14px; }
        .diff-analysis__title { font-size: 12px; font-weight: 600; margin-bottom: 8px; }
        .diff-analysis__cause { font-size: 12px; color: var(--qy-text-secondary); line-height: 1.6; }
        .diff-analysis__cause ul { margin: 4px 0; padding-left: 16px; }

        /* Loading overlay */
        .loading-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(255,255,255,0.8); z-index: 2000; display: none; align-items: center; justify-content: center; }
        .loading-overlay.is-visible { display: flex; }
        .loading-spinner { text-align: center; }
        .loading-spinner__icon { font-size: 32px; animation: spin 1s linear infinite; }
        .loading-spinner__text { font-size: 14px; color: var(--qy-text-secondary); margin-top: 12px; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

        /* Info table in drawer */
        .info-table { width: 100%; border-collapse: collapse; font-size: 13px; }
        .info-table th { text-align: left; padding: 8px; background: var(--qy-bg-secondary); font-size: 12px; color: var(--qy-text-muted); border-bottom: 1px solid var(--qy-border-light); }
        .info-table td { padding: 8px; border-bottom: 1px solid var(--qy-border-light); }
        .info-table .amount-breakdown { font-size: 11px; color: var(--qy-text-muted); }

        /* Confirm overlay */
        .confirm-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.45); z-index: 1002; display: none; align-items: center; justify-content: center; }
        .confirm-overlay.is-visible { display: flex; }
        .confirm-box { background: var(--qy-bg-primary); border-radius: var(--qy-radius-lg); width: 400px; max-width: 90%; box-shadow: var(--qy-shadow-lg); padding: 24px; }
        .confirm-box__title { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
        .confirm-box__text { font-size: 14px; color: var(--qy-text-secondary); margin-bottom: 20px; line-height: 1.6; }
        .confirm-box__footer { display: flex; justify-content: flex-end; gap: 12px; }
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 新增UI组件CSS — 导入对话框、配对抽屉、差异分析、loading、统计卡片"
```

---

### Task 5: 改造页面 HTML — 新布局、统计卡片、筛选条

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html` (HTML body section, lines ~276-448)

- [x] **Step 1: Replace the page body content (summary cards, filter bar, table header)**

Replace the section from `<!-- Summary Cards -->` through the table header `<thead>` (approximately lines 306-435) with:

```html
                <!-- Summary Stats -->
                <div class="stats-grid" id="statsGrid">
                    <div class="stat-card stat-card--total">
                        <div class="stat-card__label">总记录数</div>
                        <div class="stat-card__value" id="statTotal">0</div>
                        <div class="stat-card__amount" id="statTotalAmount">¥0.00</div>
                    </div>
                    <div class="stat-card stat-card--matched">
                        <div class="stat-card__label">已匹配</div>
                        <div class="stat-card__value" id="statMatched">0</div>
                        <div class="stat-card__amount" id="statMatchedAmount">¥0.00</div>
                    </div>
                    <div class="stat-card stat-card--pending">
                        <div class="stat-card__label">待确认</div>
                        <div class="stat-card__value" id="statPending">0</div>
                        <div class="stat-card__amount" id="statPendingAmount">¥0.00</div>
                    </div>
                    <div class="stat-card stat-card--diff">
                        <div class="stat-card__label">差异</div>
                        <div class="stat-card__value" id="statDiff">0</div>
                        <div class="stat-card__amount" id="statDiffAmount">¥0.00</div>
                    </div>
                </div>

                <!-- Match Status Filter -->
                <div class="filter-bar" id="matchFilterBar">
                    <span class="filter-bar__label">匹配状态</span>
                    <div class="filter-bar__group">
                        <div class="filter-bar__item filter-bar__item--match-all is-active" data-match="all" onclick="toggleMatchFilter('all')">
                            全部 <span class="filter-bar__count" id="matchCountAll">0</span>
                        </div>
                        <div class="filter-bar__item filter-bar__item--matched" data-match="matched" onclick="toggleMatchFilter('matched')">
                            已匹配 <span class="filter-bar__count" id="matchCountMatched">0</span>
                        </div>
                        <div class="filter-bar__item filter-bar__item--pending" data-match="pending" onclick="toggleMatchFilter('pending')">
                            待确认 <span class="filter-bar__count" id="matchCountPending">0</span>
                        </div>
                        <div class="filter-bar__item filter-bar__item--diff" data-match="diff" onclick="toggleMatchFilter('diff')">
                            差异 <span class="filter-bar__count" id="matchCountDiff">0</span>
                        </div>
                    </div>
                    <div class="filter-bar__divider"></div>
                    <span class="filter-bar__label">账单类型</span>
                    <div class="filter-bar__group">
                        <div class="filter-bar__item filter-bar__item--type-all is-active" data-type="all" onclick="toggleTypeFilter('all')">
                            全部
                        </div>
                        <div class="filter-bar__item filter-bar__item--huijiao" data-type="huijiao" onclick="toggleTypeFilter('huijiao')">
                            汇缴
                        </div>
                        <div class="filter-bar__item filter-bar__item--bujiao" data-type="bujiao" onclick="toggleTypeFilter('bujiao')">
                            补缴
                        </div>
                        <div class="filter-bar__item filter-bar__item--tiaoji" data-type="tiaoji" onclick="toggleTypeFilter('tiaoji')">
                            调基补差
                        </div>
                    </div>
                </div>

                <!-- Data Table -->
                <div id="unifiedTable">
                    <div class="data-table">
                        <table class="qy-table">
                            <thead>
                                <tr>
                                    <th><input type="checkbox" onchange="toggleSelectAll()"></th>
                                    <th>匹配状态</th>
                                    <th>账单类型</th>
                                    <th>姓名</th>
                                    <th>身份证号</th>
                                    <th>险种</th>
                                    <th>应缴月份</th>
                                    <th>系统金额</th>
                                    <th>台账金额</th>
                                    <th>差异</th>
                                    <th>操作</th>
                                </tr>
                            </thead>
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 改造页面HTML — 统计卡片、匹配状态筛选条、新表格头"
```

---

### Task 6: 实现台账导入功能

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [x] **Step 1: Add import dialog HTML before the closing `</body>` tag (before existing drawer HTML)**

Add before the `<div class="toast-container">` line:

```html
    <!-- Import Dialog -->
    <div class="import-dialog" id="importDialog" onclick="closeImportDialog(event)">
        <div class="import-dialog__box" onclick="event.stopPropagation()">
            <div class="import-dialog__header">
                <h3 class="import-dialog__title">导入税务台账</h3>
                <button class="drawer__close" onclick="closeImportDialog()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>
            <div class="import-dialog__body" id="importDialogBody">
                <!-- Step 1: File selection -->
                <div id="importStep1">
                    <div class="form-group">
                        <label class="form-group__label">参保主体</label>
                        <select class="form-group__select" id="importSubject">
                            <option value="">请选择</option>
                            <option value="某科技有限公司">某科技有限公司</option>
                            <option value="另一家公司">另一家公司</option>
                            <option value="第三家公司">第三家公司</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-group__label">参保规则</label>
                        <select class="form-group__select" id="importRule">
                            <option value="">请选择</option>
                            <option value="社保规则A">社保规则A</option>
                            <option value="社保规则B">社保规则B</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-group__label">应缴月份</label>
                        <select class="form-group__select" id="importMonth">
                            <option value="2026-04">2026-04</option>
                            <option value="2026-03">2026-03</option>
                        </select>
                    </div>
                    <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
                        <div class="drop-zone__text">📁 拖拽文件到此处，或点击选择文件</div>
                        <div class="drop-zone__hint">支持格式：.xlsx, .xls</div>
                        <input type="file" id="fileInput" accept=".xlsx,.xls" style="display:none" onchange="handleFileSelect(event)">
                    </div>
                </div>
                <!-- Step 2: Preview (hidden initially) -->
                <div id="importStep2" style="display:none;">
                    <p style="font-size:13px;margin-bottom:12px;" id="importPreviewSummary"></p>
                    <div id="importPreviewErrors"></div>
                    <table class="qy-table import-preview__table" id="importPreviewTable">
                        <thead>
                            <tr><th>姓名</th><th>身份证</th><th>险种</th><th>月份</th><th>金额</th><th>状态</th></tr>
                        </thead>
                        <tbody id="importPreviewBody"></tbody>
                    </table>
                </div>
            </div>
            <div class="import-dialog__footer" id="importDialogFooter">
                <button class="qy-btn qy-btn--secondary" onclick="closeImportDialog()">取消</button>
                <button class="qy-btn qy-btn--primary" id="importNextBtn" onclick="importNextStep()">下一步</button>
            </div>
        </div>
    </div>

    <!-- Confirm Overlay -->
    <div class="confirm-overlay" id="confirmOverlay">
        <div class="confirm-box">
            <div class="confirm-box__title" id="confirmTitle">确认</div>
            <div class="confirm-box__text" id="confirmText"></div>
            <div class="confirm-box__footer">
                <button class="qy-btn qy-btn--secondary" onclick="closeConfirm(false)">取消</button>
                <button class="qy-btn qy-btn--primary" onclick="closeConfirm(true)">确认</button>
            </div>
        </div>
    </div>

    <!-- Loading Overlay -->
    <div class="loading-overlay" id="loadingOverlay">
        <div class="loading-spinner">
            <div class="loading-spinner__icon">⏳</div>
            <div class="loading-spinner__text" id="loadingText">正在对账...</div>
        </div>
    </div>
```

- [x] **Step 2: Add import JavaScript functions**

Add before the `// ========== Init ==========` section:

```javascript
        // ========== 台账导入 ==========

        let importFileData = null;  // Parsed Excel data

        function openImportDialog() {
            document.getElementById('importStep1').style.display = 'block';
            document.getElementById('importStep2').style.display = 'none';
            document.getElementById('importDialog').classList.add('is-visible');
            importFileData = null;
            document.getElementById('importNextBtn').textContent = '下一步';
        }

        function closeImportDialog(event) {
            if (event && event.target !== event.currentTarget) return;
            document.getElementById('importDialog').classList.remove('is-visible');
            importFileData = null;
        }

        // Drag and drop
        document.addEventListener('DOMContentLoaded', () => {
            const dropZone = document.getElementById('dropZone');
            if (dropZone) {
                dropZone.addEventListener('dragover', (e) => {
                    e.preventDefault();
                    dropZone.classList.add('is-dragover');
                });
                dropZone.addEventListener('dragleave', () => {
                    dropZone.classList.remove('is-dragover');
                });
                dropZone.addEventListener('drop', (e) => {
                    e.preventDefault();
                    dropZone.classList.remove('is-dragover');
                    const file = e.dataTransfer.files[0];
                    if (file) processFile(file);
                });
            }
        });

        function handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) processFile(file);
        }

        function processFile(file) {
            // In a prototype, we simulate parsing. In production, use SheetJS (xlsx)
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    // Try to parse as Excel if SheetJS is loaded
                    if (typeof XLSX !== 'undefined') {
                        const workbook = XLSX.read(e.target.result, { type: 'array' });
                        const sheetName = workbook.SheetNames[0];
                        const sheet = workbook.Sheets[sheetName];
                        const data = XLSX.utils.sheet_to_json(sheet);
                        parseImportData(data);
                    } else {
                        // Fallback: use mock data for demo
                        useMockImportData();
                    }
                } catch (err) {
                    showToast('文件解析失败: ' + err.message, 'error');
                }
            };
            reader.readAsArrayBuffer(file);
        }

        function useMockImportData() {
            // Mock data for prototype demo
            importFileData = {
                successRows: [
                    { name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', amount: 1500 },
                    { name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', amount: 635.25 },
                    { name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', amount: 384 },
                    { name: '张三', idCard: '430105199001011234', insuranceType: '养老', billingMonth: '2026-04', amount: 117 },
                    { name: '李四', idCard: '430106199102022345', insuranceType: '医疗', billingMonth: '2026-04', amount: 450 },
                    { name: '王五', idCard: '430107199203033456', insuranceType: '失业', billingMonth: '2026-04', amount: 142.50 },
                    { name: '赵六', idCard: '430108199304044567', insuranceType: '养老', billingMonth: '2026-04', amount: 823 },
                ],
                errorRows: [],
            };
            showImportPreview();
        }

        function parseImportData(rawData) {
            const successRows = [];
            const errorRows = [];

            rawData.forEach((row, index) => {
                const errors = [];

                // Validate required fields
                if (!row['身份证']) errors.push('身份证为空');
                if (!row['险种']) errors.push('险种为空');
                if (!row['应缴月份']) errors.push('应缴月份为空');
                if (row['金额'] === undefined || row['金额'] === null) errors.push('金额为空');

                if (errors.length > 0) {
                    errorRows.push({ row: index + 2, errors });
                    return;
                }

                successRows.push({
                    name: row['姓名'] || '',
                    idCard: normalizeIdCard(String(row['身份证'])),
                    insuranceType: normalizeInsuranceType(String(row['险种'])),
                    billingMonth: String(row['应缴月份']).replace(/(\d{4})(\d{2})/, '$1-$2'),
                    amount: roundToCents(Number(row['金额'])),
                });
            });

            importFileData = { successRows, errorRows };
            showImportPreview();
        }

        function showImportPreview() {
            document.getElementById('importStep1').style.display = 'none';
            document.getElementById('importStep2').style.display = 'block';
            document.getElementById('importNextBtn').textContent = '确认导入';

            const { successRows, errorRows } = importFileData;
            document.getElementById('importPreviewSummary').textContent =
                `导入结果：成功 ${successRows.length} 条 / 格式错误 ${errorRows.length} 条`;

            // Show errors
            const errorDiv = document.getElementById('importPreviewErrors');
            if (errorRows.length > 0) {
                errorDiv.innerHTML = '<div class="import-preview__error">' +
                    errorRows.map(e => `第 ${e.row} 行：${e.errors.join('、')}`).join('<br>') +
                    '</div>';
            } else {
                errorDiv.innerHTML = '';
            }

            // Preview table
            const tbody = document.getElementById('importPreviewBody');
            tbody.innerHTML = successRows.slice(0, 10).map(r =>
                `<tr><td>${r.name}</td><td>${maskIdCard(r.idCard)}</td><td>${r.insuranceType}</td><td>${r.billingMonth}</td><td>${formatMoney(r.amount)}</td><td style="color:#16A34A;">✅</td></tr>`
            ).join('') + (successRows.length > 10 ? `<tr><td colspan="6">... 还有 ${successRows.length - 10} 条</td></tr>` : '');
        }

        function importNextStep() {
            if (document.getElementById('importStep1').style.display !== 'none') {
                // Step 1 → load mock data (user hasn't selected a file yet)
                useMockImportData();
                return;
            }

            // Confirm import
            const { successRows } = importFileData;
            ledgerRecords = successRows.map((r, i) => ({
                id: 'T' + String(i + 1).padStart(3, '0'),
                name: r.name,
                idCard: r.idCard,
                insuranceType: r.insuranceType,
                billingMonth: r.billingMonth,
                amount: r.amount,
                feeType: null,
                feeTypeInferred: null,
                matchStatus: MATCH_STATUS.UNMATCHED,
                matchedSystemId: null,
                diffType: null,
                diffAmount: null,
                remark: null,
            }));

            importMeta = {
                insuranceSubject: document.getElementById('importSubject').value,
                insuranceRule: document.getElementById('importRule').value,
                billingMonth: document.getElementById('importMonth').value,
                importBatchId: 'batch_' + Date.now(),
                importedAt: new Date().toLocaleString('zh-CN'),
            };

            closeImportDialog();
            updateStats();
            updateMatchCounts();
            renderTable();
            showToast(`导入成功：${successRows.length} 条记录`, 'success');
        }
```

- [x] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 实现台账导入功能 — 对话框、拖拽上传、预览、Mock数据"
```

---

### Task 7: 实现渲染函数 — 统计卡片、筛选、数据表格

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [x] **Step 1: Replace old filter/render functions with new ones**

Replace `toggleDiffFilter`, `getFilteredRecords`, `renderTable`, `updateCounts` functions with:

```javascript
        // ========== 筛选与渲染 ==========

        function toggleMatchFilter(filterType) {
            currentMatchFilter = filterType;
            document.querySelectorAll('.filter-bar__item[data-match]').forEach(item => {
                item.classList.toggle('is-active', item.dataset.match === filterType);
            });
            renderTable();
        }

        function toggleTypeFilter(type) {
            currentTypeFilter = type;
            document.querySelectorAll('.filter-bar__item[data-type]').forEach(item => {
                item.classList.toggle('is-active', item.dataset.type === type);
            });
            renderTable();
        }

        function getAllDisplayRecords() {
            // Combine system and ledger records into display rows
            const records = [];
            const processedLedgerIds = new Set();

            for (const sysRec of systemRecords) {
                const ledRec = sysRec.matchedLedgerId
                    ? ledgerRecords.find(r => r.id === sysRec.matchedLedgerId)
                    : null;

                records.push({
                    id: sysRec.id,
                    side: 'system',
                    name: sysRec.name,
                    idCard: sysRec.idCard,
                    insuranceType: sysRec.insuranceType,
                    billingMonth: sysRec.billingMonth,
                    feeType: sysRec.feeType,
                    sysCompany: sysRec.amountCompany,
                    sysPersonal: sysRec.amountPersonal,
                    sysAmount: sysRec.amount,
                    ledgerCompany: ledRec ? null : null,
                    ledgerPersonal: null,
                    ledgerAmount: ledRec ? ledRec.amount : null,
                    matchStatus: sysRec.matchStatus,
                    diffType: sysRec.diffType,
                    diffAmount: sysRec.diffAmount,
                    record: sysRec,
                    ledgerRecord: ledRec,
                });

                if (ledRec) processedLedgerIds.add(ledRec.id);
            }

            // Add ledger-only records
            for (const ledRec of ledgerRecords) {
                if (!processedLedgerIds.has(ledRec.id)) {
                    records.push({
                        id: ledRec.id,
                        side: 'ledger',
                        name: ledRec.name,
                        idCard: ledRec.idCard,
                        insuranceType: ledRec.insuranceType,
                        billingMonth: ledRec.billingMonth,
                        feeType: ledRec.feeTypeInferred || '—',
                        sysCompany: null,
                        sysPersonal: null,
                        sysAmount: null,
                        ledgerCompany: null,
                        ledgerPersonal: null,
                        ledgerAmount: ledRec.amount,
                        matchStatus: ledRec.matchStatus,
                        diffType: ledRec.diffType,
                        diffAmount: ledRec.diffAmount,
                        record: ledRec,
                        ledgerRecord: ledRec,
                    });
                }
            }

            return records;
        }

        function getFilteredRecords() {
            let records = getAllDisplayRecords();

            // Match status filter
            if (currentMatchFilter !== 'all') {
                records = records.filter(r => r.matchStatus === currentMatchFilter.toUpperCase() ||
                    (currentMatchFilter === 'matched' && r.matchStatus === MATCH_STATUS.MATCHED) ||
                    (currentMatchFilter === 'pending' && r.matchStatus === MATCH_STATUS.PENDING) ||
                    (currentMatchFilter === 'diff' && r.matchStatus === MATCH_STATUS.DIFF));
            }

            // Type filter
            if (currentTypeFilter !== 'all') {
                records = records.filter(r => r.feeType === currentTypeFilter);
            }

            // Name search
            const nameVal = document.getElementById('filterName')?.value?.trim();
            if (nameVal) {
                records = records.filter(r =>
                    r.name.includes(nameVal) || r.idCard.includes(nameVal)
                );
            }

            return records;
        }

        function renderTable() {
            const tbody = document.getElementById('unifiedTableBody');
            if (!tbody) return;
            const records = getFilteredRecords();

            tbody.innerHTML = records.map(r => {
                const statusBadge = `<span class="status-badge ${getMatchStatusClass(r.matchStatus)}">${getMatchStatusLabel(r.matchStatus)}</span>`;
                const typeBadge = r.feeType !== '—' ? `<span class="type-badge type-badge--${r.feeType}">${getBillTypeLabel(r.feeType)}</span>` : '';

                // Diff display
                let diffStr = '—';
                if (r.diffAmount !== null && r.diffAmount !== 0) {
                    diffStr = (r.diffAmount > 0 ? '+' : '') + formatMoney(r.diffAmount);
                }

                // Action button
                let actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', '${r.side}')">详情</button>`;
                if (r.matchStatus === MATCH_STATUS.PENDING) {
                    actionBtn = `<button class="btn-action" onclick="openPairingDrawer('${r.id}')">确认配对</button>`;
                } else if (r.matchStatus === MATCH_STATUS.MATCHED) {
                    actionBtn = `<button class="btn-action" onclick="cancelMatch('${r.id}'); renderTable(); updateStats(); updateMatchCounts(); showToast('已取消匹配', 'success');">取消</button>`;
                } else if (r.matchStatus === MATCH_STATUS.DIFF) {
                    actionBtn = `<button class="btn-action" onclick="showNewDetail('${r.id}', '${r.side}')">详情</button>`;
                }

                const rowClass = r.matchStatus === MATCH_STATUS.MATCHED ? 'row-matched'
                    : r.matchStatus === MATCH_STATUS.PENDING ? 'row-pending'
                    : r.matchStatus === MATCH_STATUS.DIFF ? 'row-diff' : '';

                return `<tr class="${rowClass}" data-id="${r.id}">
                    <td><input type="checkbox" class="row-checkbox" data-id="${r.id}" data-side="${r.side}" onchange="updateBatchButtons()"></td>
                    <td>${statusBadge}</td>
                    <td>${typeBadge}</td>
                    <td><strong>${r.name}</strong></td>
                    <td>${maskIdCard(r.idCard)}</td>
                    <td>${r.insuranceType}</td>
                    <td>${r.billingMonth}</td>
                    <td>${r.sysAmount !== null ? formatMoney(r.sysAmount) : '—'}</td>
                    <td>${r.ledgerAmount !== null ? formatMoney(r.ledgerAmount) : '—'}</td>
                    <td style="color: ${r.diffAmount && r.diffAmount !== 0 ? '#DC2626' : 'inherit'}; font-weight: ${r.diffAmount && r.diffAmount !== 0 ? '600' : '400'}">${diffStr}</td>
                    <td>${actionBtn}</td>
                </tr>`;
            }).join('');

            document.getElementById('tableFooterInfo').innerHTML = `共 <strong>${records.length}</strong> 条 / 1页`;
            updateBatchButtons();
        }

        function updateStats() {
            const allSys = systemRecords;
            const allLed = ledgerRecords;

            const matchedCount = allSys.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
            const pendingCount = allSys.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
            const diffCount = allSys.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;
            const totalCount = allSys.length + allLed.filter(r => !allSys.some(s => s.matchedLedgerId === r.id)).length;

            const matchedAmount = allSys.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).reduce((s, r) => s + r.amount, 0);
            const pendingAmount = allSys.filter(r => r.matchStatus === MATCH_STATUS.PENDING).reduce((s, r) => s + r.amount, 0);
            const diffAmount = allSys.filter(r => r.matchStatus === MATCH_STATUS.DIFF).reduce((s, r) => s + Math.abs(r.diffAmount || 0), 0);

            document.getElementById('statTotal').textContent = totalCount;
            document.getElementById('statTotalAmount').textContent = formatMoney(allSys.reduce((s, r) => s + r.amount, 0) + allLed.reduce((s, r) => s + r.amount, 0));
            document.getElementById('statMatched').textContent = matchedCount;
            document.getElementById('statMatchedAmount').textContent = formatMoney(matchedAmount);
            document.getElementById('statPending').textContent = pendingCount;
            document.getElementById('statPendingAmount').textContent = formatMoney(pendingAmount);
            document.getElementById('statDiff').textContent = diffCount;
            document.getElementById('statDiffAmount').textContent = formatMoney(diffAmount);
        }

        function updateMatchCounts() {
            const all = getAllDisplayRecords();
            const matchedCount = all.filter(r => r.matchStatus === MATCH_STATUS.MATCHED).length;
            const pendingCount = all.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
            const diffCount = all.filter(r => r.matchStatus === MATCH_STATUS.DIFF).length;
            const totalCount = all.length;

            document.getElementById('matchCountAll').textContent = totalCount;
            document.getElementById('matchCountMatched').textContent = matchedCount;
            document.getElementById('matchCountPending').textContent = pendingCount;
            document.getElementById('matchCountDiff').textContent = diffCount;
        }
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 实现渲染函数 — 统计卡片、匹配筛选、数据表格、计数更新"
```

---

### Task 8: 实现确认配对抽屉

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [x] **Step 1: Add pairing drawer HTML and JS**

Add the pairing drawer HTML before the existing detail drawer:

```html
    <!-- Pairing Drawer -->
    <div class="drawer-overlay" id="pairingDrawer" onclick="closePairingDrawer(event)">
        <div class="drawer" style="width: 600px;">
            <div class="drawer__header">
                <h3 class="drawer__title" id="pairingDrawerTitle">确认配对</h3>
                <button class="drawer__close" onclick="closePairingDrawer()">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                </button>
            </div>
            <div class="drawer__body" id="pairingDrawerBody"></div>
            <div class="drawer__footer">
                <button class="qy-btn qy-btn--secondary" onclick="closePairingDrawer()">取消</button>
                <button class="qy-btn qy-btn--primary" id="pairingConfirmBtn" onclick="confirmPairing()">确认全部配对</button>
            </div>
        </div>
    </div>
```

Add JS functions before the init section:

```javascript
        // ========== 确认配对抽屉 ==========

        let currentPairingGroup = null;
        let pairingSelections = {};  // { systemId: ledgerId }

        function openPairingDrawer(systemId) {
            const sysRec = systemRecords.find(r => r.id === systemId);
            if (!sysRec || sysRec.matchStatus !== MATCH_STATUS.PENDING) return;

            // Find the pending group for this record
            const group = matchingResults.pending.find(g =>
                g.systemRecords.some(r => r.id === systemId)
            );
            if (!group) return;

            currentPairingGroup = group;
            // Default pairing: Nth system ↔ Nth ledger
            pairingSelections = {};
            group.systemRecords.forEach((sys, i) => {
                if (group.ledgerRecords[i]) {
                    pairingSelections[sys.id] = group.ledgerRecords[i].id;
                }
            });

            renderPairingDrawer();
            document.getElementById('pairingDrawer').classList.add('is-visible');
        }

        function closePairingDrawer(event) {
            if (event && event.target !== event.currentTarget) return;
            document.getElementById('pairingDrawer').classList.remove('is-visible');
            currentPairingGroup = null;
            pairingSelections = {};
        }

        function renderPairingDrawer() {
            const group = currentPairingGroup;
            if (!group) return;

            const firstSys = group.systemRecords[0];
            const body = document.getElementById('pairingDrawerBody');

            let html = `
                <div class="drawer-section">
                    <div class="drawer-row">
                        <span class="drawer-row__label">员工</span>
                        <span class="drawer-row__value">${firstSys.name}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">险种</span>
                        <span class="drawer-row__value">${firstSys.insuranceType}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">应缴月份</span>
                        <span class="drawer-row__value">${firstSys.billingMonth}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">同金额待确认</span>
                        <span class="drawer-row__value">${formatMoney(group.amount)}（系统${group.systemRecords.length}笔 / 台账${group.ledgerRecords.length}笔）</span>
                    </div>
                </div>

                <div class="pairing-section">
                    <div class="pairing-section__title">智能推荐配对</div>
                    <div class="pairing-recommendation">
            `;

            // Show recommended pairings
            group.systemRecords.forEach((sys, i) => {
                const led = group.ledgerRecords[i];
                const isChecked = pairingSelections[sys.id] === led?.id;
                html += `
                    <div class="pairing-row">
                        <input type="checkbox" class="pairing-row__check" ${isChecked ? 'checked' : ''} onchange="togglePairingCheck('${sys.id}')" id="pairCheck_${sys.id}">
                        <span class="pairing-row__label">${getBillTypeLabel(sys.feeType)} ${formatMoney(sys.amount)}</span>
                        <span class="pairing-row__arrow">→</span>
                        <select class="pairing-row__select" id="pairSelect_${sys.id}" onchange="updatePairingSelection('${sys.id}', this.value)">
                            <option value="">-- 选择台账记录 --</option>
                            ${group.ledgerRecords.map(led =>
                                `<option value="${led.id}" ${pairingSelections[sys.id] === led.id ? 'selected' : ''}>${led.billingMonth} ${formatMoney(led.amount)}</option>`
                            ).join('')}
                        </select>
                    </div>
                `;
            });

            html += `
                    </div>
                    <div class="pairing-hint">💡 系统按列表顺序推荐配对。可通过下拉菜单修改配对关系，如两条系统记录选择了同一条台账记录将提示冲突。</div>
                </div>
            `;

            body.innerHTML = html;
            document.getElementById('pairingDrawerTitle').textContent = `确认配对 — ${firstSys.name} | ${firstSys.insuranceType} | ${firstSys.billingMonth}`;
        }

        function togglePairingCheck(systemId) {
            const checkbox = document.getElementById('pairCheck_' + systemId);
            if (checkbox.checked) {
                // Restore default selection
                const idx = currentPairingGroup.systemRecords.findIndex(r => r.id === systemId);
                if (currentPairingGroup.ledgerRecords[idx]) {
                    pairingSelections[systemId] = currentPairingGroup.ledgerRecords[idx].id;
                }
            } else {
                delete pairingSelections[systemId];
            }
            // Update select to match
            const select = document.getElementById('pairSelect_' + systemId);
            if (select) select.value = pairingSelections[systemId] || '';
        }

        function updatePairingSelection(systemId, ledgerId) {
            if (ledgerId) {
                pairingSelections[systemId] = ledgerId;
                // Check the checkbox
                const checkbox = document.getElementById('pairCheck_' + systemId);
                if (checkbox) checkbox.checked = true;
            } else {
                delete pairingSelections[systemId];
                const checkbox = document.getElementById('pairCheck_' + systemId);
                if (checkbox) checkbox.checked = false;
            }
        }

        function confirmPairing() {
            // Validate no conflicts (two system records selecting same ledger)
            const selectedLedgerIds = Object.values(pairingSelections);
            const uniqueLedgerIds = new Set(selectedLedgerIds);
            if (uniqueLedgerIds.size < selectedLedgerIds.length) {
                showToast('配对冲突：多条系统记录选择了同一条台账记录', 'error');
                return;
            }

            let confirmed = 0;
            for (const [sysId, ledId] of Object.entries(pairingSelections)) {
                if (confirmPendingPairing(sysId, ledId)) {
                    confirmed++;
                }
            }

            closePairingDrawer();
            renderTable();
            updateStats();
            updateMatchCounts();
            if (confirmed > 0) {
                showToast(`已确认 ${confirmed} 对配对`, 'success');
            }
        }
```

- [x] **Step 2: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 实现确认配对抽屉 — 智能推荐、下拉选择、冲突检测"
```

---

### Task 9: 实现差异详情抽屉 + 开始对账

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [x] **Step 1: Add "开始对账" button handler and detail drawer**

Add before the init section:

```javascript
        // ========== 开始对账 ==========

        function startReconciliation() {
            if (ledgerRecords.length === 0) {
                showToast('请先导入台账数据', 'warning');
                return;
            }

            // Show loading
            document.getElementById('loadingOverlay').classList.add('is-visible');

            // Simulate processing delay for UX
            setTimeout(() => {
                executeMatching();
                document.getElementById('loadingOverlay').classList.remove('is-visible');
                renderTable();
                updateStats();
                updateMatchCounts();

                const { matched, pending, diffs } = matchingResults;
                showToast(`对账完成：已匹配 ${matched.length} 条，待确认 ${pending.length} 条，差异 ${diffs.length} 条`, 'success');
            }, 800);
        }

        // ========== 差异详情抽屉 ==========

        function showNewDetail(recordId, side) {
            let sysRec, ledRec;
            if (side === 'system') {
                sysRec = systemRecords.find(r => r.id === recordId);
                ledRec = sysRec?.matchedLedgerId ? ledgerRecords.find(r => r.id === sysRec.matchedLedgerId) : null;
            } else {
                ledRec = ledgerRecords.find(r => r.id === recordId);
                sysRec = ledRec?.matchedSystemId ? systemRecords.find(r => r.id === ledRec.matchedSystemId) : null;
            }

            const displayRec = sysRec || ledRec;
            if (!displayRec) return;
            currentDetailRecord = displayRec;

            const body = document.getElementById('drawerBody');
            let html = `
                <div class="drawer-section">
                    <div class="drawer-section__title">基本信息</div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">员工</span>
                        <span class="drawer-row__value">${displayRec.name}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">身份证</span>
                        <span class="drawer-row__value">${displayRec.idCard}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">险种</span>
                        <span class="drawer-row__value">${displayRec.insuranceType}</span>
                    </div>
                    <div class="drawer-row">
                        <span class="drawer-row__label">应缴月份</span>
                        <span class="drawer-row__value">${displayRec.billingMonth}</span>
                    </div>
                    ${displayRec.feeType ? `<div class="drawer-row">
                        <span class="drawer-row__label">账单类型</span>
                        <span class="drawer-row__value"><span class="type-badge type-badge--${displayRec.feeType}">${getBillTypeLabel(displayRec.feeType)}</span></span>
                    </div>` : ''}
                    ${displayRec.payableMonth ? `<div class="drawer-row">
                        <span class="drawer-row__label">具体应缴月份</span>
                        <span class="drawer-row__value">${displayRec.payableMonth}</span>
                    </div>` : ''}
                </div>

                <div class="drawer-section">
                    <div class="drawer-section__title">金额对比</div>
            `;

            if (sysRec) {
                html += `
                    <div class="drawer-row">
                        <span class="drawer-row__label">系统金额</span>
                        <span class="drawer-row__value">${formatMoney(sysRec.amount)}
                            <span class="amount-breakdown">（单位: ${formatMoney(sysRec.amountCompany)} / 个人: ${formatMoney(sysRec.amountPersonal)}）</span>
                        </span>
                    </div>
                `;
            }
            if (ledRec) {
                html += `
                    <div class="drawer-row">
                        <span class="drawer-row__label">台账金额</span>
                        <span class="drawer-row__value">${formatMoney(ledRec.amount)}</span>
                    </div>
                `;
            }
            if (!sysRec) {
                html += `<div class="drawer-row"><span class="drawer-row__label">系统侧</span><span class="drawer-row__value" style="color:#DC2626;">无匹配记录</span></div>`;
            }
            if (!ledRec && sysRec?.matchStatus === MATCH_STATUS.DIFF) {
                html += `<div class="drawer-row"><span class="drawer-row__label">台账侧</span><span class="drawer-row__value" style="color:#DC2626;">无匹配记录</span></div>`;
            }

            if (displayRec.diffAmount !== null && displayRec.diffAmount !== 0) {
                const diffLabel = displayRec.diffAmount > 0 ? `+${formatMoney(displayRec.diffAmount)}（系统多）` : `${formatMoney(displayRec.diffAmount)}（台账多）`;
                html += `<div class="drawer-row"><span class="drawer-row__label">差异</span><span class="drawer-row__value" style="color:#DC2626;">${diffLabel}</span></div>`;
            }

            html += `</div>`;

            // Diff analysis
            if (displayRec.matchStatus === MATCH_STATUS.DIFF) {
                html += `
                    <div class="drawer-section">
                        <div class="drawer-section__title">差异分析</div>
                        <div class="diff-analysis">
                            <div class="diff-analysis__content">
                `;
                if (displayRec.diffType === DIFF_TYPE.SYSTEM_MORE) {
                    html += `<strong>系统侧有记录，台账侧无此记录</strong>
                        <div class="diff-analysis__cause">
                            可能原因：
                            <ul><li>台账漏采集：税务系统未采集该笔费用</li><li>误增员：系统多申报了该员工</li><li>申报失败未通知</li></ul>
                        </div>`;
                } else if (displayRec.diffType === DIFF_TYPE.LEDGER_MORE) {
                    html += `<strong>台账侧有记录，系统侧无此记录</strong>
                        <div class="diff-analysis__cause">
                            可能原因：
                            <ul><li>系统漏申报</li><li>台账误增</li><li>跨月申报</li></ul>
                        </div>`;
                } else if (displayRec.diffType === DIFF_TYPE.AMOUNT_MISMATCH) {
                    html += `<strong>系统侧与台账侧金额不一致</strong>
                        <div class="diff-analysis__cause">
                            可能原因：
                            <ul><li>基数上下限调整导致缴费比例变化</li><li>台账金额含/不含小数位舍入差异</li><li>政策调整导致缴费金额变更</li><li>台账录入错误</li></ul>
                        </div>`;
                }
                html += `
                            </div>
                        </div>
                        <div style="margin-top:12px;">
                            <label style="font-size:12px;color:var(--qy-text-muted);">备注</label>
                            <input type="text" class="form-group__input" id="diffRemark" placeholder="输入处理备注" value="${displayRec.remark || ''}" style="margin-top:4px;">
                        </div>
                    </div>
                `;
            }

            body.innerHTML = html;

            // Update drawer footer for diff handling
            const footer = document.querySelector('#detailDrawer .drawer__footer');
            if (displayRec.matchStatus === MATCH_STATUS.DIFF) {
                footer.innerHTML = `
                    <button class="qy-btn qy-btn--secondary" onclick="closeDetailDrawer()">关闭</button>
                    <button class="qy-btn qy-btn--primary" onclick="handleDiffRemark()">标记已处理</button>
                `;
            } else {
                footer.innerHTML = `<button class="qy-btn qy-btn--secondary" onclick="closeDetailDrawer()">关闭</button>`;
            }

            document.getElementById('detailDrawer').classList.add('is-visible');
        }

        function handleDiffRemark() {
            const remark = document.getElementById('diffRemark')?.value || '';
            if (currentDetailRecord) {
                currentDetailRecord.remark = remark || '已处理';
                markDiffHandled(currentDetailRecord.id);
            }
            closeDetailDrawer();
            renderTable();
            updateStats();
            updateMatchCounts();
            showToast('已标记为已处理', 'success');
        }

        function archiveResults() {
            if (!matchingResults.executed) {
                showToast('请先执行对账', 'warning');
                return;
            }

            const pendingCount = systemRecords.filter(r => r.matchStatus === MATCH_STATUS.PENDING).length;
            const diffCount = systemRecords.filter(r => r.matchStatus === MATCH_STATUS.DIFF && !r.remark).length;

            if (pendingCount > 0 || diffCount > 0) {
                showConfirmDialog(
                    '归档确认',
                    `还有 ${pendingCount} 条待确认和 ${diffCount} 条未处理差异，是否继续归档？`,
                    (confirmed) => {
                        if (confirmed) doArchive();
                    }
                );
            } else {
                doArchive();
            }
        }

        function doArchive() {
            systemRecords.forEach(r => {
                if (r.matchStatus === MATCH_STATUS.MATCHED) {
                    r.archived = true;
                    r.archivedAt = new Date().toLocaleString('zh-CN');
                }
            });
            ledgerRecords.forEach(r => {
                if (r.matchStatus === MATCH_STATUS.MATCHED) {
                    r.archived = true;
                    r.archivedAt = new Date().toLocaleString('zh-CN');
                }
            });

            renderTable();
            updateStats();
            updateMatchCounts();
            showToast(`归档完成：共归档 ${systemRecords.filter(r => r.archived).length} 条记录`, 'success');
        }

        // ========== Confirm Dialog ==========

        let confirmCallback = null;

        function showConfirmDialog(title, text, callback) {
            document.getElementById('confirmTitle').textContent = title;
            document.getElementById('confirmText').textContent = text;
            confirmCallback = callback;
            document.getElementById('confirmOverlay').classList.add('is-visible');
        }

        function closeConfirm(result) {
            document.getElementById('confirmOverlay').classList.remove('is-visible');
            if (confirmCallback) confirmCallback(result);
            confirmCallback = null;
        }
```

- [x] **Step 2: Add "开始对账" and "归档结果" buttons to toolbar**

In the toolbar section, update the buttons to include:

```html
                    <div class="toolbar__right">
                        <button class="qy-btn qy-btn--secondary" onclick="openImportDialog()">
                            📥 导入台账
                        </button>
                        <button class="qy-btn qy-btn--primary" onclick="startReconciliation()">
                            ▶ 开始对账
                        </button>
                        <button class="qy-btn qy-btn--secondary" onclick="archiveResults()">
                            ✅ 归档结果
                        </button>
                        <button class="qy-btn qy-btn--secondary">
                            📤 导出
                        </button>
                    </div>
```

- [x] **Step 3: Commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 实现差异详情抽屉、开始对账、归档、确认对话框"
```

---

### Task 10: 完善初始化 + 端到端测试

**Files:**
- Modify: `prototype/qingyang-reconciliation-unified.html`

- [x] **Step 1: Update the init function**

Replace the existing `DOMContentLoaded` handler with:

```javascript
        // ========== Init ==========

        document.addEventListener('DOMContentLoaded', () => {
            updateStats();
            updateMatchCounts();
            renderTable();
        });
```

- [x] **Step 2: Open in browser and test the full flow**

Test the following scenarios:
1. Page loads with system records, empty ledger, stats show totals from system only
2. Click "导入台账" → dialog opens → click "下一步" → mock data loads → click "确认导入"
3. After import, stats update to show system + ledger totals
4. Click "开始对账" → loading shows → results display:
   - Unique amount matches → green "已匹配" rows
   - Same amount multiple records → yellow "待确认" rows
   - No match → red "差异" rows
5. Click "确认配对" on a pending row → drawer opens with recommended pairings
6. Modify a pairing via dropdown → click "确认全部配对"
7. Click "详情" on a diff row → drawer shows analysis
8. Click "标记已处理" → diff marked
9. Click "归档结果" → confirmation if pending/diff remain
10. Click "取消" on a matched row → returns to unmatched

- [x] **Step 3: Final commit**

```bash
git add prototype/qingyang-reconciliation-unified.html
git commit -m "feat: 完善初始化 + 端到端测试通过"
```

---

## Self-Review

### Spec Coverage Check

| Spec Section | Covered By Task |
|--------------|-----------------|
| 数据模型（系统侧+台账侧） | Task 1 |
| 匹配状态机 | Task 1, Task 3 |
| 导入模板格式/险种映射 | Task 6 |
| 匹配算法（分组/精确匹配/差异检测） | Task 3 |
| 页面布局/统计卡片/筛选条 | Task 5, Task 7 |
| 数据表格/行颜色 | Task 7 |
| 待确认抽屉（智能推荐+批量映射） | Task 8 |
| 差异详情抽屉 | Task 9 |
| 导入对话框（两步骤） | Task 6 |
| 导入流程（5步） | Task 6, Task 9 |
| 批量操作 | Task 7 (checkboxes), Task 9 (archive) |
| 边界情况/错误处理 | Task 6 (validation), Task 9 (confirm dialog) |

### Placeholder Scan
No TBD/TODO/placeholder patterns found. All code is complete in each step.

### Type Consistency
- `MATCH_STATUS` enum used consistently across all tasks
- `DIFF_TYPE` enum used consistently
- `systemRecords` / `ledgerRecords` arrays used consistently
- Function names match between definition and call sites
- `confirmPendingPairing` defined in Task 3, called in Task 8
- `markDiffHandled` defined in Task 3, called in Task 9
