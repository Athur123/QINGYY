# 社保对账复核 PRD（v2.0 — 生产交付版）

## Problem Statement

青阳云HRO系统根据员工参保异动自动生成应缴费用（汇缴/补缴/调基补差），但补缴和补差类型缺少应缴月份。社保局台账（Excel导入）记录了应缴月份，但不区分费用类型。社保专员需将系统侧费用与台账账单逐笔核对，确保缴费金额一致后将结果归档用于付款。

核心矛盾：**系统有费用类型无应缴月份，台账有应缴月份无费用类型**。双方共同拥有身份证号、险种、金额。同一员工同一险种可能产生多笔费用（1笔汇缴 + N笔补缴 + M笔调基补差），金额相同的记录无法自动区分。

## Solution

两层结构对账系统：汇总列表页（按参保主体分组概览） + 明细核对页（Tab分离逐笔核对）。核心流程：导入台账 → 自动匹配 → 人工确认待核记录 → 处理差异 → 归档批次 → 付款。

## 系统架构

### 数据流

```
员工异动记录 ──→ 系统侧账单生成 ──→ systemRecords[]
                                        │
社保局 Excel ──→ 导入标准化    ──→ ledgerRecords[]
                                        │
                    ┌───────────────────┘
                    ▼
            executeMatching()
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    MATCHED     PENDING       DIFF
        │           │           │
        │      确认核对    强制核对
        │           │           │
        └───────────┴───────────┘
                    │
                    ▼
              archiveResults()
                    │
              archiveBatches[]
                    │
                    ▼
              doPayment() → PAID
```

### 模块划分

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| 台账导入 | Excel解析+标准化+判重 | .xlsx文件 | ledgerRecords[] |
| 匹配引擎 | 按分组精确金额配对 | systemRecords+ledgerRecords | matchingResults |
| 明细核对 | Tab表格渲染+筛选+批量 | matchingResults | 用户确认/取消/强制核对 |
| 配对确认 | 同金额多笔人工确认 | PENDING记录 | MATCHED记录 |
| 差异处理 | 金额不一致分析+台账选择器 | DIFF记录 | MATCHED或DIFF |
| 归档批次 | 归档+批次管理+筛选 | MATCHED记录 | archiveBatches[] |
| 付款申请 | 批次付款+状态变更 | 归档批次 | PAID记录 |
| 汇总列表 | 跨规则聚合统计 | DEMO_RULES | 表格+批量操作 |

## User Stories

### 台账导入（7条）
1. 作为社保专员，我想导入社保局台账Excel(.xlsx/.xls)，选择参保主体+规则+月份后上传，以便与系统费用比对
2. 导入前必须先选择台账月份，否则禁止上传文件
3. 上传后展示预览：成功条数、错误条数、错误行详情（行号+原因），以便修正后重新导入
4. 导入时自动标准化：身份证（去空格、X大写）、险种（别名→标准名，含大额医疗）、金额（保留2位小数）、日期（统一YYYY-MM）
5. 重复导入同一参保主体+规则+月份的台账时弹窗提示覆盖
6. 多次导入不同月份的数据应累加而非覆盖
7. 导入空文件或格式不支持的提示错误

### 对账匹配（8条）
8. 点击"开始对账"后自动执行金额配对：按`身份证|险种|应缴月份`分组，组内同金额精确匹配
9. 无需导入台账也可执行——汇缴→DIFF(system_more)，补缴/调基补差→UNMATCHED
10. 唯一配对自动MATCHED：系统回填payableMonth，台账回填feeTypeInferred
11. 多笔同金额→PENDING：提供智能推荐（按列表顺序配对，默认勾选）
12. 在配对抽屉中可手动下拉调整系统侧与台账侧的映射关系，然后确认
13. 系统有台账无：汇缴→DIFF(system_more)（须核查）；补缴/调基补差→UNMATCHED（可后续月份匹配）
14. 台账有系统无→DIFF(ledger_more)
15. 双方都有但金额不一致→DIFF(amount_mismatch)，记录最接近金额的差额

### 强制核对（5条）
16. DIFF/UNMATCHED系统侧记录可通过"强制核对"直接标记MATCHED，跳过台账匹配
17. 台账侧**不允许**强制核对——必须匹配系统记录
18. 强制核对前弹窗确认，展示受影响记录明细（姓名/身份证/险种/金额）
19. 强制核对后可取消，从_original字段恢复原始DIFF/UNMATCHED
20. 支持底部批量选中→批量强制核对（仅对选中的DIFF/UNMATCHED生效）

### 明细核对（5条）
21. Tab分离系统侧/台账侧，sticky吸顶，两侧各自独立维护筛选状态
22. 筛选：核对状态（全部/已核对/待确认/未匹配/差异，附金额统计）+ 费用类型（全部/汇缴/补缴/调基补差）+ 归档批次下拉
23. 已核对记录两侧同时展示，系统侧台账金额列带↔Txxx，台账侧系统金额列带↔Sxxx
24. PENDING批量确认核对；DIFF/UNMATCHED批量操作
25. DIFF行"详情"打开右侧抽屉：金额对比(系统vs台账，单位/个人拆分)+差异分析(可能原因分类)+底部台账选择器手动匹配

### 归档批次（10条）
26-35. （保持不变：归档→创建批次→多次归档→批次抽屉→查看此批次→筛选→已归档规则）

### 付款申请（8条）
36-43. （保持不变：申请付款→确认弹窗→PAID状态→行蓝色→不可取消）

### 汇总列表（7条）
44-50. （保持不变：二级表头→分组→颜色编码→批量操作→导入→已归档→信息栏）

## 系统侧账单明细生成逻辑

系统侧账单明细来源于员工参保异动记录，按费用类型分为三类：

### 汇缴
- 来源：异动类型为「增员」的异动明细（自动拆分的补缴除外）
- 应缴月份 = 异动生效月份 = 费款所属期，不为空
- 筛选：所选对账复核月份 = 增员异动应缴月份

### 补缴
- 来源一（增员自动拆分）：应缴月份默认为空。所选月份与费款所属期一致时自动获取
- 来源二（单补缴异动）：应缴月份默认为空。系统获取所有补缴且应缴月份为空的记录
- 费款所属期 = 补缴月份，≠ 应缴月份
- 展示：按成员+险种+补缴月份逐条展示

### 调基补差
- 来源一（调基）：生效月份产生的补差费用，应缴月份默认为空。任意月份自动获取
- 来源二（政策调整）：生效月份产生的补差费用，应缴月份默认为空。任意月份自动获取
- 费款所属期 = 调基补差月份，≠ 应缴月份
- 展示：按成员+险种+费款所属期逐条展示，每一笔独立核对（不合并）

### 字段关系表

| 字段 | 汇缴 | 补缴 | 调基补差 |
|------|------|------|---------|
| 应缴月份(payableMonth) | =费款所属期 | 默认空→匹配后回填 | 默认空→匹配后回填 |
| 费款所属期(feePeriod) | =应缴月份 | =补缴月份 | =补差月份 |
| 数据筛选 | 所选月=应缴月 | 费款期=所选月 或 应缴月为空 | 应缴月为空(全量) |

## Data Model

### 系统侧费用记录

```
{
  id: string,              // 主键 S001-Sxxx
  employee_name: string,   // 员工姓名
  id_card: string,         // 18位身份证号
  insurance_type: string,  // 养老/医疗/失业/工伤/生育/大额医疗/公积金
  billing_month: string,   // 对账复核所选账单月份 YYYY-MM
  fee_type: enum,          // huijiao(汇缴)/bujiao(补缴)/tiaoji(调基补差)
  fee_period: string,      // 费款所属期 YYYY-MM
  payable_month: string|null, // 应缴月份。汇缴有值；补缴/调基初始null，匹配后回填
  amount_company: number,  // 单位金额
  amount_personal: number, // 个人金额
  amount: number,          // 合计 = company + personal
  match_status: enum,      // UNMATCHED/MATCHED/PENDING/DIFF/PAID
  matched_ledger_id: string|null,
  diff_type: enum|null,    // system_more/ledger_more/amount_mismatch
  diff_amount: number|null,// 正数系统多，负数台账多
  archived: boolean,       // 是否归档(独立标记，非match_status值)
  archived_at: string|null,
  archive_batch_id: string|null,
  force_matched: boolean,  // 是否强制核对
  remark: string|null,
}
```

### 台账侧记录

```
{
  id: string,              // 主键 T001-Txxx
  employee_name, id_card, insurance_type,
  billing_month: string,   // 台账应缴月份
  fee_period: string|null, // 费款所属期
  amount: number,
  fee_type_inferred: string|null, // 匹配后从系统侧回填
  match_status: enum,      // 同系统侧
  matched_system_id: string|null,
  diff_type, diff_amount,
  archived, archived_at, archive_batch_id,
  import_batch_id: string,
  insurance_subject: string, // 参保主体
  insurance_rule: string,    // 参保规则
  imported_at: string,
  imported_by: string,
}
```

### 归档批次 + 对账结果

```
archiveBatch: { id, label, billing_month, created_at, record_count, total_amount }
matchingResults: { matched[], pending[], diffs[], executed: bool }
```

## 核对状态机

```
UNMATCHED ──匹配──→ MATCHED / PENDING / DIFF
PENDING ──确认──→ MATCHED
DIFF ──强制核对──→ MATCHED (仅系统侧)
MATCHED ──取消──→ PENDING (已归档不可取消)
MATCHED ──归档──→ archived=true + archiveBatchId (matchStatus保持MATCHED)
MATCHED(archived) ──付款──→ PAID (archived+archiveBatchId保留)
```

**关键约束**：
- archived是独立布尔字段，不是matchStatus值
- 已归档记录不可取消核对，操作列显示"详情"
- 已付款记录不可取消核对/归档，操作列显示"详情"
- 台账侧无强制核对入口
- PAID记录与MATCHED在"已核对"筛选下一起展示

## 匹配算法（完整规格）

### 数据准备
- 身份证标准化：去空格、X大写、trim
- 险种标准化：通过INSURANCE_TYPE_ALIAS映射，无法识别标记"未知"
- 金额标准化：保留2位小数四舍五入
- 分组key：`idCard|insuranceType|billingMonth`

### 组内匹配规则
1. 统计每个金额的出现次数
2. 系统1:台账1 → 自动MATCHED，双向回填
3. 系统多:台账多(同金额) → PENDING
4. 系统有台账无 → 汇缴DIFF(system_more) / 补缴调基UNMATCHED
5. 台账有系统无 → DIFF(ledger_more)
6. 金额不一致 → DIFF(amount_mismatch)

### forcePending机制
原型演示用标记。forcePending=true的记录即使1:1金额一致也进入PENDING。后端对应requires_manual_review字段。Post-processing修正被分到DIFF的forcePending记录。

### 险种别名映射（7+1种）
养老(基本养老/养老保险/基本养老保险)、医疗(基本医疗/医疗保险/基本医疗保险)、失业(失业保险/失业保险金)、工伤(工伤保险/工伤保险金)、生育(生育保险/生育保险金)、大额医疗(大额医疗保险/大病医疗)、公积金(住房公积金/住房公积)

## 导入流程（完整规格）

1. 选择导入参数（参保主体/参保规则/台账月份，月份必选）
2. 上传Excel（.xlsx/.xls，拖拽或点击，drop-zone区域）
3. 格式校验：必填列检查(姓名/身份证/险种/应缴月份/金额) + 身份证格式 + 险种映射 + 金额格式
4. 判重：参保主体+规则+月份是否已有台账 → 提示覆盖
5. 导入预览：成功/失败条数 + 错误行详情 + 前10条预览表格
6. 确认导入：写入ledgerRecords，累加不覆盖

## 交互规范（完整）

### 明细核对页布局
```
面包屑 ← 对账复核 / 规则名    标题
工具栏（6按钮）：导入/对账/归档/归档记录/导出/标注
Tab栏（sticky吸顶）：系统侧(计数) | 台账侧(计数)
筛选栏（3组）：核对状态(5按钮+金额) | 费用类型(4按钮) | 归档批次(下拉)
表格（12列×N行）
批量操作栏（4按钮 + 总数/页码）
```

### 表格12列完整规格（系统侧）
| # | 列名 | 格式 | 说明 |
|---|------|------|------|
| 1 | ☑ | checkbox | 选中参与批量操作 |
| 2 | 核对状态 | badge+圆点 | UNMATCHED灰/MATCHED绿/PENDING黄/DIFF红/已归档灰/PAID蓝 |
| 3 | 费用类型 | badge | 汇缴蓝/补缴紫/调基补差青 |
| 4 | 姓名 | strong加粗 | |
| 5 | 身份证 | 脱敏 | 前6+****+后4 |
| 6 | 险种 | 文本 | |
| 7 | 应缴月份 | payableMonth | 汇缴有值；补缴/调基初始"—"→匹配后回填 |
| 8 | 费款所属期 | feePeriod | 始终有值 |
| 9 | 系统金额 | ¥格式化 | =单位+个人 |
| 10 | 台账金额 | ¥+↔Txxx | 已核对显示跨引用；其他"—" |
| 11 | 差异 | ±¥红色 | +系统多/-台账多 |
| 12 | 操作 | 按钮 | 按状态映射(详情/确认核对/取消/强制核对) |

### 表格12列（台账侧差异）
- 列6：台账金额 | 列7：系统金额+↔Sxxx | 费用类型列未核对时"—"
- **操作列无强制核对按钮**

### 行颜色
| 状态 | 背景色 |
|------|--------|
| MATCHED未归档 | #F0FDF4(绿) |
| PENDING | #FEFCE8(黄) |
| DIFF | #FEF2F2(红) |
| 已归档 | #F1F5F9(灰)+opacity.7 |
| PAID | #EFF6FF(蓝) |

### 操作列按钮映射
| 记录状态 | 系统侧按钮 | 台账侧按钮 |
|---------|-----------|-----------|
| UNMATCHED | 强制核对 | 详情 |
| PENDING | 确认核对 | 确认核对 |
| MATCHED未归档 | 取消 | 取消 |
| MATCHED已归档 | 详情 | 详情 |
| DIFF | 强制核对 | 详情 |
| PAID | 详情 | 详情 |

### 交互组件（6个+1个通用确认）

**配对确认抽屉**（right 600px）
- 触发：PENDING行"确认核对"
- 内容：信息栏 + 智能推荐区(按列表顺序,默认勾选) + 手动调整区(系统↔台账下拉映射) + [取消][确认全部配对]
- 冲突检测：两系统记录不能选同一台账

**差异详情抽屉**（right 520px）
- 触发：DIFF行"详情"
- 内容：基本信息区 + 金额对比区(系统vs台账,单位/个人) + 差异分析区(原因分类) + [关闭][确认核对]
- "确认核对"切换为台账选择器：按身份证+险种筛选候选 → 单选匹配

**强制核对确认弹窗**（center 480px）
- 触发：DIFF/UNMATCHED行"强制核对"
- 内容：红色警告 + 规则说明 + 记录列表 + [取消][确认强制核对(红)]
- 仅系统侧有入口

**导入台账对话框**（center 520px，两步）
- Step1：月份(必选)+主体+规则 + drop-zone上传(.xlsx/.xls)
- Step2：预览结果(成功/失败+错误详情+前10条预览表格)
- 判重提示

**归档批次抽屉**（right 560px）
- 触发：工具栏"📦归档记录"
- 内容：批次列表(批次/月份/记录数/金额/时间/查看此批次+申请付款)
- "查看此批次"：关闭抽屉→筛选器设为该批次→表格过滤
- "申请付款"：弹出付款确认弹窗

**付款确认弹窗**（center 480px）
- 触发：批次行"申请付款"
- 内容：批次信息+记录数+金额+[取消][确认付款]
- 确认后doPayment()将批次内MATCHED+archived→PAID

**通用确认弹窗**（center 400px）
- showConfirmDialog(title,text,callback)
- 归档确认、判重覆盖等复用

### 批量操作栏
| 按钮 | 样式 | 启用条件 | 行为 |
|------|------|---------|------|
| 全选 | secondary | 始终 | 选中/取消当前Tab所有可见行 |
| 确认所选 | primary | 选中含PENDING | 批量确认PENDING→MATCHED |
| 取消确认 | secondary | 选中含MATCHED未归档 | 批量取消→PENDING |
| 强制核对 | danger | 选中含DIFF/UNMATCHED(仅系统侧) | 排除MATCHED/PENDING后执行 |

### 键盘交互
Escape关闭链：导入对话框 → 确认弹窗 → 配对抽屉 → 详情抽屉 → 强制核对弹窗 → 付款弹窗 → 归档批次抽屉 → 标注模式

## Edge Cases（完整）

| # | 场景 | 预期行为 |
|---|------|---------|
| 1 | 同一台账重复导入 | 参保主体+规则+月份判重，弹窗覆盖确认 |
| 2 | 核对成功取消 | 恢复PENDING，系统清空payableMonth，台账清空feeTypeInferred |
| 3 | 已归档取消核对 | doCancelMatch拦截，toast"已归档记录不可取消核对" |
| 4 | 已付款取消核对 | 操作列仅"详情"，无取消按钮 |
| 5 | 强制核对后取消 | 从_originalMatchStatus/_originalDiffType/_originalDiffAmount恢复 |
| 6 | 身份证格式不一致 | 导入时标准化(去空格、X大写) |
| 7 | 险种名称不一致 | 映射表标准化，无法识别→"未知" |
| 8 | 台账无有效数据 | 提示"文件中无有效数据" |
| 9 | 必填字段为空 | 标记为格式错误行，跳过该行 |
| 10 | 无待归档记录 | toast"无待归档记录"，不创建批次 |
| 11 | 只有PENDING/DIFF无MATCHED | toast"无已核对记录可归档" |
| 12 | 台账侧强制核对尝试 | 按钮不存在 |
| 13 | 补缴/调基无台账 | UNMATCHED(非DIFF)，可在后续月份匹配 |
| 14 | 归档批次全部付款后 | 再次"申请付款"→toast"该批次无可付款记录" |
| 15 | 导出空数据 | 提示无数据可导出 |
| 16 | 大量数据(>1000条) | 显示进度条，分批匹配 |
| 17 | Excel格式不支持 | 拒绝导入，提示使用.xlsx/.xls |
| 18 | 未选台账月份上传 | 提示"请先选择台账月份" |
| 19 | 两次系统记录选同一台账 | 配对抽屉冲突检测+错误提示 |

## Error Handling（完整）

| 错误 | 用户提示 | 系统行为 |
|------|---------|---------|
| Excel格式不支持 | "请使用.xlsx或.xls文件" | 拒绝导入 |
| 身份证校验失败 | "第N行身份证格式不正确" | 标记跳过 |
| 金额格式错误 | "第N行金额格式不正确" | 标记跳过 |
| 应缴月份格式错误 | "第N行应缴月份格式不正确(YYYY-MM)" | 标记跳过 |
| 必填列缺失 | "第N行缺少必填字段：XX" | 标记跳过 |
| 未选月份上传 | "请先选择台账月份" | 阻止上传 |
| 判重冲突 | "已有台账，是否覆盖？" | 确认弹窗 |
| 匹配异常 | "对账过程发生错误，请重试" | 回滚状态 |
| 网络中断导入 | "导入失败，请重试" | 保持原数据 |

## Testing Strategy（完整）

### 测试原则
- 验证外部行为，不测试内部实现
- 每个用户故事至少一个正向+一个异常测试
- 状态机每条转换路径必须有测试
- 边界条件必须覆盖

### 功能测试（20场景）

**台账导入(5)**：正常导入17条 / 空文件提示 / 缺列跳过 / 判重覆盖 / 多月累加

**对账匹配(4)**：全1:1自动MATCHED / forcePending→PENDING / 无台账→DIFF+UNMATCHED / 台账独有→DIFF

**强制核对(3)**：DIFF→强制核对→MATCHED→取消→恢复 / 台账侧无按钮 / 批量仅DIFF/UNMATCHED参与

**归档批次(4)**：无差异归档→第1批 / DIFF存在→确认弹窗→仅归档MATCHED / 新增记录→第2批 / 空归档toast

**付款(2)**：归档→付款→PAID / 全部付款→无可付款提示

**汇总列表(2)**：展开收起分组 / 已归档规则灰行禁用

### 状态机测试（覆盖所有转换路径）
UNMATCHED→MATCHED/PENDING/DIFF | PENDING→MATCHED | DIFF→MATCHED(强制) | MATCHED→PENDING(取消) | MATCHED→archived | MATCHED(archived)→PAID | 已归档取消拦截 | 已付款取消拦截

### 数据一致性测试
- 归档前后systemRecords.archived计数一致
- 批次totalAmount = Σ该批次记录amount
- 取消核对后payableMonth/feeTypeInferred清空
- 强制核对取消后_original字段恢复
- PAID后archiveBatchId保留

### UI验证
- CSS无404错误
- 5种行颜色正确渲染
- 6种状态badge正确显示
- 抽屉/弹窗打开关闭动画
- sticky Tab吸顶
- 筛选后金额统计更新

### 测试数据
- 系统侧23条（汇缴14+补缴3+调基补差3+forcePending 7）
- 台账侧26条（覆盖全部匹配/差异场景）
- 需覆盖：全部MATCHED/全部DIFF/混合/空台账 四种场景

## 技术规范

### 浏览器支持
Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### 性能要求
- 首屏渲染 < 1s
- 匹配引擎（500条以内）< 200ms
- 表格渲染（500行）< 300ms
- 导入Excel（1000条）< 2s
- 大量数据（>1000）显示进度条

### 可访问性
- 按钮可键盘操作（Tab/Enter）
- 焦点环可见（outline）
- 颜色非唯一指示方式（状态同时有文字+badge+颜色）
- 表格使用语义化HTML（thead/tbody/th/td）

### 外部依赖
- SheetJS (xlsx CDN)：Excel解析
- Google Fonts：Plus Jakarta Sans + Inter
- 无其他运行时依赖

### 生产目标技术栈
Vue 3 + TypeScript + Vite (Composition API)，当前原型为纯HTML/CSS/JS

## Out of Scope

- 后端API/数据库实现
- 用户权限控制和操作审计日志
- 移动端响应式适配
- 多语言/国际化
- 与社保局系统实时对接
- 数据导出为Excel

## Reference

| 资源 | 路径 |
|------|------|
| 明细核对原型（v1完整版,含PAID） | `prototype/reconciliation/unified.html` |
| 汇总列表原型 | `prototype/reconciliation/summary.html` |
| 设计文档（含账单生成逻辑） | `docs/superpowers/specs/reconciliation/type-month-matching.md` |
| 实现计划（v1整合版） | `docs/superpowers/plans/reconciliation/v1-complete-plan.md` |
| 账单生成逻辑源文件 | `source/应付核对系统账单明细取值逻辑.md` |
| 原型标注（47条） | 嵌入在unified.html中（💬标注按钮） |
