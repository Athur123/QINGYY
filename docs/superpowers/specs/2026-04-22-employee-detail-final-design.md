# 员工详情页最终设计规范

## Context

基于青阳云 HRO 系统的员工详情页原型设计，完成了以下核心功能：
- 员工详情页 Tab 导航结构
- 动态记录时间线组件
- 明细记录（新增/编辑/删除）卡片展示
- 统一的数据结构

## 页面结构

### Tab 导航

| Tab 名称 | 说明 |
|---------|------|
| 基础信息 | 员工基本信息 |
| 合同信息 | 劳动合同明细（支持多条） |
| 银行卡 | 银行卡信息（支持多条） |
| 教育经历 | 教育背景（支持多条） |
| 工作经历 | 工作履历（支持多条） |
| 证书资质 | 证书明细（支持多条） |
| 培训记录 | 培训记录（支持多条） |
| 参保档案 | 社保信息 |
| **个税档案** | 税务信息（支持多条） |
| **动态记录** | 变更历史时间线 |

### Tab 样式

- 高度 36px，紧凑设计
- 选中态：蓝色下划线 (2px) + 文字 `#2563EB` 加粗
- 未选中态：灰色文字 `#64748B`
- 支持横向滚动

## 动态记录设计

### 数据结构（统一）

```javascript
{
  eventType: "修改员工档案",    // 显示的事件类型
  eventTypeClass: "gray",       // CSS样式类
  eventTime: "2026-04-22 14:30",
  operator: "张三",
  dotClass: "",                 // 圆点样式
  action: "编辑",               // 新增/编辑/删除
  tabName: "银行卡",            // Tab名称，基础信息为空
  record: "招商银行(副卡)",      // 记录名称
  changes: [                    // 变更字段（编辑时）
    { field: "开户银行", oldValue: "-", newValue: "招商银行深圳福田支行" }
  ],
  fields: {...}                 // 完整字段（新增/删除时）
}
```

### 事件类型

| eventType | eventTypeClass | 说明 |
|-----------|----------------|------|
| 入职 | success | 新员工入职 |
| 转正 | success | 试用期转正式 |
| 调岗 | primary | 岗位变动 |
| 调薪 | primary | 薪资调整 |
| 离职 | danger | 员工离职 |
| 重新入职 | success | 离职后再入职 |
| 信息变更 | gray | 编辑修改档案 |
| 修改员工档案 | gray/primary/danger | 通用明细操作 |
| 参保报送 | primary | 社保公积金报送 |
| 个税报送 | primary | 税务申报 |
| 个税档案 | primary/gray/danger | 个税档案操作 |

### 操作标签

| action | 标签颜色 | CSS类 |
|--------|---------|-------|
| 新增 | 绿色 `#d1fae5` 背景 + `#065f46` 文字 | `timeline-item__action-tag--add` |
| 编辑 | 蓝色 `#eff6ff` 背景 + `#2563EB` 文字 | `timeline-item__action-tag--edit` |
| 删除 | 红色 `#fee2e2` 背景 + `#991b1b` 文字 | `timeline-item__action-tag--delete` |

### 卡片样式

**新增记录卡片** (`timeline-item__change-card--added`)
- 背景：#f0fdf4（浅绿）
- 边框：#bbf7d0（绿色）

**编辑记录卡片**（默认）
- 背景：#F8FAFC（灰色）
- 边框：无

**删除记录卡片** (`timeline-item__change-card--deleted`)
- 背景：#fef2f2（浅红）
- 边框：#fecaca（红色）

### 卡片头部格式

| 场景 | 格式 | 示例 |
|------|------|------|
| 基础信息变更 | `{action} {record}` | 编辑 基础信息 |
| 多记录Tab变更 | `{action} {tabName}({record})` | 新增 银行卡(招商银行副卡) |

## 筛选功能

### 筛选器组件

- **类型筛选** (`typeFilter`)：按 eventType 筛选
- **字段筛选** (`fieldFilter`)：按变更字段名筛选（支持 changes 和 fields）
- **时间筛选** (`timeFilter`)：近一周/近一月/近三月/近一年

### 字段筛选逻辑

```javascript
if (log.changes) {
  return log.changes.some(change => change.field === fieldFilter.value);
}
if (log.fields) {
  return Object.keys(log.fields).some(key => key === fieldFilter.value);
}
```

## 个税档案 Tab

### 字段定义

| 字段名 | 说明 | 输入类型 |
|--------|------|---------|
| 扣缴义务人 | 扣缴单位名称 | text |
| 人员状态 | 在职状态 | select（正常/待入职/离职） |
| 申报状态 | 申报状态 | select（待申报/已申报/申报失败） |
| 主管税务机关名称 | 税务局 | text |
| 是否默认 | 是否默认 | select（是/否） |
| 是否允许算税 | 是否参与算税 | select（是/否） |
| 任职受雇从业类型 | 雇员类型 | select（雇员/保险营销员/证券经纪人/独立董事/其他） |

### 示例数据结构

```javascript
{
  withholdingObligor: '深圳市前海人力资源有限公司',
  personStatus: '正常',
  declareStatus: '待申报',
  taxAuthority: '国家税务总局深圳市税务局',
  isDefault: true,
  allowTaxCalc: true,
  employmentType: '雇员'
}
```

## 代码组织

### 文件结构

```
prototype/employee-detail-v2.html  # 单文件原型（包含HTML/CSS/JS）
```

### 代码分节注释

```javascript
// ============================================================================
// SECTION: Copy Function
// ============================================================================
// SECTION: Dynamic Logs Data & Renderer
// ============================================================================
// SECTION: Modal & Form Handlers
// ============================================================================
// SECTION: Sample Data
// ============================================================================
// SECTION: Helper Functions
// ============================================================================
// SECTION: Delete Record Handler
// ============================================================================
```

### 核心函数

| 函数名 | 说明 |
|--------|------|
| `renderDynamicLogs()` | 渲染动态记录时间线 |
| `renderLogCard(log)` | 渲染单条记录卡片 |
| `initFieldFilter()` | 初始化字段筛选下拉框 |
| `toggleLogDetail(index)` | 展开/收起详情 |
| `openModal(type, index)` | 打开编辑Modal |
| `saveRecord()` | 保存记录并生成变更日志 |
| `deleteRecord(type, index, label)` | 删除记录 |
| `generateChanges(category, oldData, newData)` | 生成变更差异 |

## 设计令牌

```css
:root {
  /* Colors */
  --primary: #2563EB;
  --primary-hover: #1d4ed8;
  --primary-light: #eff6ff;
  --background: #F8FAFC;
  --surface: #FFFFFF;
  --border: #E2E8F0;
  --text-primary: #1E293B;
  --text-secondary: #64748B;
  --text-muted: #94a3b8;
  --success: #10b981;
  --success-bg: #d1fae5;
  --success-text: #065f46;
  --danger: #ef4444;
  --danger-bg: #fee2e2;
  --danger-text: #991b1b;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 12px;
  --space-lg: 16px;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
}
```

## 实施文件

- `prototype/employee-detail-v2.html` — 员工详情页原型（含所有功能）

## 验证清单

- [ ] Tab导航显示正确，所有Tab可切换
- [ ] 动态记录时间线正确显示
- [ ] 操作标签（新增/编辑/删除）颜色正确
- [ ] 卡片格式：基础信息显示"编辑 基础信息"，多记录Tab显示"新增 银行卡(招商银行)"
- [ ] 筛选器按类型/字段/时间筛选正常
- [ ] 编辑Modal可正常打开和保存
- [ ] 删除记录功能正常
- [ ] 个税档案Tab显示正确
