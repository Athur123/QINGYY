# 参保档案字段采集配置设计

## 1. 需求概述

不同地区的参保规则在发起异动（增员、减员、调基、补缴）时，需要用户提交不同的附加信息字段（如合同附件、合同日期、身份证附件、户籍等）。字段的需求因参保规则和操作类型而异，包括：

- **字段集合不同** — 增员需要的字段与减员不同
- **必填要求不同** — 同一字段在不同规则中必填状态不同
- **字段类型多样** — 文本、数值、附件、照片、日期、下拉选择等
- **值来源不同** — 部分字段从员工档案自动获取，部分需手动填写

本设计实现**配置模型**（字段定义、配置界面），运行时采集引擎在后续独立 spec 中实现。

## 2. 决策汇总

| 决策项 | 选择 |
|--------|------|
| 方案选择 | 独立关联表（非 JSON 扩展、非模板化） |
| 字段管理 | 全局字段字典，参保规则引用字典项 |
| 配置粒度 | 按操作类型（增/减/调/补）独立配置 |
| UI 位置 | 嵌入现有"社保参保规则配置"页面，新增第四项 Tab |
| 自动填充 | 只读展示，不可修改 |

## 3. 数据模型

### 3.1 全局字段字典 (`field_dict`)

定义系统中所有可采集字段的元数据，供所有参保规则复用。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| field_code | VARCHAR(64) UNIQUE | 字段编码，如 `contract_attachment` |
| field_name | VARCHAR(128) | 字段名称，如"合同附件" |
| field_type | ENUM | 字段类型：`text`, `number`, `date`, `file`, `photo`, `select` |
| value_source | ENUM | 值来源：`AUTO`（员工档案自动获取）/ `MANUAL`（手动填写） |
| auto_source_path | VARCHAR(256) | 自动获取路径，如 `employee.contract.startDate`（仅 AUTO 类型） |
| options | JSON | select 类型的选项列表，如 `[{"label":"城镇","value":"urban"}]` |
| description | VARCHAR(512) | 字段说明 |

### 3.2 采集配置头 (`field_collection_config`)

关联参保规则与操作类型，每个规则的每种操作对应一条记录。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| rule_id | BIGINT FK | 关联 `insurance_rule.id` |
| operation_type | ENUM | 操作类型：`ADD`(增员), `REMOVE`(减员), `ADJUST`(调基), `SUPPLEMENT`(补缴) |

- 唯一约束：`(rule_id, operation_type)`

### 3.3 采集字段项 (`field_collection_item`)

从字典中选择字段并配置其在特定操作中的行为。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BIGINT PK | 主键 |
| config_id | BIGINT FK | 关联 `field_collection_config.id` |
| field_dict_id | BIGINT FK | 关联 `field_dict.id` |
| sort_order | INT | 展示排序顺序（从小到大） |
| is_required | TINYINT | 是否必填：`0`-否, `1`-是 |
| validation_rule | VARCHAR(512) | 校验规则：正则表达式或预定义规则编码 |
| display_label | VARCHAR(128) | 覆盖字典中的默认标签（为空时使用 `field_name`） |
| placeholder | VARCHAR(256) | 输入框提示语（仅 MANUAL 类型字段） |

### 3.4 关系图

```
insurance_rule (1) ─── (N) field_collection_config (4行/规则)
field_collection_config (1) ─── (N) field_collection_item
field_dict (1) ─── (N) field_collection_item (复用)
```

### 3.5 预留：运行时存储表

后续运行时采集引擎实现时使用，本次不创建。

```sql
employee_field_collection (
  id             BIGINT PK,
  change_id      BIGINT FK,    -- 关联异动记录
  field_dict_id  BIGINT FK,    -- 关联 field_dict
  value_text     TEXT,          -- 文本/日期/数值
  value_file_ids VARCHAR(512)  -- 附件/照片文件ID列表
)
```

## 4. 配置UI设计

### 4.1 入口位置

在现有"社保参保规则配置"编辑页中，现有"基本信息"、"参保险种"、"规则配置"三个分段的下方，新增**"字段采集配置"**分段（或作为第四个Tab）。

### 4.2 页面布局

```
┌─────────────────────────────────────────────────────┐
│  基本信息  │  参保险种  │  规则配置  │ [NEW]字段采集 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  [增员]  [减员]  [调基]  [补缴]                      │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │ 排序 │ 字段名称 │ 类型 │ 来源 │ 必填 │ 校验 │  │  │
│  ├──────┼──────────┼──────┼──────┼──────┼──────┤  │
│  │  1   │ 合同附件  │ 附件 │ 手动 │  是  │  -   │  │  │
│  │  2   │ 合同起始日│ 日期 │ 档案 │  是  │  -   │  │  │
│  │  3   │ 身份证附件│ 附件 │ 手动 │  否  │  -   │  │  │
│  └───────────────────────────────────────────────┘  │
│                                                     │
│  + 添加字段                                         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4.3 交互说明

- **操作类型切换**：点击"增员/减员/调基/补缴"按钮切换当前编辑的操作类型，未配置的显示空列表
- **添加字段**：弹出字段选择器（从 `field_dict` 中选择），支持多选添加
- **排序**：通过 `sort_order` 输入框调整，支持拖拽排序
- **编辑字段**：可修改 `is_required`、`validation_rule`、`display_label`、`placeholder`
- **删除字段**：移除该字段项，不影响字典
- **联动显示**：`field_type` 和 `value_source` 来自字典，配置时只读展示

## 5. 全局字段字典初始化数据

建议预置以下常见字段：

| field_code | field_name | field_type | value_source | auto_source_path |
|------------|-----------|-----------|-------------|-----------------|
| contract_attachment | 合同附件 | file | MANUAL | - |
| contract_start_date | 合同开始日期 | date | AUTO | employee.contract.startDate |
| contract_end_date | 合同结束日期 | date | AUTO | employee.contract.endDate |
| id_card_front | 身份证正面 | photo | MANUAL | - |
| id_card_back | 身份证反面 | photo | MANUAL | - |
| household_type | 户籍类型 | select | AUTO | employee.household.type |
| household_address | 户籍地址 | text | AUTO | employee.household.address |
| social_security_card | 社保卡号 | text | AUTO | employee.socialSecurity.cardNo |
| bank_account | 银行账号 | text | AUTO | employee.bankAccount.no |
| marriage_status | 婚姻状况 | select | AUTO | employee.basic.marriageStatus |
| emergency_contact | 紧急联系人 | text | AUTO | employee.emergency.name |
| emergency_phone | 紧急联系电话 | text | AUTO | employee.emergency.phone |

后续可根据实际业务需要持续扩充。

## 6. 运行时流程（预留）

后续独立 spec 实现，此处仅说明配置模型如何支撑：

1. 用户发起异动（增/减/调/补）时，加载该规则对应操作类型的 `field_collection_item` 列表
2. 按 `sort_order` 排序后渲染表单
3. `value_source = AUTO` 的字段：按 `auto_source_path` 从员工档案读取值，只读展示
4. `value_source = MANUAL` 的字段：按 `field_type` 渲染对应输入组件
5. 提交时校验：`is_required` 非空检查 + `validation_rule` 格式检查
6. 校验通过后保存异动及字段值到 `employee_field_collection` 表

## 7. 异常流与边界条件

- **空状态**：某操作类型未配置任何字段时，展示"未配置采集字段"提示，该操作类型的异动按原有流程执行
- **字段字典删除**：已被引用的字典项不允许删除，需先移除所有关联配置
- **校验规则为空**：`validation_rule` 为空时仅做类型基础校验（如日期格式、数字范围）
- **超长文本**：`display_label` 和 `placeholder` 长度限制，防止前端溢出
