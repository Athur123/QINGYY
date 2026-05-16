# 对账复核 v1 完整实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 实现社保对账复核完整功能——台账导入、精确金额匹配、类型/月份互推、Tab分离、批量操作、强制核对、归档批次、已付款状态

**Architecture:** 两层页面结构（汇总列表 + 明细核对）。明细核对页采用系统侧/台账侧 Tab 分离，匹配算法按 `身份证|险种|应缴月份` 分组做精确金额匹配。导入按 `参保主体 + 参保规则 + 账单月份` 维度判重覆盖。已付款从已归档批次发起。

**Tech Stack:** Vanilla JS, HTML, CSS — single-file prototypes. SheetJS (xlsx CDN) for Excel import.

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `prototype/reconciliation/summary.html` | 汇总列表页 — 按参保主体分组展示对账概览 |
| `prototype/reconciliation/unified.html` | 明细核对页 — 系统侧/台账侧逐笔核对 |
| `docs/superpowers/specs/reconciliation/type-month-matching.md` | 设计文档 |

---

## 一、数据模型与状态机

### Task 1.1: 基础数据 + 常量

- [ ] 定义 `MATCH_STATUS` 五状态常量（UNMATCHED / MATCHED / PENDING / DIFF / PAID）
- [ ] 定义 `BILL_TYPES` 三费用类型（huijiao / bujiao / tiaoji）
- [ ] 定义 `DIFF_TYPE` 三差异类型（system_more / ledger_more / amount_mismatch）
- [ ] 定义 `INSURANCE_TYPE_ALIAS` 险种别名映射表（7 险种 + 大额医疗）
- [ ] 预置 `systemRecords` 23 条演示数据（覆盖汇缴/补缴/调基补差全部场景）
- [ ] 初始化 `ledgerRecords = []`、`matchingResults = { matched, pending, diffs, executed }`、`archiveBatches = []`
- [ ] 每条记录含 `archiveBatchId` 字段

### Task 1.2: 状态机实现

- [ ] `getMatchStatusLabel(status)` + `getMatchStatusClass(status)` 五状态映射
- [ ] 行颜色编码 CSS（`.row-matched` `.row-pending` `.row-diff` `.row-archived` `.row-paid`）
- [ ] 状态 badge CSS（`.status-badge--matched` `--pending` `--diff` `--unmatched` `--archived` `--paid`）

---

## 二、台账导入

### Task 2.1: 导入对话框

- [ ] 两步流程：参数选择（参保主体+规则+月份）→ 上传 → 预览确认
- [ ] `openImportDialog()` / `closeImportDialog(event)` 
- [ ] 月份选择器必选校验（未选时提示）
- [ ] 文件拖拽+点击上传，支持 .xlsx/.xls

### Task 2.2: 数据标准化

- [ ] 身份证标准化（去空格、X 大写）
- [ ] 险种别名映射（通过 `INSURANCE_TYPE_ALIAS` 转标准名，无法识别标记"未知"）
- [ ] 金额保留 2 位小数
- [ ] 应缴月份统一 YYYY-MM 格式
- [ ] 判重：按 `参保主体 + 参保规则 + 账单月份` 维度只保留一份台账，重复导入时提示是否覆盖
- [ ] 导入预览：成功/错误条数 + 错误行详情 + 前 10 条预览
- [ ] 导入记录写入当前页面上下文对应的账单批次，不支持同一导入操作跨月份累加

---

## 三、匹配算法

### Task 3.1: 核心匹配引擎

- [ ] `buildSystemCandidateSet(pageContext, systemRecords)` — 按当前页面上下文组装系统候选集
  - 汇缴：取 `payableMonth = 当前账单月份`
  - 自动拆分补缴：取 `feePeriod = 当前账单月份` 且 `payableMonth` 为空
  - 单补缴/调基/政策调整：取 `payableMonth` 为空记录
- [ ] `buildLedgerCandidateSet(pageContext, ledgerRecords)` — 仅取当前 `参保主体 + 参保规则 + 账单月份` 的有效台账批次
- [ ] `normalizeMatchingRecords(records, side)` — 标准化身份证、险种、月份、金额；拦截非法输入
- [ ] `getEffectivePayableMonth(record, pageContext, side)` — 计算本轮分组用“有效应缴月份”
- [ ] `groupByMainKey(records)` — 按 `idCard | insuranceType | effectivePayableMonth` 分组
- [ ] `bucketByAmount(group)` — 主分组内二次按金额建桶
- [ ] `executeMatching()` — 主匹配函数
  - Pass 1：先处理唯一 1:1 金额桶；汇缴且非 `forcePending` 自动进入 `MATCHED`，补缴 / 调基补差 / `forcePending` 进入 `PENDING`
  - Pass 2：处理同金额多笔和 `forcePending`
  - Pass 3：处理单边残留和 `amount_mismatch`
  - 自动匹配成功后双向回填；待确认候选由用户确认核对后再双向回填
- [ ] `applyAutoMatchedPair()` — 汇缴唯一 1:1 自动落 `MATCHED`
- [ ] `applyPendingCandidate()` — 非汇缴唯一 1:1、同金额多笔、`forcePending` 落 `PENDING`
- [ ] `confirmSelectedPairing()` — 统一确认核对，成功后回填 `payableMonth / matchedLedgerId / matchedSystemId / feeTypeInferred / payableMonthInferred`
- [ ] `applyAmountMismatch()` — 标记双方残差为 `DIFF(amount_mismatch)`
- [ ] `applySingleSideResidual()` — 汇缴系统多→`DIFF(system_more)`；补缴/调基系统多→`UNMATCHED`；台账多→`DIFF(ledger_more)`
- [ ] `calculateStats()` — 匹配结果统计（matched/pending/diff 计数+金额）
- [ ] 无需台账也可执行对账（汇缴→DIFF，补缴/调基补差→UNMATCHED）

### Task 3.2: forcePending 机制（演示用）

- [ ] `forcePending` 字段标记的记录跳过自动匹配直接进入 PENDING
- [ ] Post-processing：修正 forcePending 被分到 DIFF 分支的记录
- [ ] 明确 `forcePending` 仅影响自动决策，不改变人工确认后的回填规则

### Task 3.3: 匹配算法测试任务

- [ ] 覆盖 `S1-S15` 样例矩阵
- [ ] 验证“先消唯一，再处理残差”的执行顺序
- [ ] 验证同一主分组内 `MATCHED + PENDING + DIFF` 可同时存在
- [ ] 验证 `amount_mismatch` 不会吞掉已可自动匹配的记录
- [ ] 验证强制核对只影响系统侧，不为台账侧生成伪匹配关系

---

## 四、明细核对页 — Tab 分离与表格

### Task 4.1: Tab 组件

- [ ] `.bill-tabs` + `.bill-tab` + `.bill-tab-panel` HTML 结构
- [ ] `switchBillTab(tab)` — Tab 切换交互
- [ ] Tab `position: sticky; top: 0` 吸顶
- [ ] Tab 角标显示当前记录总数
- [ ] 两侧各自独立维护筛选状态（`currentBillTab` / `currentSystemMatchFilter` / `currentSystemTypeFilter` / `currentLedger*`）

### Task 4.2: 筛选栏

- [ ] 核对状态筛选（5 按钮 + 金额统计），`toggleSystemMatchFilter()` / `toggleLedgerMatchFilter()`
- [ ] 费用类型筛选（4 按钮），`toggleSystemTypeFilter()` / `toggleLedgerTypeFilter()`
- [ ] 归档批次下拉筛选器，`updateArchiveBatchFilters()`
- [ ] `getFilteredSystemRecords()` / `getFilteredLedgerRecords()` 筛选逻辑

### Task 4.3: 系统侧表格渲染

- [ ] `getSystemDisplayRecords()` — 生成渲染数据（合并 ledger 关联信息）
- [ ] `renderSystemTable()` — 12 列表格渲染
  - 复选框 / 核对状态 / 费用类型 / 姓名 / 身份证 / 险种 / 应缴月份 / 费款所属期 / 系统金额 / 台账金额（+跨引用） / 差异 / 操作
- [ ] 操作列按钮按状态映射：UNMATCHED / PENDING / DIFF→确认核对，MATCHED→取消核对/详情(已归档)，PAID→详情；系统侧另保留批量强制核对兜底能力
- [ ] 已核对记录台账金额列显示 `↔ Txxx` 跨引用
- [ ] 已归档行灰色背景 +「已归档」badge
- [ ] 已付款行蓝色背景 +「已付款」badge

### Task 4.4: 台账侧表格渲染

- [ ] `getLedgerDisplayRecords()` — 生成渲染数据（合并 system 关联信息）
- [ ] `renderLedgerTable()` — 同上结构
- [ ] 费用类型列：已核对显示推断类型 badge，否则 "—"
- [ ] 系统金额列：已核对显示金额 + `↔ Sxxx` 跨引用
- [ ] **台账侧无强制核对按钮**

### Task 4.5: 批量操作栏

- [ ] 全选 / 批量确认核对 / 批量取消核对 / 强制核对 四个按钮
- [ ] `getSelectedSystemIds()` / `toggleSystemSelectAll()` / `updateSystemBatchButtons()`
- [ ] 按钮根据选中行状态动态启用/禁用
- [ ] `systemBatchConfirm()` / `systemBatchCancel()` / `systemBatchForceMatch()`
- [ ] 台账侧独立批量逻辑（无强制核对）

---

## 五、交互组件

### Task 5.1: 配对确认抽屉

- [ ] `PENDING / UNMATCHED / DIFF` 行点击→右侧滑出抽屉（`#pairingDrawer`，宽 600px）
- [ ] 点击「批量确认核对」从系统侧或台账侧选中记录打开同一个抽屉
- [ ] 抽屉分为系统侧明细、台账侧明细、合计校验区
- [ ] `confirmPairing()` / `confirmSelectedPairing()` — 确认核对，回填 `payableMonth` 和 `feeTypeInferred`
- [ ] 支持 1:1、一对多、多对一、多对多
- [ ] 确认前校验同成员 + 同险种 + 当前账单月份 + 同费款所属期 + 系统合计金额 = 台账合计金额
- [ ] 确认成功后生成同一 `matchGroupId`，组内记录全部转 `MATCHED`

### Task 5.2: 差异详情抽屉

- [ ] DIFF 行点击→右侧滑出抽屉（`#detailDrawer`）
- [ ] 信息区：员工信息 + 费用类型
- [ ] 金额对比区：系统侧 vs 台账侧，金额拆分（单位/个人）
- [ ] 差异分析区：可能原因分类
- [ ] 台账选择器：按身份证+险种筛选候选，单选匹配
- [ ] `confirmFromDrawer()` — 确认匹配

### Task 5.3: 强制核对

- [ ] 系统侧批量操作栏保留「强制核对」按钮，单行操作列不展示强制核对
- [ ] `showForceMatchConfirm(recordIds)` — 确认弹窗
- [ ] `forceMatch(recordIds)` — 标记 `matchStatus=MATCHED`, `forceMatched=true`, `payableMonth` 回填为当前页面账单月份
- [ ] 强制核对允许选择一笔或多笔系统侧 `DIFF / UNMATCHED` 明细后批量执行
- [ ] 保存核对前原始状态快照，用于取消核对时完整恢复
- [ ] `cancelMatch` 增加快照恢复逻辑
- [ ] `systemBatchForceMatch()` — 批量强制核对
- [ ] 台账侧无强制核对入口

### Task 5.4: 导入对话框

- 同 Task 2.1

### Task 5.5: 确认弹窗

- [ ] `showConfirmDialog(title, text, callback)` — 通用确认弹窗
- [ ] 归档确认弹窗：存在 PENDING/DIFF 时提示

---

## 六、取消核对

### Task 6.1: 取消逻辑

- [ ] `doCancelMatch(id)` — 已归档记录拦截（toast "已归档记录不可取消核对"）
- [ ] `cancelMatch(id)` — 清空本次匹配回填字段，并恢复至核对前原始状态
- [ ] 自动匹配、人工确认、强制核对取消时都按同一快照口径恢复

---

## 七、归档批次

### Task 7.1: 归档核心

- [ ] `archiveResults()` — 筛选 MATCHED+unarchived → 调用 `doArchive(toArchive)`
- [ ] `doArchive(toArchive)` — 创建批次对象 → 标记系统侧+台账侧 `archived=true, archiveBatchId`
- [ ] 批次编号自动递增（第1批/第2批...）
- [ ] 空批次 toast "无待归档记录"
- [ ] DIFF/PENDING 存在时确认弹窗

### Task 7.2: 归档批次抽屉

- [ ] 工具栏「📦 归档记录」按钮（无批次 disabled）
- [ ] `openArchiveBatchDrawer()` — 右侧抽屉展示批次列表
- [ ] `viewArchiveBatch(batchId)` — 关闭抽屉 → 筛选器设为该批次 → 表格过滤
- [ ] 批次列表含「查看此批次」和「申请付款」按钮

### Task 7.3: 归档筛选

- [ ] `updateArchiveBatchFilters()` — 动态更新下拉选项
- [ ] `onSystemArchiveBatchChange()` / `onLedgerArchiveBatchChange()` — 筛选切换
- [ ] 筛选逻辑集成到 `getFilteredSystemRecords()` / `getFilteredLedgerRecords()`

---

## 八、已付款状态

### Task 8.1: 付款功能

- [ ] `showPaymentConfirm(batchId)` — 付款确认弹窗
- [ ] `doPayment(batchId)` — 遍历批次内 MATCHED+archived → `matchStatus = PAID`
- [ ] 台账侧同步更新为 PAID
- [ ] 已付款后该批次「申请付款」无效

### Task 8.2: 已付款行渲染

- [ ] PAID 行蓝色背景（`.row-paid`）
- [ ] 状态列「已付款」badge
- [ ] 操作列仅「详情」
- [ ] 已付款记录不可取消核对

---

## 九、汇总列表页

### Task 9.1: 页面框架

- [ ] `DEMO_RULES` 6 条规则定义（含 `systemArchived`/`systemArchivedAmount` 字段）
- [ ] `SYSTEM_RECORDS_ALL` + `MOCK_LEDGER_DATA` 全量数据
- [ ] `buildSubjectGroups()` — 按 `region + insuranceSubject` 分组
- [ ] 信息栏：规则数 / 参保主体数 / 已导入数 / 已归档数
- [ ] 账单月份上下文 + 地区筛选下拉
- [ ] 切换账单月份时不减少主体 / 规则清单，仅刷新当前页面上下文

### Task 9.2: 表格渲染

- [ ] 二级表头：系统侧明细(已核对/差异/已归档) │ 台账侧明细(总计/已核对/差异/待确认)
- [ ] 分组行：参保主体(粗体)+地区(灰字)，点击展开/收起
- [ ] 子行：规则名称 + 当前账单月份 + 各列统计（笔数+金额）
- [ ] 汇总表账单月份列统一展示当前账单月份上下文
- [ ] 行颜色：已对账无差异→浅绿，有差异→浅黄，已归档→灰
- [ ] 金额颜色：匹配绿 / 差异红 / 待确认橙

### Task 9.3: 批量操作

- [ ] `toggleSelectAll()` / `toggleRuleSelection()` — 行选择
- [ ] `batchReconcile()` — 批量对账，遍历选中规则调用 `executeMatchingForRule`
- [ ] `batchArchive()` — 批量归档，仅 reconciled+零差异规则
- [ ] `openImportDialog()` — 总台账导入，自动按规则拆分；台账月份由当前账单月份上下文锁定，不允许手动切换
- [ ] `navigateToDetail()` / `groupDetail()` — 跳转明细页，均传递当前账单月份 `month`

### Task 9.4: 交互

- [ ] `toggleGroupExpand(groupId)` — 分组展开/收起
- [ ] `toggleGroupCheckbox(checkbox)` — 分组批量选择
- [ ] `groupReconcile(groupId)` — 分组一键对账
- [ ] Toast 通知组件
- [ ] 导入对话框复用明细页样式

---

## 十、CSS 与布局

- [ ] `.qy-main { margin-left: 0 }` 覆盖 base.css 的 flex 布局修正
- [ ] `.qy-page { padding: 20px 20px }` 页面内边距
- [ ] 筛选栏 `.filter-bar` 样式（按钮+金额）
- [ ] Tab 吸顶 sticky
- [ ] 抽屉 `.drawer-overlay` + `.drawer` 通用组件
- [ ] 弹窗 `.force-match-dialog` 通用组件
- [ ] Batch 相关样式（`.batch-row` `.sub-row` `.summary-cell` 等）
- [ ] 归档批次相关样式（`.archive-badge` `.archive-batch-section` 等）

---

## 实施顺序

建议按以下顺序交付，每个阶段均可独立验证：

| 阶段 | Task | 产出 |
|------|------|------|
| 1 | 一 + 二 + 三 | 数据模型 + 导入 + 匹配逻辑（可对账） |
| 2 | 四 | Tab分离 + 表格渲染 + 批量操作（完整明细页） |
| 3 | 五 + 六 | 交互组件 + 取消核对（完整交互闭环） |
| 4 | 七 | 归档批次（多次归档+筛选+抽屉） |
| 5 | 九 | 汇总列表页（两层结构完整） |
| 6 | 八 | 已付款状态（归档→付款最终闭环） |
