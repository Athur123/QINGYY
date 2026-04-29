# 对账复核 Tab 切换设计 Spec

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有统一表格拆分为系统侧/台账侧两个独立 Tab，解决系统侧与台账侧账单明细混在一起无法辨识的问题。

**Architecture:** 现有数据模型（systemRecords、ledgerRecords、matchingResults）不变，仅改造渲染层。将 `#unifiedTable` 替换为 `.bill-tabs` + 两个 `.bill-tab-panel`，每个面板有独立的筛选、统计和表格。

**Tech Stack:** HTML/CSS/JS 单文件原型（qingyang-reconciliation-unified.html）

---

## 数据模型（不变）

当前 `getAllDisplayRecords()` 遍历 systemRecords 和 ledgerRecords，合并为一个列表渲染。改造后不再调用此函数，改为：

- `getSystemDisplayRecords()` — 返回 systemRecords 的渲染数据（含关联 ledger 信息）
- `getLedgerDisplayRecords()` — 返回 ledgerRecords 的渲染数据（含关联 system 信息）

已匹配的记录同时出现在两个 Tab 中：
- 系统侧行显示 `ledgerAmount` 和 `ledgerId` 链接
- 台账侧行显示 `systemAmount`、`feeTypeInferred`（推断的账单类型）和 `systemId` 链接

## UI 结构

```
┌─────────────────────────────────────────────────┐
│ Tab: [系统侧账单 6]  [台账侧账单 7]              │
├─────────────────────────────────────────────────┤
│ 汇总摘要卡片（各Tab独立）                         │
│ 筛选栏：匹配状态 + 账单类型                       │
│ 表格：                                          │
│   ☑ | 状态 | 类型 | ... | 操作                   │
│ 页脚：全选 | 确认所选 | 取消确认 | 计数           │
└─────────────────────────────────────────────────┘
```

## CSS 结构

- `.bill-tabs` — Tab 栏容器，底部 2px 边框
- `.bill-tab` — 单个 Tab，底部 2px 透明边框，`.is-active` 时边框变蓝
- `.bill-tab .tab-count` — 记录数角标
- `.bill-tab-panel` — 面板容器，`.is-active` 时显示
- 各 Tab 面板内的 `.summary-strip`、`.filter-bar`、`.data-table` 结构与现有类似

## Tab 列定义

### 系统侧 Tab

| 列 | 说明 |
|----|------|
| ☑ | 复选框 |
| 匹配状态 | 已匹配/待确认/差异 badge |
| 账单类型 | 汇缴/补缴/调基补差 badge |
| 姓名 | 加粗 |
| 身份证号 | 脱敏 |
| 险种 | 文本 |
| 应缴月份 | 汇缴显示，补缴/调基显示 "—" |
| 费款所属期 | 所有类型均显示 |
| 系统金额 | 格式化为 ¥ |
| 台账金额 | 已匹配显示金额 + `↔ Txxx` 链接，否则 "—" |
| 差异 | 差异时显示金额，否则 "—" |
| 操作 | 详情/确认配对/取消 |

### 台账侧 Tab

| 列 | 说明 |
|----|------|
| ☑ | 复选框 |
| 匹配状态 | 已匹配/待确认/差异 badge |
| 账单类型 | 已匹配显示推断类型 badge，否则 "—" |
| 姓名 | 加粗 |
| 身份证号 | 脱敏 |
| 险种 | 文本 |
| 应缴月份 | 即 billingMonth |
| 费款所属期 | feePeriod |
| 台账金额 | 格式化为 ¥ |
| 系统金额 | 已匹配显示金额 + `↔ Sxxx` 链接，否则 "—" |
| 差异 | 差异时显示金额，否则 "—" |
| 操作 | 详情/确认配对/取消 |

## 交互规则

1. **Tab 切换**：点击 Tab 切换 `.is-active`，隐藏/显示对应 `.bill-tab-panel`
2. **筛选状态独立**：两个 Tab 各自维护 `matchFilter` 和 `typeFilter` 状态
3. **汇总摘要独立**：每个 Tab 显示各自的统计（总数、已匹配、待确认、差异）
4. **操作联动**：在任一侧取消匹配或确认配对，两个 Tab 都需要重新渲染（数据模型共享）
5. **批量操作**：全选/确认所选/取消确认仅在当前 Tab 的可见记录内生效
6. **抽屉交互**：
   - 系统侧「确认配对」→ 打开配对抽屉，选择台账记录
   - 台账侧「确认配对」→ 打开配对抽屉，选择系统记录
   - 操作完成后两侧表格同步更新

## 行颜色

- 已匹配：绿色背景 `#F0FDF4`
- 待确认：黄色背景 `#FEFCE8`
- 差异：红色背景 `#FEF2F2`

两侧 Tab 使用相同的行颜色方案。

## 文件变更

**修改：** `prototype/qingyang-reconciliation-unified.html`
- HTML：替换 `#unifiedTable` 为 `.bill-tabs` + 两个 `.bill-tab-panel`
- CSS：新增 `.bill-tabs`、`.bill-tab`、`.bill-tab-panel`、`.summary-strip` 样式
- JS：
  - 新增 `currentSystemMatchFilter`、`currentSystemTypeFilter`、`currentLedgerMatchFilter`、`currentLedgerTypeFilter` 状态变量
  - 新增 `getSystemDisplayRecords()`、`getLedgerDisplayRecords()`
  - 新增 `switchBillTab(tab)`、`toggleSystemMatchFilter()`、`toggleSystemTypeFilter()`、`toggleLedgerMatchFilter()`、`toggleLedgerTypeFilter()`
  - 修改 `renderTable()` → `renderSystemTable()` + `renderLedgerTable()`
  - 修改 `renderPairingDrawer()` 兼容从两侧打开
  - 修改 `doCancelMatch()`、`confirmPendingPairing()` 等数据变更后触发 `renderAllTables()`

## 测试场景

1. 导入台账 → 系统侧 Tab 显示 6 条，台账侧 Tab 显示 7 条
2. 开始对账 → 两侧统计卡片更新，行颜色正确
3. 张三汇缴已匹配 → 两侧均显示，系统侧显示 `↔ T001`，台账侧显示类型「汇缴」+ `↔ S001`
4. 李四补缴差异 → 两侧均显示为差异行，系统侧差异 `+¥600`，台账侧差异 `-¥450`
5. 台账侧「确认配对」→ 打开抽屉选择系统记录，确认后两侧同步更新
6. 切换 Tab 后筛选状态各自独立保留
