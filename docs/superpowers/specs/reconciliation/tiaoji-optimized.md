# 社保对账复核 - 调基补差对账优化设计

> 状态说明：
> 这份文档是对账复核模块中“调基补差”场景的专项深化设计，用于补充复杂业务场景下的匹配与展示规则。
> 当前对账复核模块的完整主规格仍以 `type-month-matching.md` 为准；若本文件与主规格存在冲突，应优先采用 `type-month-matching.md`，并将本文件视为待吸收或待同步的专题补充文档。

## 1. 概述

### 1.1 文档目的

本文档针对社保对账系统中「调基补差」账单类型的匹配逻辑进行优化设计，解决原设计中存在的业务逻辑不完善问题。

### 1.2 问题背景

**业务场景差异**：
- **系统行为**：逐月生成调基补差，知道「补差月份」，不知道「实缴月份」
- **台账行为**：一次性导入多个月份的调基补差，知道「实缴月份」

**核心矛盾**：台账一次性导入多个月份的调基补差，但系统是逐月生成的。当台账中多个月份的调基补差导入后，如何与系统的单月记录正确匹配？

### 1.3 调基补差的四种业务场景

| 场景 | 说明 | 业务示例 |
|------|------|---------|
| 同月调基 | 同一员工在同一月份发生单次基数调整 | 员工A 2026-01 月薪从 10000 调整为 12000 |
| 跨月调基 | 调基生效月份与申报月份不同 | 2026-02 申报 2026-01 的社保，基数调整追溯到 2026-01 |
| 多次调基 | 同一员工在同一月份发生多次基数调整 | 员工A 2026-01 先调整为 11000，再调整为 12000 |
| 历史补调 | 对历史月份的基数进行补充调整 | 2026-04 发现 2026-01 的基数少报，补调差额 |

---

## 2. 匹配逻辑优化

### 2.1 原设计的问题

**原匹配 Key**：
```
身份证 + 险种 + 调基事件ID + 补差月份
```

**问题**：
1. `调基事件ID` 是系统生成的，但台账不知道这个 ID
2. 当台账一次性导入多个月份时，无法与系统的单月记录一一对应
3. 多次调基产生的多条记录可能被错误地合并或拆分

### 2.2 优化后的匹配 Key

**新匹配 Key**：
```
身份证 + 险种 + 调基生效月份 + 补差月份
```

**为什么这样设计**：
- `调基生效月份` 是调基政策执行的时间点，系统和台账都知道
- `补差月份` 是产生补差的月份，系统知道，台账也知道
- 不依赖系统生成的 `调基事件ID`，台账可以独立匹配

### 2.3 月份对齐 + 金额比对策略

**原设计**：直接求和比对
```
同一 Key 下所有系统记录金额求和 vs 同一 Key 下所有台账记录金额求和
```

**问题**：如果系统是逐月生成，而台账是一次性导入多个月份，直接求和可能导致月份错配。

**优化方案**：采用「月份对齐 + 金额比对」双重校验

```
Step 1: 按「身份证 + 险种 + 调基生效月份」分组
Step 2: 在每组内，按「补差月份」对齐系统记录和台账记录
Step 3: 如果某补差月份在台账中存在多条记录（多次调基），求和后再比对
Step 4: 如果某补差月份在系统中存在多条记录，求和后再比对
```

### 2.4 合并且匹配算法

```typescript
interface MatchGroup {
  matchKey: string;           // 身份证+险种+调基生效月份
  sysRecords: TiaojiRecord[]; // 系统记录列表
  ledgerRecords: TiaojiRecord[]; // 台账记录列表
}

interface MatchResult {
  matchKey: string;
  billingMonth: string;        // 补差月份
  sysTotal: number;           // 系统金额合计
  ledgerTotal: number;        // 台账金额合计
  sysRecordIds: string[];     // 匹配的系统记录ID
  ledgerRecordIds: string[];   // 匹配的台账记录ID
  matchStatus: 'MATCHED' | 'SYSTEM_MORE' | 'LEDGER_MORE';
  matchType: 'EXACT' | 'MERGED';  // 精确匹配还是合并匹配
}

function matchTiaojiRecords(groups: MatchGroup[]): MatchResult[] {
  const results: MatchResult[] = [];

  for (const group of groups) {
    // 按补差月份进一步分组
    const byBillingMonth = groupBy(group, 'billingMonth');

    for (const [billingMonth, sysRecs] of Object.entries(byBillingMonth.sysRecords)) {
      const ledgerRecs = byBillingMonth.ledgerRecords[billingMonth] || [];

      if (ledgerRecs.length === 0) {
        // 系统有，台账无
        results.push({
          matchKey: group.matchKey,
          billingMonth,
          sysTotal: sum(sysRecs, 'total'),
          ledgerTotal: 0,
          sysRecordIds: sysRecs.map(r => r.id),
          ledgerRecordIds: [],
          matchStatus: 'SYSTEM_MORE',
          matchType: 'EXACT'
        });
      } else if (sysRecs.length === 0) {
        // 系统无，台账有
        results.push({
          matchKey: group.matchKey,
          billingMonth,
          sysTotal: 0,
          ledgerTotal: sum(ledgerRecs, 'total'),
          sysRecordIds: [],
          ledgerRecordIds: ledgerRecs.map(r => r.id),
          matchStatus: 'LEDGER_MORE',
          matchType: 'EXACT'
        });
      } else {
        // 双方都有，合并后比对
        const sysTotal = sum(sysRecs, 'total');
        const ledgerTotal = sum(ledgerRecs, 'total');

        results.push({
          matchKey: group.matchKey,
          billingMonth,
          sysTotal,
          ledgerTotal,
          sysRecordIds: sysRecs.map(r => r.id),
          ledgerRecordIds: ledgerRecs.map(r => r.id),
          matchStatus: sysTotal === ledgerTotal ? 'MATCHED' : 'SYSTEM_MORE',
          matchType: sysRecs.length > 1 || ledgerRecs.length > 1 ? 'MERGED' : 'EXACT'
        });
      }
    }
  }

  return results;
}
```

---

## 3. 实缴月份确认机制

### 3.1 原设计的问题

**原设计**：确认时系统自动将台账的 `paidMonth` 写入记录。

**问题**：没有考虑调基补差的「滞后性」——当月调基可能次月才申报实缴。

### 3.2 优化后的实缴月份确认逻辑

```typescript
function determinePaidMonth(record: TiaojiRecord, ledgerRecord?: LedgerRecord): string {
  // 优先级1：台账提供的实缴月份
  if (ledgerRecord?.paidMonth) {
    return ledgerRecord.paidMonth;
  }

  // 优先级2：系统记录的实缴日期字段
  if (record.actualPaidMonth) {
    return record.actualPaidMonth;
  }

  // 优先级3：申报月份 + 1（次月申报惯例）
  // 假设社保为次月申报
  const declareMonth = parseMonth(record.billingMonth);
  return addMonths(declareMonth, 1).toString(); // 格式：YYYY-MM
}

function verifyRecord(record: TiaojiRecord): VerifyResult {
  const canVerify =
    record.matchStatus === 'MATCHED' &&           // 金额一致
    record.verifyStatus === 'PENDING' &&          // 未确认
    record.paidMonth !== null &&                  // 有实缴月份
    record.paidMonth !== undefined;

  return {
    canVerify,
    record: canVerify ? { ...record, verifyStatus: 'VERIFIED' } : record
  };
}
```

### 3.3 实缴月份显示规则

| 场景 | 显示内容 |
|------|---------|
| 已确认 | 实缴月份（如 2026-02） |
| 未确认 | "—" |
| 台账有但未匹配 | "待确认" |

---

## 4. 同月多笔调基的处理

### 4.1 业务场景

**场景**：员工A在2026-01月发生两次调基：
- 01-15：基数从 10000 → 11000（补差 ¥50）
- 01-28：基数从 11000 → 12000（补差 ¥80）

**台账表现**：
- 方式A：合并为一条 ¥130 的记录
- 方式B：分成两条 ¥50 和 ¥80 的记录

### 4.2 匹配模式

**模式一：合并比对（默认）**
```typescript
// 同一补差月份的所有记录合并后比对
function matchByMerge(sysRecords: TiaojiRecord[], ledgerRecords: TiaojiRecord[]) {
  const sysTotal = sum(sysRecords, 'total');
  const ledgerTotal = sum(ledgerRecords, 'total');

  return {
    matchStatus: sysTotal === ledgerTotal ? 'MATCHED' : 'SYSTEM_MORE',
    sysTotal,
    ledgerTotal,
    matchType: 'MERGED'
  };
}
```

**模式二：逐笔比对**
```typescript
// 尝试一一配对，无法配对的按合并处理
function matchByOneByOne(sysRecords: TiaojiRecord[], ledgerRecords: TiaojiRecord[]) {
  const results: MatchResult[] = [];
  const paired: [TiaojiRecord, LedgerRecord][] = [];
  const unpairedSys: TiaojiRecord[] = [];
  const unpairedLedger: LedgerRecord[] = [];

  // 优先配对金额完全一致的记录
  for (const sys of sysRecords) {
    const match = ledgerRecords.find(l => l.total === sys.total && !l.paired);
    if (match) {
      paired.push([sys, match]);
      match.paired = true;
    } else {
      unpairedSys.push(sys);
    }
  }

  // 剩余未配对的记录
  const unpairedLedgerRecs = ledgerRecords.filter(l => !l.paired);

  // 配对成功的记录
  for (const [sys, ledger] of paired) {
    results.push({
      matchStatus: 'MATCHED',
      sysRecordIds: [sys.id],
      ledgerRecordIds: [ledger.id],
      matchType: 'EXACT'
    });
  }

  // 未配对的系统记录
  for (const sys of unpairedSys) {
    results.push({
      matchStatus: 'SYSTEM_MORE',
      sysRecordIds: [sys.id],
      ledgerRecordIds: [],
      matchType: 'EXACT'
    });
  }

  // 未配对的台账记录
  for (const ledger of unpairedLedgerRecs) {
    results.push({
      matchStatus: 'LEDGER_MORE',
      sysRecordIds: [],
      ledgerRecordIds: [ledger.id],
      matchType: 'EXACT'
    });
  }

  return results;
}
```

### 4.3 匹配模式选择

```
┌─────────────────────────────────────────────────────┐
│                   匹配模式选择                        │
├─────────────────────────────────────────────────────┤
│  台账记录数 = 1 && 系统记录数 = 1  → 逐笔比对(精确)     │
│  台账记录数 = 1 && 系统记录数 > 1  → 合并比对          │
│  台账记录数 > 1 && 系统记录数 = 1  → 合并比对          │
│  台账记录数 > 1 && 系统记录数 > 1  → 合并比对(默认)    │
└─────────────────────────────────────────────────────┘
```

---

## 5. 历史调基补差的处理

### 5.1 业务场景

**场景**：2026-04 进行调基补差申报，但追溯的是 2026-01、2026-02、2026-03 三个月的差额。

**问题**：
- 系统逐月生成补差记录（1月、2月、3月各一条）
- 台账一次性导入三个月
- 台账的 paidMonth 是哪个？（申报月份 vs 各自实缴月份）

### 5.2 数据模型扩展

```typescript
interface TiaojiRecord {
  // 基础信息
  id: string;
  employeeId: string;
  employeeName: string;
  idCard: string;
  customer: string;
  insuranceType: string;

  // 调基信息
  adjustmentId: string;        // 调基事件ID
  adjustmentMonth: string;    // 调基生效月份
  adjustmentDetail: {
    beforeBase: number;        // 调基前基数
    afterBase: number;         // 调基后基数
  };

  // 补差信息
  billingMonth: string;        // 补差月份（产生补差的月份）
  paidMonth: string;           // 实缴月份（台账提供）

  // 追溯信息（新增强化）
  retrospectiveMonths: string[];  // 追溯的月份范围（如 [2026-01, 2026-02, 2026-03]）
  isRetrospective: boolean;       // 是否为历史追溯调基

  // 金额
  sysCompany: number;
  sysPersonal: number;
  sysTotal: number;
  ledgerCompany: number;
  ledgerPersonal: number;
  ledgerTotal: number;

  // 合并信息
  sysMultiple: number;         // 系统合并笔数
  ledgerMultiple: number;      // 台账合并笔数

  // 匹配信息（新增加）
  matchDetail: {
    sysRecordIds: string[];
    ledgerRecordIds: string[];
    matchType: 'EXACT' | 'MERGED';
  };

  // 核对状态
  status: 'PENDING' | 'VERIFIED' | 'UNDO';
  verifiedAt?: string;
  verifiedBy?: string;

  // 匹配状态
  matchStatus: 'MATCHED' | 'SYSTEM_MORE' | 'LEDGER_MORE';
}
```

### 5.3 历史调基的匹配逻辑

```typescript
function matchRetrospectiveTiaoji(
  sysRecords: TiaojiRecord[],    // 系统记录（按月分开）
  ledgerRecords: LedgerRecord[]  // 台账记录（一次性导入）
): MatchResult[] {
  const results: MatchResult[] = [];

  // Step 1: 识别追溯月份范围
  const allBillingMonths = new Set([
    ...sysRecords.map(r => r.billingMonth),
    ...ledgerRecords.map(r => r.billingMonth)
  ]);

  // Step 2: 按追溯月份分组匹配
  for (const month of allBillingMonths) {
    const sysForMonth = sysRecords.filter(r => r.billingMonth === month);
    const ledgerForMonth = ledgerRecords.filter(r => r.billingMonth === month);

    // 同一月份内采用合并比对
    const sysTotal = sum(sysForMonth, 'total');
    const ledgerTotal = sum(ledgerForMonth, 'total');

    results.push({
      matchKey: buildMatchKey(sysForMonth[0]),
      billingMonth: month,
      sysTotal,
      ledgerTotal,
      sysRecordIds: sysForMonth.map(r => r.id),
      ledgerRecordIds: ledgerForMonth.map(r => r.id),
      matchStatus: sysTotal === ledgerTotal ? 'MATCHED' :
                   sysTotal > ledgerTotal ? 'SYSTEM_MORE' : 'LEDGER_MORE',
      matchType: sysForMonth.length > 1 || ledgerForMonth.length > 1 ? 'MERGED' : 'EXACT'
    });
  }

  return results;
}
```

---

## 6. 状态机设计

### 6.1 三态设计

```
                    ┌─────────────────┐
                    │    PENDING      │
                    │   （待核对）     │
                    └────────┬────────┘
                             │
                   金额一致 + 有实缴月份
                             │
                             ▼
                    ┌─────────────────┐
                    │    VERIFIED     │
                    │ （已核对完成）   │
                    └────────┬────────┘
                             │
                   取消确认或修改金额
                             │
                             ▼
                    ┌─────────────────┐
                    │      UNDO       │
                    │ （已撤销）      │
                    └────────┬────────┘
                             │
                          重新核对
                             │
                             ▼
                    ┌─────────────────┐
                    │    PENDING      │
                    └─────────────────┘
```

### 6.2 状态转换规则

| 当前状态 | 操作 | 目标状态 | 条件 |
|---------|------|---------|------|
| PENDING | 确认 | VERIFIED | 金额一致 + 有实缴月份 |
| VERIFIED | 取消确认 | UNDO | — |
| UNDO | 重新核对 | PENDING | — |

### 6.3 批量确认逻辑

```typescript
function batchVerify(records: TiaojiRecord[]): BatchVerifyResult {
  const toVerify: TiaojiRecord[] = [];
  const skipped: SkippedRecord[] = [];

  for (const record of records) {
    if (record.matchStatus === 'MATCHED' &&
        record.verifyStatus === 'PENDING' &&
        record.paidMonth) {
      toVerify.push({ ...record, verifyStatus: 'VERIFIED' });
    } else {
      skipped.push({
        record,
        reason: !record.paidMonth ? '缺少实缴月份' :
                record.matchStatus !== 'MATCHED' ? '金额不一致' :
                '已确认'
      });
    }
  }

  return { toVerify, skipped };
}
```

---

## 7. 界面设计

### 7.1 调基补差列表布局

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  [← 返回仪表盘]    调基补差对账                                      [导出]    │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─ 筛选 ─────────────────────────────────────────────────────────────────┐   │
│  │ [月份 ▼] [结算主体 ▼] [调基事件 ▼] [核对状态 ▼] [姓名/证件号      ] [搜索] │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─ 数据列表 ─────────────────────────────────────────────────────────────┐   │
│  │ ☐ 姓名           │ 身份证  │ 客户 │ 险种 │ 调基事件       │ 补差月份 │ 实缴月份 │ 系统金额 │ 台账金额 │ 状态      │ 操作   │   │
│  │  ─────────────────────────────────────────────────────────────────────────────────────────────   │
│  │ ☐ 赵六 [已匹配]  │ 4301** │ A公司│ 养老 │ 2026-01调基    │ 2026-01  │ 2026-02  │ ¥334     │ ¥334     │ [✓已核对] │ [详情] │   │
│  │ ☐ 赵六           │ 4301** │ A公司│ 医疗 │ 2026-01调基    │ 2026-01  │ 2026-02  │ ¥89      │ ¥89      │ [✓已核对] │ [详情] │   │
│  │ ☐ 郑十一 [已匹配]│ 4301** │ B公司│ 养老 │ 2026-03调基    │ 2026-03  │ 2026-04  │ ¥156     │ ¥156     │ [待核对]  │ [详情] │   │
│  │  ...                                                                              │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─ 批量操作 ─────────────────────────────────────────────────────────────┐   │
│  │ [全选] [确认所选(3)] [取消确认]                          共 6 条 / 1页  │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 7.2 调基事件列显示格式

```
┌─────────────────────────────────────────────┐
│ 调基事件                                    │
├─────────────────────────────────────────────┤
│ 2026-01 基数调整                            │
│ ¥10000 → ¥12000                             │
│ 追溯: 2026-01~2026-03                       │
└─────────────────────────────────────────────┘
```

### 7.3 状态标签样式

| 状态 | 样式 |
|------|------|
| 待核对 | `qy-tag qy-tag--warning` 黄色 |
| 已核对 | `qy-tag qy-tag--success` 绿色 |
| 已撤销 | `qy-tag qy-tag--default` 灰色 |

### 7.4 "已匹配"标签样式

**样式**：简单边框，绿色文字，不喧宾夺主

```css
.match-tag {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  padding: 1px 4px;
  border-radius: 2px;
  font-size: 10px;
  font-weight: 500;
  color: var(--qy-success-600);
  vertical-align: middle;
  margin-left: 4px;
  border: 1px solid var(--qy-success-200);
  background: transparent;
}
```

---

## 8. 与原设计的差异对比

| 项目 | 原设计 | 新设计 |
|-----|-------|-------|
| 匹配 Key | 身份证+险种+调基事件ID+补差月份 | 身份证+险种+调基生效月份+补差月份 |
| 合并且匹配 | 直接求和比对 | 月份对齐后再求和比对 |
| 实缴月份 | 台账paidMonth | 台账paidMonth + 申报月份+1 兜底 |
| 批量确认条件 | 金额一致 | 金额一致 + 有实缴月份 + 未确认 |
| 状态机 | PENDING/VERIFIED 两态 | PENDING/VERIFIED/UNDO 三态 |
| UI | 无调基事件列 | 增加调基事件列，显示调基详情和追溯月份 |
| 数据模型 | 基础字段 | 增加调基详情、追溯信息、匹配详情 |
| 多次调基 | 无区分 | EXACT/MERGED 两种匹配类型 |

---

## 9. 非功能性要求

| 要求 | 说明 |
|-----|------|
| 性能 | 单次导入控制在5分钟内，差异比对在3秒内响应 |
| 容量 | 单月单结算主体最大支持10万条记录 |
| 数据保留 | 台账数据保留24个月 |
| 权限 | 仅管理员和HR运营角色可访问 |
| 审计 | 所有核对操作记录操作人和时间戳 |

---

*文档版本：v4.0*
*创建日期：2026-04-09*
*最后更新：2026-04-09*
*状态：新增文档*
