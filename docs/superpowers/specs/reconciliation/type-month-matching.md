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

## UI 设计

### 页面整体布局

```
┌───────────────────────────────────────────────────────────────────────┐
│  青阳云 HRO  |  智能薪酬  │  对账复核                                  │
├───────────────────────────────────────────────────────────────────────┤
│  社保对账复核                                                          │
├───────────────────────────────────────────────────────────────────────┤
│  [📥 导入台账] [▶ 开始对账] [✅ 归档结果] [📦 归档记录] [📤 导出]      │
├───────────────────────────────────────────────────────────────────────┤
│  Tab: [🖥 系统侧账单(23)]  [📋 台账侧账单(17)]                        │
├───────────────────────────────────────────────────────────────────────┤
│  核对状态：[全部 ¥9659] [已核对 ¥0] [待确认 ¥0] [未匹配 ¥9659] [差异 ¥0]│
│  费用类型：[全部] [汇缴] [补缴] [调基补差]  归档批次：[全部批次 ▼]      │
├───────────────────────────────────────────────────────────────────────┤
│  数据表格（12列，见下方）                                               │
├───────────────────────────────────────────────────────────────────────┤
│  [☐ 全选] [确认所选] [取消确认] [强制核对]                 共 23 条    │
└───────────────────────────────────────────────────────────────────────┘
```

### Tab 切换设计

页面采用 **Tab 切换** 方式分离系统侧和台账侧账单明细。`position: sticky; top: 0` 吸顶。两侧各自独立维护筛选状态和金额统计。已核对记录同时出现在两个 Tab 中，带跨引用标记（系统侧 `↔ Txxx`，台账侧 `↔ Sxxx`）。

### 系统侧 Tab 表格字段

| 列 | 说明 |
|---|------|
| ☑ | 复选框（用于批量操作） |
| 核对状态 | UNMATCHED(灰) / MATCHED(绿) / PENDING(黄) / DIFF(红) / 已归档(灰badge) |
| 费用类型 | 汇缴(蓝badge) / 补缴(紫badge) / 调基补差(青badge) |
| 姓名 | 加粗 |
| 身份证号 | 脱敏显示（前6+后4） |
| 险种 | 文本 |
| 应缴月份 | 即 payableMonth。汇缴初始就有值，补缴/调基补差初始为空对账后回填 |
| 费款所属期 | 即 feePeriod。汇缴=应缴月份；补缴=补缴月份；调基补差=补差月份。所有类型均有值 |
| 系统金额 | = 单位金额 + 个人金额 |
| 台账金额 | 已核对时显示台账金额 + `↔ Txxx` 跨引用，否则 "—" |
| 差异 | +金额(系统多) / -金额(台账多)，红色加粗。无差异显示 "—" |
| 操作 | 各状态对应不同按钮：详情 / 确认核对 / 取消 / 强制核对 |

### 台账侧 Tab 表格字段

| 列 | 说明 |
|---|------|
| ☑ | 复选框 |
| 核对状态 | 同系统侧 |
| 费用类型 | 已核对显示推断类型 badge，否则 "—" |
| 姓名 | 加粗 |
| 身份证号 | 脱敏显示 |
| 险种 | 文本 |
| 应缴月份 | 即 billingMonth |
| 费款所属期 | feePeriod |
| 台账金额 | 格式化为 ¥ |
| 系统金额 | 已核对显示金额 + `↔ Sxxx`，否则 "—" |
| 差异 | 同上 |
| 操作 | 详情 / 确认核对 / 取消（台账侧无强制核对） |

### 配对确认抽屉

点击 PENDING 行的「确认核对」→ 右侧滑出抽屉。智能推荐：系统按列表顺序自动推荐配对（系统第N笔 ↔ 台账第N笔），默认全部勾选。支持手动下拉调整映射关系。确认后回填 payableMonth 和 feeTypeInferred。

### 差异详情抽屉

点击 DIFF 行的「详情」→ 右侧滑出抽屉。显示金额对比（系统侧 vs 台账侧）、差异分析、可能原因。底部「确认核对」按钮可手动匹配差异或未匹配记录。

### 导入台账对话框

两步流程：选择参保主体+规则+月份 → 上传 Excel → 预览导入结果（成功/错误条数+详情）→ 确认导入。支持 .xlsx/.xls。判重：参保主体+规则+月份已有台账时提示覆盖。

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
