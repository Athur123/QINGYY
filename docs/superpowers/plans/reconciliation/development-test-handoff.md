# 对账复核研发测试开工清单 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将对账复核模块当前主 spec、PRD 和现行原型收口为一份研发与测试可直接开工、排期、认领、联调的任务清单。

**Architecture:** 以 `type-month-matching.md` 作为算法真源，以 `unified.html` 作为明细核对页参考原型，以 `summary.html` 作为汇总页参考原型。实现顺序采用“统一匹配口径 → 明细页引擎 → 明细页交互 → 导入与归档 → 汇总页对齐 → 联调回归”，避免汇总页和明细页各自实现一套算法。

**Tech Stack:** 当前仓库为 HTML / CSS / Vanilla JS 原型；正式研发实现可沿用团队既定 Vue 3 + TypeScript + Vite，但本清单不展开接口与数据库设计。

---

## Files Overview

**Source of truth**
- `docs/superpowers/specs/reconciliation/type-month-matching.md`
- `docs/superpowers/specs/reconciliation/ledger-import.md`
- `docs/superpowers/prd/reconciliation/reconciliation.md`
- `docs/superpowers/plans/reconciliation/v1-complete-plan.md`

**Active prototype reference**
- `prototype/reconciliation/unified.html`
- `prototype/reconciliation/summary.html`

**Current prototype gaps that must be treated as implementation inputs, not final behavior**
- `prototype/reconciliation/unified.html`
  - `makeGroupKey()` 当前按 `idCard | insuranceType | billingMonth` 分组，尚未实现主 spec 的“有效应缴月份”规则。
  - `executeMatching()` 当前未拆分候选集、未显式处理“先消唯一，再处理残差”、未完整表达 `amount_mismatch`。
  - `cancelMatch()` 当前普通取消统一恢复 `PENDING`，与最新 spec 的“恢复原业务状态 / 强制核对恢复原始状态”不一致。
  - 导入流程仍是 mock 预览，未体现完整校验、标准化、覆盖逻辑。
- `prototype/reconciliation/summary.html`
  - `makeGroupKey()` 当前包含 `feePeriod`，与主 spec 的匹配主键不一致。
  - `executeMatchingForRule()` 当前是简化算法，只能作为展示参考，不能直接视为正式实现逻辑。
  - 汇总页统计与明细页结果未绑定同一套匹配引擎。

## 开工前统一约束

- [ ] 所有研发、测试先以 `type-month-matching.md` 为最终口径，不再以旧原型行为反推规则。
- [ ] 当前现行原型只认 `summary.html` 和 `unified.html`，不再引用 `obsolete/index.html`。
- [ ] 本期范围内不补接口文档、不补数据落库设计，避免研发在错误层面分散精力。
- [ ] 汇总页和明细页必须共用同一套匹配判定逻辑，不允许各自维护不同版本的“简化规则”。

## 建议分工

- **前端研发 A**
  - 负责明细页匹配引擎、待确认抽屉、差异详情、强制核对、取消恢复
- **前端研发 B**
  - 负责导入流程、归档付款、汇总页统计、批量操作、页面间口径对齐
- **测试**
  - 负责样例矩阵、导入校验矩阵、状态机回归矩阵、汇总页/明细页一致性回归
- **产品 / 业务验收**
  - 只看主 spec、PRD、现行原型，不再单独解释旧探索版本

## Task 1: 锁定统一领域模型与状态语义

**Files**
- Reference: `docs/superpowers/specs/reconciliation/type-month-matching.md`
- Reference: `docs/superpowers/prd/reconciliation/reconciliation.md`
- Reference: `prototype/reconciliation/unified.html`
- Reference: `prototype/reconciliation/summary.html`

- [ ] 统一以下常量口径，不允许页面各自重命名或改义：
  - `MATCH_STATUS = UNMATCHED / MATCHED / PENDING / DIFF / PAID`
  - `BILL_TYPES = huijiao / bujiao / tiaoji`
  - `DIFF_TYPE = system_more / ledger_more / amount_mismatch`
- [ ] 锁定系统侧最小字段集：
  - `id / idCard / insuranceType / feeType / amount / billingMonth / payableMonth / feePeriod / matchStatus / matchedLedgerId / diffType / diffAmount / archived / archiveBatchId / forcePending / forceMatched`
- [ ] 锁定台账侧最小字段集：
  - `id / idCard / insuranceType / amount / billingMonth / feeTypeInferred / payableMonthInferred / matchStatus / matchedSystemId / diffType / diffAmount / archived / archiveBatchId`
- [ ] 锁定取消核对规则：
  - 普通自动匹配 / 人工确认：清空回填字段，系统侧按原业务类型恢复
  - 强制核对：从 `_originalMatchStatus / _originalDiffType / _originalDiffAmount / _originalPayableMonth` 恢复
- [ ] 锁定归档 / 已付款规则：
  - `archived` 是独立标记，不是 `matchStatus`
  - 已归档保留 `MATCHED`
  - 已付款转 `PAID`

**完成标准**
- 研发、测试、产品对字段语义只保留一套解释
- 任何任务单、联调单、测试单不再出现“取消后统一恢复 PENDING”“汇总页与明细页口径不同”这类歧义

**测试关注点**
- 状态定义与按钮权限是否一致
- 台账侧是否始终没有“强制核对”入口

## Task 2: 落明细页正式匹配引擎

**Files**
- Modify: `prototype/reconciliation/unified.html`
- Reference: `docs/superpowers/specs/reconciliation/type-month-matching.md`

- [ ] 将 `executeMatching()` 从“直接按现有数组分组”重构为以下固定流程：
  - `buildSystemCandidateSet(pageContext, systemRecords)`
  - `buildLedgerCandidateSet(pageContext, ledgerRecords)`
  - `normalizeMatchingRecords(records, side)`
  - `getEffectivePayableMonth(record, pageContext, side)`
  - `groupByMainKey(records)`
  - `bucketByAmount(group)`
  - `applyAutoMatch() / applyPending() / applyAmountMismatch() / applySingleSideResidual()`
  - `calculateStats()`
- [ ] 系统侧候选集必须落实主 spec 的取数范围：
  - 汇缴：`payableMonth = 当前账单月份`
  - 自动拆分补缴：`feePeriod = 当前账单月份` 且 `payableMonth` 为空
  - 单补缴 / 调基 / 政策调整：`payableMonth` 为空
- [ ] 台账侧候选集必须只取当前 `参保主体 + 参保规则 + 账单月份` 的有效批次
- [ ] 正式分组 key 改为：
  - `身份证 + 险种 + 有效应缴月份`
- [ ] 金额桶执行顺序必须改为：
  - Pass 1：唯一 1:1 自动匹配
  - Pass 2：同金额多笔或 `forcePending` 进入 `PENDING`
  - Pass 3：识别同成员 + 同险种 + 当前账单月份 + 同费款所属期下合计金额相等的组合 `PENDING` 组，覆盖一对多、多对一、多对多
  - Pass 4：处理单边残留与 `amount_mismatch`
- [ ] 差异判定必须落齐：
  - 汇缴系统多：`DIFF(system_more)`
  - 补缴 / 调基补差系统多：`UNMATCHED`
  - 台账多：`DIFF(ledger_more)`
  - 剩余无法闭合：`DIFF(amount_mismatch)`

**完成标准**
- 明细页的自动匹配结果可直接覆盖 `S1-S11`
- 匹配结果里允许同一主分组同时出现 `MATCHED + PENDING + DIFF`
- `amount_mismatch` 不会吞掉已可自动匹配的记录

**测试关注点**
- `S1` 唯一自动匹配
- `S2-S3` 同金额歧义进入 `PENDING`
- `S4-S7` 三类差异分流
- `S8-S9` 金额不一致与“部分成功、部分差异”
- `S10-S11` forcePending 与无台账执行

## Task 3: 完成明细页人工处理闭环

**Files**
- Modify: `prototype/reconciliation/unified.html`
- Reference: `docs/superpowers/prd/reconciliation/reconciliation.md`

- [ ] 改造 `confirmPendingPairing()`：
  - 人工确认成功后，系统侧与台账侧一起转 `MATCHED`
  - 同步回填 `payableMonth / matchedLedgerId / matchedSystemId / feeTypeInferred / payableMonthInferred`
- [ ] 改造 `openPairingDrawer()` / `confirmPairing()`：
  - 允许一对多、多对一、多对多场景人工映射
  - 阻止“两条系统记录映射到同一条台账”
  - 允许同成员 + 同险种 + 当前账单月份 + 同费款所属期下选择系统侧与台账侧明细做组合确认
  - 组合确认前必须校验系统合计金额 = 台账合计金额
  - 组合确认成功后生成同一 `manualMatchGroupId`，取消时整组恢复
- [ ] 改造 `showNewDetail()` / `confirmFromDrawer()`：
  - `DIFF` 场景可查看候选台账
  - “最接近金额”只用于展示，不直接落自动匹配
- [ ] 改造 `forceMatch()`：
  - 仅系统侧可执行
  - 保留 `_original*` 恢复字段
  - 强制后系统侧转 `MATCHED`，台账侧不自动转 `MATCHED`
- [ ] 改造 `cancelMatch()` / `doCancelMatch()`：
  - 已归档、已付款不可取消
  - 普通匹配取消后恢复原业务状态
  - 强制核对取消后从 `_original*` 恢复
- [ ] 批量操作遵循当前 Tab 可见记录：
  - `systemBatchConfirm()`
  - `systemBatchCancel()`
  - `systemBatchForceMatch()`
  - `ledgerBatchConfirm()`
  - `ledgerBatchCancel()`

**完成标准**
- `S12-S15` 可完整覆盖
- 台账侧无任何强制核对入口
- 取消核对后，字段恢复与状态恢复一致，不产生脏关联

**测试关注点**
- 强制核对只改系统侧
- 普通取消与强制取消两条链路分开验证
- 归档后、付款后不可取消

## Task 4: 补齐导入与输入质量闭环

**Files**
- Modify: `prototype/reconciliation/unified.html`
- Modify: `prototype/reconciliation/summary.html`
- Reference: `docs/superpowers/specs/reconciliation/ledger-import.md`

- [ ] 导入流程统一为“两步”：
  - Step 1：选择上下文参数
  - Step 2：上传、预览、确认导入
- [ ] 导入前置校验必须覆盖：
  - 未选月份
  - 文件格式不支持
  - 空文件
  - 必填字段为空
  - 金额格式错误
  - 应缴月份格式错误
  - 险种无法标准化
- [ ] 导入标准化必须落实：
  - 身份证去空格、X 大写
  - 险种别名映射
  - 应缴月份统一 `YYYY-MM`
  - 金额四舍五入到分
- [ ] 覆盖判重规则：
  - 同一 `参保主体 + 参保规则 + 账单月份` 只保留一份有效台账
  - 重复导入时必须走“是否覆盖”确认
- [ ] 导入预览必须包含：
  - 成功条数
  - 错误条数
  - 错误行原因
  - 前若干条成功预览

**完成标准**
- 导入后形成可直接进入匹配引擎的标准输入
- 测试可仅通过导入预览就快速判断“是数据问题还是匹配问题”

**测试关注点**
- 同一文件内重复主键是否只提示不擅自合并
- 输入质量问题是否会造成假性 `ledger_more`

## Task 5: 完成归档、批次、付款闭环

**Files**
- Modify: `prototype/reconciliation/unified.html`
- Reference: `docs/superpowers/prd/reconciliation/reconciliation.md`

- [ ] `archiveResults()` 只归档 `MATCHED + archived=false`
- [ ] 有 `PENDING / DIFF` 时允许继续，但必须先确认“只归档已核对记录”
- [ ] `doArchive()` 必须同步系统侧与已关联台账侧：
  - `archived = true`
  - `archiveBatchId`
  - `archivedAt`
- [ ] `openArchiveBatchDrawer()` / `viewArchiveBatch()` / `updateArchiveBatchFilters()` 形成批次查看与筛选闭环
- [ ] `showPaymentConfirm()` / `executePayment()` 只从归档批次发起付款
- [ ] 付款后系统侧和已关联台账侧一起转 `PAID`

**完成标准**
- 可多次归档同一账单月份
- 已付款批次不能重复付款
- 批次查看、批次筛选、付款状态展示一致

**测试关注点**
- 无待归档记录提示
- 已全部付款批次再次付款拦截
- 批次筛选是否同时影响系统侧与台账侧

## Task 6: 让汇总页与明细页共用同一口径

**Files**
- Modify: `prototype/reconciliation/summary.html`
- Reference: `prototype/reconciliation/unified.html`
- Reference: `docs/superpowers/specs/reconciliation/type-month-matching.md`

- [ ] 重写 `summary.html` 中的 `makeGroupKey()` 与 `executeMatchingForRule()`：
  - 不再使用当前 `billingMonth + feePeriod` 的简化 key
  - 不再只对 `huijiao` 做特殊处理
  - 对账统计必须与明细页匹配引擎同口径
- [ ] 统一汇总页统计字段来源：
  - 系统侧已核对 / 差异 / 已归档
  - 台账侧总计 / 已核对 / 差异 / 待确认
- [ ] `batchReconcile()` 与 `groupReconcile()` 要以正式匹配结果回填规则统计，不允许继续使用“简化总数”
- [ ] `batchArchive()` 只允许对符合条件的规则触发
- [ ] `navigateToDetail()` / `groupDetail()` 跳转时传递稳定上下文
- [ ] 汇总页左上角月份为账单月份上下文，不作为主体 / 规则清单过滤条件
- [ ] 切换账单月份后，汇总页主体 / 规则清单保持不变，表格账单月份列展示当前账单月份
- [ ] 汇总页和明细页导入台账时，台账月份均继承当前账单月份且不可修改

**完成标准**
- 同一条规则在汇总页看到的状态、金额、差异数，与进入明细页后的结果一致
- 汇总页不再是“演示版统计”，而是正式结果的聚合视图
- 子行详情与分组详情进入明细页时，URL 均包含当前 `month`

**测试关注点**
- 同一规则在两页的 matched / pending / diff 数量一致
- 同一规则在两页的金额合计一致
- 批量对账后汇总页颜色状态与明细页状态一致

## Task 7: 测试开工包

**Files**
- Reference: `docs/superpowers/specs/reconciliation/type-month-matching.md`
- Reference: `docs/superpowers/prd/reconciliation/reconciliation.md`
- Reference: `docs/superpowers/specs/reconciliation/ledger-import.md`

- [ ] 以主 spec 的 `S1-S15` 样例矩阵作为最小回归集
- [ ] 额外补三类测试分组：
  - 导入测试组
  - 归档 / 付款测试组
  - 汇总页 / 明细页一致性测试组
  - 账单月份上下文回归测试组
- [ ] 每条测试用例至少包含：
  - 场景编号
  - 前置数据
  - 页面上下文
  - 执行动作
  - 预期状态
  - 预期回填字段
  - 预期批次 / 付款影响
- [ ] 测试结论输出时，必须能回答这 4 个问题：
  - 算法判定是否正确
  - 字段回填是否正确
  - 页面交互是否正确
  - 汇总页与明细页是否一致
- [ ] 账单月份上下文回归至少覆盖：
  - 切换账单月份后汇总主体 / 规则数量不变
  - 汇总页账单月份列变为当前选择月份
  - 子行详情和分组详情 URL 都包含当前 `month`
  - 明细页标题 / 副标题展示当前账单月份
  - 导入台账月份锁定且不可修改
  - 强制核对后系统侧 `payableMonth` 等于当前账单月份

**完成标准**
- 测试团队不依赖额外口头说明即可开写用例
- 任何 bug 都能定位到“输入问题 / 匹配判定问题 / 状态流转问题 / 页面展示问题”中的一个层级

## 推荐实施顺序

1. Task 1：统一字段和状态语义
2. Task 2：先把明细页匹配引擎做对
3. Task 3：把人工处理和强制/取消闭环做完整
4. Task 4：补导入质量与覆盖逻辑
5. Task 5：补归档、批次、付款闭环
6. Task 6：最后让汇总页改成正式聚合视图
7. Task 7：测试按 `S1-S15 + 导入 + 归档付款 + 跨页一致性` 回归

## 研发开工时的必看顺序

1. `docs/superpowers/specs/reconciliation/type-month-matching.md`
2. `docs/superpowers/prd/reconciliation/reconciliation.md`
3. `docs/superpowers/specs/reconciliation/ledger-import.md`
4. `prototype/reconciliation/unified.html`
5. `prototype/reconciliation/summary.html`
6. `docs/superpowers/plans/reconciliation/v1-complete-plan.md`

## 交付判断标准

- 明细页匹配结果已与主 spec 完整对齐
- 导入输入质量与匹配输出之间的边界清晰
- 取消核对、强制核对、归档、付款状态机全部闭环
- 汇总页不再维护独立“简化算法”
- 测试可仅依据现有文档和样例矩阵直接开工
