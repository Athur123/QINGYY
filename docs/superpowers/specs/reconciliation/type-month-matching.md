# 社保对账复核：类型/月份互推匹配设计

## Context

青阳云系统根据员工参保异动自动生成应缴费用，包含汇缴、补缴、调基补差三种类型。系统知道费用类型，但补缴和补差不知道应缴月份。税务台账（Excel导入）知道应缴月份，但不知道费用类型。

核心矛盾：系统有类型无月份，台账有月份无类型。双方共同拥有：身份证、险种、金额。

同一应缴月份内，一个员工同一险种可能产生多笔费用：1笔汇缴 + N笔补缴 + M笔调基补差。台账中同样有多笔，但无法区分类型。金额特征（零头、特殊值）无法作为类型判断依据。

## 约束确认

| 项目 | 确认值 |
|------|--------|
| 匹配范围 | 身份证 + 险种 + 应缴月份 |
| 匹配方式 | 精确金额匹配（一分不差） |
| 触发方式 | 台账导入后，用户手动点击"开始对账"（无需台账也可执行，全部标记差异/未匹配） |
| 匹配成功后 | 系统回填应缴月份，台账回填费用类型 |
| 同金额多笔 | 标记"待确认"，人工判断 |
| 待确认交互 | 智能推荐 + 批量映射 + 确认 |
| 对账输出 | 匹配成功归档 + 差异处理流程 |
| 判重规则 | 参保主体 + 参保规则 + 应缴月份 维度只保留一份台账 |
| 差异类型 | 系统多（台账无）、台账多（系统无）、金额不一致（双方都有但金额不同） |

## 系统侧账单明细生成逻辑

系统侧账单明细来源于员工参保异动记录，按费用类型分为三类，各有不同的取数规则。

### 汇缴

异动类型为增员的明细产生的费用均为正常参保费用（自动拆分的补缴除外）。其应缴月份默认为异动生效月份，且等于费款所属期。系统自动获取所选对账复核月份与增员异动应缴月份一致的成员明细。

### 补缴

来源有两种：
1. **增员时自动拆分的补缴**：增员时自动拆分的补缴月份产生的补缴费用，其应缴月份默认为空。当所选对账复核月份与该类补缴明细的费款所属期一致时，列表自动获取这些成员补缴明细。
2. **单补缴异动**：补缴月份产生的补缴费用，其应缴月份默认为空。系统自动获取所有异动类型为补缴且应缴月份为空的补缴成员明细，不区分所选月份。

补缴明细按成员 + 险种 + 补缴月份（即费款所属期）逐条展示。补缴明细的费款所属期为补缴月份，与应缴月份不一定相等。

### 调基补差

来源有两种：
1. **调基**：调基生效月份产生的调基补差费用，其应缴月份默认为空。在任意月份的系统侧账单明细中，应自动获取所有异动类型为调基且应缴月份为空的调基成员费用明细。
2. **政策调整**：自调整生效月份产生的调基补差费用，其应缴月份默认为空。在任意月份的系统侧账单明细中，需要自动获取所有异动类型为政策调整且应缴月份为空的政策调整成员费用明细。

调基补差明细按成员 + 险种 + 费款所属期逐条展示，每一笔明细都需要核对。同一成员、险种、补差月份的费用分别展示多条明细。

### 关键字段关系

| 字段 | 汇缴 | 补缴 | 调基补差 |
|------|------|------|---------|
| 应缴月份 (payableMonth) | = 费款所属期，不为空 | 默认为空，核对后从台账回填 | 默认为空，核对后从台账回填 |
| 费款所属期 (feePeriod) | = 异动生效月份 = 应缴月份 | = 补缴月份，≠ 应缴月份 | = 调基补差月份，≠ 应缴月份 |
| 数据筛选规则 | 所选月份 = 应缴月份 | 费款所属期 = 所选月份 或 应缴月份为空 | 应缴月份为空（全量获取） |

## 数据模型

### 系统侧费用记录

系统侧费用记录来自参保异动记录，字段说明：

```
{
  // 基础字段
  "id": "S001",
  "employee_name": "张三",
  "id_card": "430105199001011234",
  "insurance_type": "养老",               // 险种：养老/医疗/失业/工伤/生育/大额医疗/公积金
  "fee_type": "补缴",                     // 费用类型：huijiao（汇缴）/ bujiao（补缴）/ tiaoji（调基补差）
  "amount_company": 423.50,               // 单位金额
  "amount_personal": 211.75,              // 个人金额
  "amount": 635.25,                       // 合计金额 = amount_company + amount_personal

  // 月份字段
  "billing_month": "2026-04",             // 对账复核所选账单月份
  "payable_month": null,                  // 具体应缴月份。汇缴默认=费款所属期；补缴/调基补差默认为空，对账匹配后从台账回填
  "fee_period": "2025-12",               // 费款所属期。汇缴=应缴月份；补缴=补缴月份；调基补差=补差月份

  // 匹配字段
  "match_status": "UNMATCHED",            // UNMATCHED / MATCHED / PENDING / DIFF / PAID
  "matched_ledger_id": null,              // 关联的台账记录ID
  "diff_type": null,                      // DIFF类型：system_more / ledger_more / amount_mismatch
  "diff_amount": null,                    // 差异金额（正=系统多，负=台账多）

  // 归档字段
  "archived": false,
  "archived_at": null,
  "archive_batch_id": null,               // 归属归档批次ID

  // 其他
  "remark": null,                         // 备注
  "force_matched": false,                 // 是否强制核对
}
```

### 台账侧记录

台账侧记录来自导入的 Excel，存储为临时对账表：

```
{
  // 导入字段
  "id": "T003",
  "employee_name": "张三",
  "id_card": "430105199001011234",
  "insurance_type": "养老",               // 导入时通过别名映射标准化
  "billing_month": "2026-04",
  "fee_period": "2025-12",
  "amount": 635.25,

  // 匹配回填字段
  "fee_type_inferred": null,              // 推断的费用类型，匹配后从系统侧回填
  "payable_month_inferred": null,         // 推断的应缴月份
  "match_status": "UNMATCHED",            // UNMATCHED / MATCHED / PENDING / DIFF / PAID
  "matched_system_id": null,              // 关联的系统记录ID
  "diff_type": null,
  "diff_amount": null,

  // 导入元数据
  "import_batch_id": null,
  "insurance_subject": "",                // 参保主体
  "insurance_rule": "",                   // 参保规则
  "imported_at": null,
  "imported_by": null,

  // 归档字段
  "archived": false,
  "archived_at": null,
  "archive_batch_id": null,
}
```

### 核对状态机

`matchStatus` 的五种状态流转：

```
                    ┌──────────┐
                    │ UNMATCHED │  ← 初始状态（导入后）
                    └─────┬────┘
                          │ 执行对账
              ┌───────────┼───────────┐
              │           │           │
        ┌─────┴────┐ ┌────┴─────┐ ┌──┴──────┐
        │  MATCHED  │ │ PENDING  │ │  DIFF   │
        │ (唯一配对) │ │ (待确认)  │ │ (差异)  │
        └─────┬────┘ └────┬─────┘ └────┬─────┘
              │           │           │
              │     确认核对│     强制核对│
              │           │           │
              │    ┌──────┴─────┐     │
              │    │  MATCHED   │ ←───┘
              │    └──────┬─────┘
              │           │
              └── 取消核对 ─┘（仅未归档的 MATCHED）
              │
              ▼ 归档（archived=true，创建归档批次）
        ┌──────────┐
        │ MATCHED   │  ← archived=true, archiveBatchId
        │ (已归档)   │
        └─────┬────┘
              │ 付款申请 → 从已归档批次获取付款明细 → 完成付款
              ▼
        ┌──────────┐
        │   PAID    │  ← 已付款（matchStatus = PAID）
        │ (已付款)   │     archived=true, archiveBatchId 保留
        └──────────┘
```

**`archived` 独立标记**：`archived` 不是 `matchStatus` 的值，而是记录上的独立布尔字段。已归档记录的 `matchStatus` 仍为 `MATCHED`，`archived=true` + `archiveBatchId` 指向归属批次。同一账单月份可多次归档，每次生成新批次。

**已付款状态**：付款申请从已归档批次中获取明细，完成付款后 `matchStatus` 从 `MATCHED` 变更为 `PAID`。`archived=true` 和 `archiveBatchId` 保留用于追溯。

**已归档记录规则**：
- 操作列显示「详情」而非「取消」
- `doCancelMatch()` 拦截已归档记录，toast "已归档记录不可取消核对"
- 表格行灰色背景（`row-archived`），状态列显示「已归档」

**已付款记录规则**：
- 操作列显示「详情」，不可取消核对、不可取消归档
- 表格行背景色区别于已归档，状态列显示「已付款」

状态说明：
- `UNMATCHED`: 未参与匹配（初始状态）
- `MATCHED`: 匹配成功（自动配对、人工确认或强制核对后），可通过 `archived` 标记是否已归档
- `PENDING`: 待确认（同金额多笔，或取消核对后恢复）
- `DIFF`: 差异（金额无匹配或金额不一致），可通过强制核对直接转为 MATCHED
- `PAID`: 已付款（从已归档批次发起付款申请并完成付款后），保留 `archived=true` 和 `archiveBatchId`

### 导入模板格式

Excel 必填列：

| 列名 | 类型 | 说明 | 示例 |
|------|------|------|------|
| 姓名 | 文本 | 员工姓名 | 张三 |
| 身份证 | 文本 | 18位身份证号 | 430105199001011234 |
| 险种 | 文本 | 险种名称（支持别名） | 养老 / 基本养老保险 |
| 应缴月份 | 日期/文本 | YYYY-MM 格式 | 2026-04 |
| 金额 | 数值 | 精确到分，保留2位小数 | 635.25 |

可选列：单位金额 / 个人金额 / 备注

### 险种名称映射表

```javascript
const INSURANCE_TYPE_ALIAS = {
  '养老': ['养老', '基本养老保险', '养老保险', '基本养老'],
  '医疗': ['医疗', '基本医疗保险', '医疗保险', '基本医疗'],
  '失业': ['失业', '失业保险', '失业保险金'],
  '工伤': ['工伤', '工伤保险', '工伤保险金'],
  '生育': ['生育', '生育保险', '生育保险金'],
  '大额医疗': ['大额医疗', '大额医疗保险', '大病医疗'],
  '公积金': ['公积金', '住房公积金', '住房公积'],
};
```

导入时标准化规则：
1. 身份证：去空格、X大写、trim
2. 险种：通过映射表转为标准名称，无法识别的标记为"未知"
3. 应缴月份：统一转为 YYYY-MM 格式（如 202604 → 2026-04）
4. 金额：保留2位小数，四舍五入到分

---

## 匹配算法

### Step 1: 数据准备

```javascript
function prepareMatchingData(systemRecords, ledgerRecords) {
  systemRecords.forEach(r => {
    r.idCard = normalizeIdCard(r.idCard);
    r.insuranceType = normalizeInsuranceType(r.insuranceType);
  });
  ledgerRecords.forEach(r => {
    r.idCard = normalizeIdCard(r.idCard);
    r.insuranceType = normalizeInsuranceType(r.insuranceType);
    r.amount = roundToCents(r.amount);
  });
  // 分组 key = idCard + '|' + insuranceType + '|' + billingMonth
  const systemGroups = groupByKey(systemRecords, makeGroupKey);
  const ledgerGroups = groupByKey(ledgerRecords, makeGroupKey);
  const allKeys = new Set([...systemGroups.keys(), ...ledgerGroups.keys()]);
  return { allKeys, systemGroups, ledgerGroups };
}
```

### Step 2: 精确金额匹配

```javascript
function executeMatching(allKeys, systemGroups, ledgerGroups) {
  const results = { matched: [], pending: [], diffs: [] };

  for (const key of allKeys) {
    const sysRecords = systemGroups.get(key) ?? [];
    const ledRecords = ledgerGroups.get(key) ?? [];
    const sysAmountMap = countByAmount(sysRecords);
    const ledAmountMap = countByAmount(ledRecords);
    const allAmounts = new Set([...sysAmountMap.keys(), ...ledAmountMap.keys()]);

    for (const amount of allAmounts) {
      const sysForAmount = sysAmountMap.get(amount) ?? [];
      const ledForAmount = ledAmountMap.get(amount) ?? [];

      if (sysForAmount.length > 0 && ledForAmount.length === 0) {
        // 系统有，台账无
        // 汇缴 → DIFF(system_more)：汇缴应在当前月份有对应台账
        // 补缴/调基补差 → UNMATCHED：可能对应其他月份，可在后续匹配
        sysForAmount.forEach(r => {
          if (r.feeType === 'bujiao' || r.feeType === 'tiaoji') {
            r.matchStatus = 'UNMATCHED';
          } else {
            r.matchStatus = 'DIFF'; r.diffType = 'system_more'; r.diffAmount = r.amount;
            results.diffs.push({ systemRecord: r, ledgerRecords: [] });
          }
        });
      } else if (sysForAmount.length === 0 && ledForAmount.length > 0) {
        // 台账有，系统无 → DIFF(ledger_more)
        ledForAmount.forEach(r => {
          r.matchStatus = 'DIFF'; r.diffType = 'ledger_more'; r.diffAmount = -r.amount;
          results.diffs.push({ systemRecords: [], ledgerRecord: r });
        });
      } else if (sysForAmount.length === 1 && ledForAmount.length === 1) {
        // 唯一配对 → 自动 MATCHED，回填应缴月份和费用类型
        const sysRec = sysForAmount[0], ledRec = ledForAmount[0];
        sysRec.matchStatus = 'MATCHED'; sysRec.matchedLedgerId = ledRec.id;
        ledRec.matchStatus = 'MATCHED'; ledRec.matchedSystemId = sysRec.id;
        sysRec.payableMonth = ledRec.billingMonth;
        ledRec.feeTypeInferred = sysRec.feeType;
        results.matched.push({ systemRecord: sysRec, ledgerRecord: ledRec });
      } else {
        // 多笔同金额 → PENDING
        results.pending.push({ amount, systemRecords: sysForAmount, ledgerRecords: ledForAmount });
        sysForAmount.forEach(r => r.matchStatus = 'PENDING');
        ledForAmount.forEach(r => r.matchStatus = 'PENDING');
      }
    }
  }
  return results;
}
```

### Step 3: 金额不一致差异检测

Step 2 处理了"金额相同"的情况。对于同一分组内系统侧和台账侧金额完全不重合的情况，双方标记为"差异（金额不一致）"：系统侧记录匹配最接近的台账金额计算差额。

### 匹配结果统计

```javascript
function calculateStats(allSystemRecords, allLedgerRecords, results) {
  return {
    totalRecords: allSystemRecords.length + allLedgerRecords.length,
    matchedCount: results.matched.length,
    pendingCount: results.pending.length,
    diffCount: results.diffs.length,
    systemMoreCount: results.diffs.filter(d => d.diffType === 'system_more').length,
    ledgerMoreCount: results.diffs.filter(d => d.diffType === 'ledger_more').length,
    amountMismatchCount: results.diffs.filter(d => d.diffType === 'amount_mismatch').length,
    matchedAmount: results.matched.reduce((sum, r) => sum + r.systemRecord.amount, 0),
    diffAmount: results.diffs.reduce((sum, d) => sum + Math.abs(d.systemRecord?.amount ?? 0), 0),
  };
}
```

---

## 明细核对页 — UI 与交互设计

明细核对页是逐笔核对操作的核心页面，所有交互围绕"快速定位 + 高效核对 + 批量处理"展开。

### 页面整体布局

```
┌───────────────────────────────────────────────────────────────────────┐
│  ← 对账复核 / 社保规则A         社保对账复核 — 2026-04                  │
├───────────────────────────────────────────────────────────────────────┤
│  [📥 导入台账] [▶ 开始对账] [✅ 归档结果] [📦 归档记录] [📤 导出]      │
├───────────────────────────────────────────────────────────────────────┤
│  Tab: [🖥 系统侧账单(23)]  [📋 台账侧账单(17)]          ← sticky 吸顶  │
├───────────────────────────────────────────────────────────────────────┤
│  核对状态：[全部 ¥9659] [已核对 ¥0] [待确认 ¥0] [未匹配 ¥9659] [差异 ¥0]│
│  费用类型：[全部] [汇缴] [补缴] [调基补差]  归档批次：[全部批次 ▼]      │
├───────────────────────────────────────────────────────────────────────┤
│  ☐│状态 │类型│姓名│身份证      │险种│应缴月│费款期│系统金额│台账金额│差异│操作│
│  ☐│未匹配│汇缴│陶欢欢│500382****│养老│2026-04│2026-04│¥1233.12│   —   │ — │强制│
│  ☐│待确认│补缴│杨红  │500230****│医疗│  —   │2026-01│¥416.19 │   —   │ — │确认│
│  ☐│已核对│汇缴│陶欢欢│500382****│养老│2026-04│2026-04│¥1233.12│¥1233.12│ — │取消│
│  ☐│差异  │汇缴│王五  │500230****│失业│2026-04│2026-04│¥150.00 │   —   │+150│详情│
│  ☐│已归档│汇缴│陶欢欢│500382****│养老│2026-04│2026-04│¥1233.12│¥1233.12│ — │详情│  ← 灰色行
│                                                                       │
│  [☐ 全选] [确认所选] [取消确认] [强制核对]                 共 23 条    │
└───────────────────────────────────────────────────────────────────────┘
```

### 工具栏按钮

页面顶部有 5 个操作按钮，从左到右依次为：

| 按钮 | 功能 | 说明 |
|------|------|------|
| 📥 导入台账 | 打开导入对话框 | 上传社保局 Excel 台账。选择参保主体+参保规则+台账月份后上传文件 |
| ▶ 开始对账 | 触发匹配算法 | 无需台账也可执行。对账结果：MATCHED / PENDING(待确认) / DIFF(差异) / UNMATCHED(未匹配)。完成后 Toast 提示各状态计数 |
| ✅ 归档结果 | 创建归档批次 | 将 MATCHED 且 archived=false 的记录打包为新批次。存在 PENDING/DIFF 时弹确认窗，仅归档 MATCHED 记录。无待归档记录时 toast 提示 |
| 📦 归档记录 | 查看批次历史 | 无批次时 disabled。点击打开右侧抽屉展示所有批次列表 |
| 📤 导出 | 导出对账结果 | 当前为占位按钮 |

### Tab 切换

页面采用系统侧/台账侧双 Tab 分离展示：

- 点击 Tab 切换当前查看的账单侧，两侧各自独立维护筛选状态和金额统计
- Tab 角标显示当前记录总数，随筛选和对账结果实时更新
- `.bill-tabs` 使用 `position: sticky; top: 0; z-index: 100` 吸顶，向下滚动时始终可见
- 已核对记录同时出现在两个 Tab 中，带跨引用标记：
  - 系统侧：台账金额列显示 `¥1,500.00 ↔ T001`
  - 台账侧：系统金额列显示 `¥1,500.00 ↔ S001`
- 台账侧费用类型列：已核对时显示从系统侧回填的推断类型 badge，未核对时显示 "—"

### 筛选栏

两个 Tab 各自拥有独立的筛选栏，包含三组筛选器：

**核对状态筛选**（5 个按钮，每个附带金额统计）：
- 全部 | 已核对 | 待确认 | 未匹配 | 差异
- 金额统计随筛选和表格数据实时更新，如「已核对 ¥1500.00」
- 点击切换选中状态，同一时间仅一个激活

**费用类型筛选**（4 个按钮）：
- 全部 | 汇缴(蓝) | 补缴(紫) | 调基补差(青)
- 按费用类型过滤记录

**归档批次筛选**（下拉选择器）：
- 默认「全部批次」，选项随归档操作动态生成
- 选择某批次后表格仅显示该批次记录，通过 `record.archiveBatchId` 过滤

### 系统侧 Tab — 表格字段和行状态

系统侧表格共 12 列，每列显示规则如下：

| 列 | 显示规则 |
|---|---------|
| ☑ 复选框 | 用于批量操作。行选中后底部批量按钮根据选中行状态启用/禁用 |
| 核对状态 | 带颜色编码的 badge。已核对(绿) / 待确认(黄) / 未匹配(灰) / 差异(红) / 已归档(灰badge)。已归档时不显示批次编号，仅显示「已归档」 |
| 费用类型 | 汇缴(蓝badge) / 补缴(紫badge) / 调基补差(青badge)，所有记录均有值 |
| 姓名 | 加粗显示 |
| 身份证号 | 脱敏显示，格式：前 6 位 + `**********` + 后 4 位 |
| 险种 | 养老 / 医疗 / 失业 / 工伤 / 生育 / 大额医疗 / 公积金 |
| 应缴月份 | 即 `payableMonth`。汇缴初始就有值（=费款所属期）；补缴/调基补差初始为空显示「—」，对账匹配后从台账回填 |
| 费款所属期 | 即 `feePeriod`。汇缴=应缴月份；补缴=补缴月份；调基补差=补差月份。所有记录均有值 |
| 系统金额 | = 单位金额 + 个人金额，格式化为 ¥ 显示 |
| 台账金额 | 已核对时显示匹配台账的金额 + 跨引用标记 `↔ Txxx`；未核对/待确认/未匹配/差异时显示「—」 |
| 差异 | 已核对无差异时显示「—」；有差异时显示金额差：`+¥金额`(系统多，红色) / `-¥金额`(台账多，红色) |
| 操作 | 见下方「操作列按钮规则」 |

**行颜色编码**：

| 状态 | 行背景色 |
|------|---------|
| MATCHED（未归档） | 浅绿 `#F0FDF4` |
| PENDING | 浅黄 `#FEFCE8` |
| DIFF | 浅红 `#FEF2F2` |
| UNMATCHED | 白色（默认） |
| 已归档 | 灰色 `#F1F5F9`，opacity 0.7 |

**操作列按钮规则**（系统侧）：

| 记录状态 | 操作按钮 | 点击行为 |
|---------|---------|---------|
| UNMATCHED | **强制核对** | 打开强制核对确认弹窗 |
| PENDING | **确认核对** | 打开配对确认抽屉 |
| MATCHED（未归档） | **取消** | 恢复 PENDING 状态，清空 payableMonth |
| MATCHED（已归档） | **详情** | 打开差异详情抽屉（只读） |
| DIFF | **强制核对** | 打开强制核对确认弹窗 |

### 台账侧 Tab — 表格字段

台账侧表格同样 12 列，字段显示规则与系统侧基本一致，差异点：

| 列 | 与系统侧差异 |
|---|------------|
| 费用类型 | 已核对时显示推断类型 badge；未核对时显示「—」 |
| 应缴月份 | 即台账 billingMonth |
| 台账金额 | 格式化为 ¥，始终有值 |
| 系统金额 | 已核对时显示匹配系统记录的金额 + `↔ Sxxx`；未核对时显示「—」 |
| 差异 | 同上 |
| 操作 | 仅「详情」「确认核对」「取消」。**台账侧无强制核对按钮**——台账必须有对应系统侧记录才能匹配 |

### 配对确认抽屉

**触发**：PENDING 行点击「确认核对」→ 右侧滑出抽屉（宽度 600px）。

**内容结构**：
1. **顶部信息栏**：员工姓名 / 身份证脱敏 / 险种 / 应缴月份 / 同金额待确认统计
2. **智能推荐区**：系统按列表顺序自动推荐配对（系统第 N 笔 ↔ 台账第 N 笔），每对带复选框，默认全部勾选。提示文案："系统按列表顺序推荐配对。如不正确，请使用下方手动调整"
3. **手动调整区**：
   - 左侧列出所有系统侧记录（显示费用类型、金额、费款所属期）
   - 右侧列出所有台账侧记录（显示金额、应缴月份）
   - 配对关系区：每个系统记录对应一个下拉选择器，可选择台账记录重新映射
4. **底部按钮**：[取消] [确认全部配对]

**交互逻辑**：
- 勾选的配对才会生效
- 用户可取消某条推荐配对，或在配对关系区修改映射
- 如果两条系统记录选了同一条台账记录，显示错误提示
- 确认后：系统侧回填 `payableMonth`，台账侧回填 `feeTypeInferred`，两侧状态变为 MATCHED

### 差异详情抽屉

**触发**：DIFF 行点击「详情」→ 右侧滑出抽屉。

**内容结构**：
1. **基本信息区**：员工姓名、身份证、险种、应缴月份、费用类型
2. **金额对比区**：
   - 系统侧行：费用类型 + 金额（单位/个人拆分）
   - 台账侧行：金额（单位/个人拆分），无匹配时显示"无匹配记录"
   - 差异行：`+¥金额（系统多）` 或 `-¥金额（台账多）`
3. **差异分析区**：分类显示可能原因
   - 系统多（台账无）：台账漏采集 / 误增员 / 申报失败未通知
   - 台账多（系统无）：系统未计算该员工 / 台账数据错误
   - 金额不一致：基数调整 / 舍入差异 / 政策变更 / 录入错误
4. **底部按钮**：[关闭] [确认核对]

**确认核对按钮**：点击后抽屉内容切换为台账选择器——按身份证+险种列出所有台账侧候选记录，用户单选匹配。无候选时提示"无匹配的候选记录"。确认后调用 `confirmPendingPairing()` 回填双方字段。

### 强制核对确认弹窗

**触发**：系统侧 DIFF/UNMATCHED 行点击「强制核对」→ 模态弹窗（居中，480px 宽）。

**内容**：
- 标题：「强制核对确认」
- 警告文案（红色背景）："强制核对将把所选记录直接标记为「已核对」，无需台账匹配"
- 规则说明：台账侧差异将保持不变 / 应缴月份将使用账单月份 / 取消核对后可恢复原始状态
- 记录列表：每行显示姓名、身份证脱敏、险种、账单月份、金额
- 底部：[取消] [确认强制核对（红色 danger 按钮）]

**交互**：确认后 `forceMatch(recordIds)` → `matchStatus = MATCHED`，`forceMatched = true`，`payableMonth = billingMonth`，`matchedLedgerId = null`。取消强制核对时从 `_original*` 字段恢复原始状态。

### 归档批次抽屉

**触发**：工具栏「📦 归档记录」按钮 → 右侧滑出抽屉（宽度 560px）。

**内容**：
- 批次列表表格：批次名称 / 账单月份(小字) | 记录数 | 金额 | 归档时间 | 操作
- 每个批次行操作列为「**查看此批次**」按钮
- 无批次时显示「暂无归档批次记录」

**「查看此批次」交互**：
1. 关闭归档批次抽屉
2. 筛选栏「归档批次」下拉自动选中该批次
3. 表格过滤为仅显示该批次成员明细
4. 用户可以直观看到该批次包含的所有记录

### 导入台账对话框

**第一步 — 选择参数 + 上传**：
- 参保主体（下拉）、参保规则（下拉）、台账月份（下拉，必选）
- 拖拽/点击上传区，支持 .xlsx/.xls
- 未选月份时点击上传提示"请先选择台账月份"
- 底部：[取消] [下一步]

**第二步 — 预览确认**：
- 导入结果摘要：文件名 / 成功 N 条 / 格式错误 N 条
- 错误详情列表（如有）：行号 + 错误原因
- 预览表格（前 10 条）：姓名 / 身份证 / 险种 / 月份 / 金额 / 状态
- 判重检查：参保主体+规则+月份已有台账时提示"该维度下已有台账数据，是否覆盖？"
- 底部：[取消] [确认导入]

### 归档确认弹窗

**触发**：存在未处理的 PENDING 或 DIFF 记录时点击「✅ 归档结果」→ 模态弹窗。

**内容**：
- 标题：「归档确认」
- 提示文案："还有 N 条待确认和 M 条差异未处理，是否继续归档（仅归档已核对记录）？"
- 底部：[取消] [确认]

### 批量操作栏

底部固定操作栏，按钮根据当前 Tab 选中记录的匹配状态动态启用/禁用：

| 按钮 | 样式 | 启用条件 | 行为 |
|------|------|---------|------|
| **全选** | secondary | 始终可点击 | 选中/取消当前 Tab 所有可见记录 |
| **确认所选** | primary | 选中记录含 PENDING | 批量确认 PENDING 记录的配对 |
| **取消确认** | secondary | 选中记录含 MATCHED(未归档) | 批量取消已核对，恢复 PENDING |
| **强制核对** | danger(红) | 选中记录含 DIFF/UNMATCHED | 仅对选中中的 DIFF/UNMATCHED 执行强制核对。选中 MATCHED/PENDING 记录被自动排除 |

### 汇总列表页

**页面路径**：`prototype/reconciliation/summary.html`

按地区+参保主体分组展示所有参保规则的对账概览。

**页面布局**：
- 顶部筛选：月份 + 地区下拉
- 操作按钮：刷新 / 批量导出 / 批量对账 / 批量归档 / 导入台账
- 信息栏：「共 N 条规则，N 个参保主体，已导入 N 条，已归档 N 条」

**二级表头**：

```
系统侧明细（已核对 | 差异 | 已归档） │ 台账侧明细（总计 | 已核对 | 差异 | 待确认）
```

两组之间 2px 竖线边框分隔。

**分组行**（按地区+参保主体聚合）：
- 参保主体列：主体名称（粗体 13px）+ 地区（灰色 11px），点击展开/收起子行
- 各列显示子行金额合计（聚合值），金额为 0 或未对账时显示「—」
- 操作：`[详情] [对账]`

**子行**（单规则明细）：
- 显示规则名称、参保主体、月份及各统计数字（笔数+金额）
- 行颜色：已对账无差异→浅绿 `#F0FDF4`；已对账有差异→浅黄 `#FFFBEB`；已归档→灰色 `#F1F5F9` opacity 0.7
- 金额颜色：已匹配绿色，差异红色，待确认橙色
- 操作：`[详情]` → 跳转到明细核对页

**跳转方式**：
- 子行详情：`?ruleName=规则名&month=月份`
- 分组行详情：`?groupId=region|insuranceSubject`

---

## 导入流程

1. **导入台账**：选择参保主体+规则+月份 → 上传 Excel → 格式校验+判重 → 预览 → 确认
2. **开始对账**：执行匹配算法（无需台账也可执行）→ loading 遮罩 → Toast 结果
3. **处理差异和待确认**：配对抽屉确认 / 差异详情分析 / 批量操作
4. **归档**：将 MATCHED+unarchived 记录归档为新批次 → 锁定
5. **归档后**：可查看批次历史、筛选批次。已归档记录不可修改

---

## 批量操作

批量操作在 **当前 Tab 的可见记录** 内生效：

| 操作 | 适用状态 | 行为 |
|------|----------|------|
| 批量确认核对 | PENDING | 智能推荐配对 |
| 批量取消核对 | MATCHED（未归档） | 恢复 PENDING，清空回填字段 |
| 批量强制核对 | DIFF/UNMATCHED（仅系统侧） | 直接标记 MATCHED |
| 全选 | 全部 | 仅当前 Tab 可见记录 |

---

## 边界情况

| 场景 | 处理 |
|------|------|
| 同一台账重复导入 | 参保主体+规则+月份判重，提示覆盖 |
| 核对成功后取消 | 恢复 PENDING，系统侧清空 payableMonth，台账侧清空 feeTypeInferred |
| 已归档取消核对 | 拦截，toast "已归档记录不可取消核对" |
| 补缴/调基补差无台账 | UNMATCHED（非差异，可在后续月份匹配） |
| 汇缴无台账 | DIFF(system_more)，汇缴须在当前月份有对应台账 |
| 台账无系统对应 | DIFF(ledger_more) |
| 无待归档记录 | Toast "无待归档记录" |
| 台账侧强制核对 | 不提供，台账必须有对应系统侧记录 |
| 大批量数据 | 超过 1000 条显示进度条，分批匹配 |

---

## 两层页面结构

1. **汇总列表页** (`prototype/reconciliation/summary.html`) — 按地区+参保主体分组，展开查看规则子行。二级表头：系统侧明细(已核对/差异/已归档) | 台账侧明细(总计/已核对/差异/待确认)。支持批量导入、批量对账、批量归档。
2. **明细核对页** (`prototype/reconciliation/unified.html`) — Tab 切换系统侧/台账侧，逐笔核对操作。面包屑返回汇总页。支持 `?ruleName=X&month=Y` 和 `?groupId=region|subject` 两种入口。

---

## 归档批次

每次归档操作将当前 MATCHED 且 archived=false 的记录创建为新批次。同月份可多次归档。批次通过 `archiveBatchId` 关联记录。工具栏「归档记录」按钮打开批次抽屉。筛选栏「归档批次」下拉过滤。详见 PRD `docs/superpowers/prd/reconciliation/reconciliation.md`。

---

## 前端实现细节

### CSS 类名

| 类名 | 用途 |
|------|------|
| `.bill-tabs` / `.bill-tab` / `.bill-tab-panel` | Tab 切换组件 |
| `.cross-ref` | 跨引用标记（↔ Txxx / ↔ Sxxx） |
| `.filter-bar__item` / `.filter-bar__count` | 筛选按钮 + 金额显示 |
| `.row-matched` / `.row-pending` / `.row-diff` / `.row-archived` | 行状态颜色 |
| `.status-badge--matched` / `--pending` / `--diff` / `--unmatched` / `--archived` | 状态 badge |
| `.qy-btn--danger` / `.qy-btn--success` | 强制核对(红) / 归档(绿) |
| `.archive-batch-section` / `.archive-badge` | 归档批次相关 |

### JS 函数摘要

| 函数 | 说明 |
|------|------|
| `startReconciliation()` / `executeMatching()` | 触发匹配引擎 |
| `switchBillTab(tab)` | Tab 切换 |
| `getFilteredSystemRecords()` / `getFilteredLedgerRecords()` | 筛选记录 |
| `renderSystemTable()` / `renderLedgerTable()` | 渲染表格 |
| `archiveResults()` / `doArchive(toArchive)` | 归档操作 |
| `forceMatch(recordIds)` / `showForceMatchConfirm()` | 强制核对 |
| `cancelMatch(id)` / `doCancelMatch(id)` | 取消核对 |
| `openArchiveBatchDrawer()` / `viewArchiveBatch(batchId)` | 归档批次抽屉 |
| `renderSummaryTable()` / `batchReconcile()` / `batchArchive()` | 汇总页操作 |

### 实施差异记录

1. Tab 切换模式（PRD v6），系统侧/台账侧分离展示
2. 统计金额整合到筛选按钮，不再使用独立统计卡片
3. 补缴/调基补差无台账 → UNMATCHED（非 DIFF），可在后续月份继续匹配
4. 台账侧不允许强制核对
5. 归档为独立布尔标记而非 matchStatus 值
6. CSS 布局从 margin-left 改为 flex
7. 同一成员+险种+补差月份分别展示多条明细，每笔独立核对（非合并）

---

## Demo 数据（2026-04-30）

系统侧 23 条，台账侧 26 条。覆盖汇缴(陶欢欢5险种/李芳4险种)、补缴(陈鸣/杨红/李芳)、调基补差(陶欢欢/周敏)场景。`forcePending` 标记（王磊5险种/李芳医疗）用于演示金额一致但需人工审核。

---

## 参考文件

- PRD：`docs/superpowers/prd/reconciliation/reconciliation.md`
- 原型：`prototype/reconciliation/summary.html`、`unified.html`
- 账单生成逻辑：`source/应付核对系统账单明细取值逻辑.md`
