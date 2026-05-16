# 青阳云（Qingyang Cloud）HRO 原型仓库 Code Wiki

> 本文档基于仓库当前实际内容生成：以「静态 HTML 原型 + CSS 设计系统 + 需求/实现规划文档 + 自动化技能」为主。仓库内未发现可直接运行的后端服务或前端工程化构建产物（如 package.json、pyproject.toml 等）。

## 目录

- [1. 项目定位与整体架构](#1-项目定位与整体架构)
- [2. 目录结构与模块职责](#2-目录结构与模块职责)
- [3. 设计系统（styles）](#3-设计系统styles)
- [4. 原型页面（prototype）](#4-原型页面prototype)
- [5. 关键函数与算法（原型页内联 JS）](#5-关键函数与算法原型页内联-js)
- [6. Claude Skills 自动化（.claude/skills）](#6-claude-skills-自动化claudeskills)
- [7. 依赖关系与外部依赖](#7-依赖关系与外部依赖)
- [8. 运行与验证方式](#8-运行与验证方式)
- [9. 约定与最佳实践](#9-约定与最佳实践)
- [10. 已知不一致与缺口](#10-已知不一致与缺口)

---

## 1. 项目定位与整体架构

**定位**
- 面向「青阳云 HRO（外包派遣/客户组织）SaaS」的 UI/UE 原型与设计系统仓库。
- 主要承载：
  - 页面原型（纯 HTML/CSS/原生 JS），用于评审与交互验证。
  - 设计系统（CSS/SCSS），用于统一组件视觉与布局规范。
  - 规划/规格文档（docs/superpowers），用于沉淀需求、数据结构、流程、API 草案。
  - 浏览器自动化技能（Claude Skills），用于辅助在真实系统里做操作验证。

**整体架构（以“原型仓库”视角）**
- 原型页以浏览器直接打开或静态服务器方式运行（无打包/构建流程）。
- 设计系统通过 `<link rel="stylesheet" ...>` 方式被原型页引用。
- 原型的交互逻辑多数写在页面内联 `<script>` 中，使用 DOM API 操作，不依赖框架。
- “后端/接口”在部分原型中以 `API_BASE` 或 mock 数据存在；真实后端实现仅在 docs 中规划。

关键参考：
- 代码协作说明：[CLAUDE.md](file:///Users/athur/PycharmProjects/qyy/CLAUDE.md)
- Codex 入口说明：[AGENTS.md](file:///Users/athur/PycharmProjects/qyy/AGENTS.md)
- 设计系统规范（文档版）：[qingyang-hro-design-system.md](file:///Users/athur/PycharmProjects/qyy/qingyang-hro-design-system.md)
- 组件说明：[styles/README.md](file:///Users/athur/PycharmProjects/qyy/styles/README.md)

---

## 2. 目录结构与模块职责

> 下面仅覆盖“主仓库根目录”，`.claude/worktrees/*` 为历史/实验工作区快照，通常不作为主线源码入口。

### 2.1 顶层目录

| 目录/文件 | 职责 | 说明 |
|---|---|---|
| [prototype/](file:///Users/athur/PycharmProjects/qyy/prototype) | 静态页面原型 | 按 7 个业务模块拆分的 HTML 原型页面 |
| [styles/](file:///Users/athur/PycharmProjects/qyy/styles) | CSS/SCSS 设计系统 | 变量、基础样式、组件库、表单库以及示例页 |
| [docs/superpowers/](file:///Users/athur/PycharmProjects/qyy/docs/superpowers) | 规划与规格文档 | plans（实施计划）/ specs（设计说明、数据结构、流程） |
| [.claude/skills/](file:///Users/athur/PycharmProjects/qyy/.claude/skills) | 自动化技能说明 | 以浏览器自动化方式完成登录/切换维度等操作 |
| [.agents/skills/](file:///Users/athur/PycharmProjects/qyy/.agents/skills) | Codex 项目技能 | 与 Claude 技能对应的项目级技能入口 |
| [scripts/](file:///Users/athur/PycharmProjects/qyy/scripts) | 仓库辅助脚本 | PDF 转换、post-commit hook、memory 更新 |
| [.superpowers/](file:///Users/athur/PycharmProjects/qyy/.superpowers) | brainstorming 产物 | 片段型 HTML 草稿与策略说明 |
| [CLAUDE.md](file:///Users/athur/PycharmProjects/qyy/CLAUDE.md) | Claude 协作说明 | 约定、目录解释、原型预览方式 |
| [AGENTS.md](file:///Users/athur/PycharmProjects/qyy/AGENTS.md) | Codex 协作说明 | 与 `CLAUDE.md` 同步的项目级协作入口 |
| [README.md](file:///Users/athur/PycharmProjects/qyy/README.md) | 快速入口文档 | 新协作者的最短阅读路径 |

### 2.2 docs/superpowers 内容分层

| 子目录 | 目标 | 典型内容 |
|---|---|---|
| [docs/superpowers/specs/](file:///Users/athur/PycharmProjects/qyy/docs/superpowers/specs) | 需求/设计细节落地 | 按模块拆分：页面流程、状态机、数据结构、交互细节、导入模板 |
| [docs/superpowers/plans/](file:///Users/athur/PycharmProjects/qyy/docs/superpowers/plans) | 实施计划与拆分 | 按模块拆分：任务拆解、接口草案、落地文件结构建议 |

---

## 3. 设计系统（styles）

设计系统是本仓库的“核心可复用资产”：通过 `qy-` 前缀的组件类与 token（CSS Variables）统一 UI 规范。

### 3.1 文件组织

参考：[styles/README.md](file:///Users/athur/PycharmProjects/qyy/styles/README.md)

| 文件 | 角色 | 通常由谁引用 |
|---|---|---|
| [qingyang-variables.css](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-variables.css) | 设计令牌（颜色/间距/字体/圆角/阴影等） | 所有原型页 |
| [qingyang-base.css](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-base.css) | reset + 基础排版 + 工具类 | 所有原型页 |
| [qingyang-components.css](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-components.css) | 通用组件库（按钮/卡片/表格/弹窗等） | 业务原型页 |
| [qingyang-forms.css](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-forms.css) | 表单控件库（输入框/选择器/表单布局等） | 表单型原型页 |
| [qingyang-design-system.css](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-design-system.css) | 聚合版（变量+基础+组件） | 希望“一次引入”的原型页 |
| [qingyang-variables.scss](file:///Users/athur/PycharmProjects/qyy/styles/qingyang-variables.scss) | SCSS 变量 + mixin | SCSS 场景（当前仓库未见编译管线） |
| [example.html](file:///Users/athur/PycharmProjects/qyy/styles/example.html) | 组件展示页 | 本地直接打开预览组件效果 |

### 3.2 命名规范（关键“类”）

来源：[qingyang-hro-design-system.md](file:///Users/athur/PycharmProjects/qyy/qingyang-hro-design-system.md#L1972-L1990)

- 组件：`.qy-{组件名}`，例如 `.qy-btn`、`.qy-card`、`.qy-table`
- 修饰符：`.qy-{组件}--{variant}`，例如 `.qy-btn--primary`、`.qy-tag--success`
- 子元素：`.qy-{组件}__{element}`，例如 `.qy-card__header`、`.qy-drawer__body`
- 状态：`.is-{state}`，例如 `.is-open`、`.is-active`、`.is-selected`

### 3.3 常用组件索引（示例）

设计系统的“关键 API”就是这些 class 组合（详细用法见 [styles/README.md](file:///Users/athur/PycharmProjects/qyy/styles/README.md)）：
- 按钮：`qy-btn` + `qy-btn--primary/secondary/text/danger`
- 卡片：`qy-card` + `qy-card__header/body/footer`
- 表格：`qy-table`（容器通常配合 `qy-table-wrapper` / `qy-table-container`）
- 抽屉：`qy-drawer` + `qy-drawer__header/body/footer`（默认宽度 520px 规范见 [qingyang-hro-design-system.md](file:///Users/athur/PycharmProjects/qyy/qingyang-hro-design-system.md#L1365-L1413)）
- 标签：`qy-tag` + `qy-tag--success/warning/error/primary`
- 表单：`qy-form`、`qy-form-item`、`qy-input`、`qy-select` 等

---

## 4. 原型页面（prototype）

原型页面用于承载“页面级布局、交互流程、数据结构展示”，通常包含：
- 引用设计系统 CSS
- 页面私有样式（内联 `<style>`，用于覆盖或补充）
- 页面私有交互脚本（内联 `<script>`，包含 mock 数据与事件绑定）

### 4.1 原型页清单（按模块）

| 模块 | 主入口页面 | 主题/职责 |
|---|---|---|
| Approval | [prototype/approval/template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval/template-management.html) | 审批模板管理 |
| Reconciliation | [prototype/reconciliation/summary.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html), [prototype/reconciliation/unified.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html) | 对账汇总与明细核对主流程 |
| Calculator | [prototype/calculator/index.html](file:///Users/athur/PycharmProjects/qyy/prototype/calculator/index.html), [prototype/calculator/policy.html](file:///Users/athur/PycharmProjects/qyy/prototype/calculator/policy.html), [prototype/calculator/region-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/calculator/region-rules.html), [prototype/calculator/sub-account.html](file:///Users/athur/PycharmProjects/qyy/prototype/calculator/sub-account.html) | 社保计算、政策、地区规则、分账 |
| Employee | [prototype/employee/detail.html](file:///Users/athur/PycharmProjects/qyy/prototype/employee/detail.html), [prototype/employee/change-field.html](file:///Users/athur/PycharmProjects/qyy/prototype/employee/change-field.html) | 员工详情与异动采集 |
| Settlement | [prototype/settlement/plan.html](file:///Users/athur/PycharmProjects/qyy/prototype/settlement/plan.html), [prototype/settlement/detail.html](file:///Users/athur/PycharmProjects/qyy/prototype/settlement/detail.html), [prototype/settlement/advance-payment.html](file:///Users/athur/PycharmProjects/qyy/prototype/settlement/advance-payment.html) | 结算、归属、垫付 |
| Insurance Config | [prototype/insurance-config/stepper.html](file:///Users/athur/PycharmProjects/qyy/prototype/insurance-config/stepper.html), [prototype/insurance-config/field-collection.html](file:///Users/athur/PycharmProjects/qyy/prototype/insurance-config/field-collection.html) | 参保配置与字段采集 |
| System | [prototype/system/log-viewer.html](file:///Users/athur/PycharmProjects/qyy/prototype/system/log-viewer.html), [prototype/system/sys-log.html](file:///Users/athur/PycharmProjects/qyy/prototype/system/sys-log.html) | 系统日志类页面 |

### 4.2 页面与设计系统的引用关系（示例）

审批模板管理页在 `<head>` 中依次引入变量、基础、组件、表单（常见做法）：
- [template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval/template-management.html#L7-L10)

对账页在此基础上额外引入聚合 CSS 与外部 xlsx 库：
- [summary.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html#L10-L16)

---

## 5. 关键函数与算法（原型页内联 JS）

本仓库没有“统一的 JS 源码模块”，关键逻辑以“页面内联函数”的方式存在。以下按页面归类，列出具有代表性的函数/算法与其职责。

### 5.1 通用交互：Toast / Confirm

垫付申请页内实现了可复用的 toast 与 confirm：
- `showToast(message, type, duration)`：创建并展示 toast（自动消失/手动关闭）  
  参考：[advance-payment-apply.html](file:///Users/athur/PycharmProjects/qyy/prototype/advance-payment-apply.html#L1154-L1183)
- `dismissToast(toast)`：触发离场动画并移除  
  参考：[advance-payment-apply.html](file:///Users/athur/PycharmProjects/qyy/prototype/advance-payment-apply.html#L1185-L1188)
- `showConfirmDialog(message)` / `closeConfirmDialog(result)`：Promise 化确认弹窗  
  参考：[advance-payment-apply.html](file:///Users/athur/PycharmProjects/qyy/prototype/advance-payment-apply.html#L1202-L1217)

### 5.2 审批模板：列表渲染 + 抽屉表单

审批模板管理页核心是“模板列表渲染 + 抽屉模式切换（新建/编辑/详情）”：
- `loadTemplates()`：尝试从 `API_BASE` 拉取，失败回退 mock  
  参考：[approval-template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval-template-management.html#L231-L253)
- `renderTemplates(templates)`：将模板数组渲染为 `<tbody>` 行，并基于状态生成操作按钮  
  参考：[approval-template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval-template-management.html#L255-L279)
- `openAddTemplateDrawer()`：构建抽屉内容（表单 + 预览 + 鉴权信息），并注入 footer 操作  
  参考：[approval-template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval-template-management.html#L297-L373)
- `updateFormPreview()`：基于表单类型生成字段 JSON 预览  
  参考：[approval-template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval-template-management.html#L375-L386)
- `openEditTemplateDrawer(templateType)`：根据模板状态决定编辑权限（full/partial/name-remark-only）  
  参考：[approval-template-management.html](file:///Users/athur/PycharmProjects/qyy/prototype/approval-template-management.html#L388-L408)

### 5.3 规则匹配：地区社保规则的匹配/冲突检测

[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html) 内包含一套“可运行的规则匹配 demo”，其结构非常接近未来后端/规则引擎的雏形：
- 条件匹配：
  - `evaluateCondition(condition, employee)`：单条件判断（in / notIn / = / !=）  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L471-L485)
  - `evaluateConditionGroup(conditions, logicalType, employee)`：组内 AND/OR  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L487-L493)
  - `evaluateRule(rule, employee)`：规则整体匹配（多个 group）  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L495-L499)
- 区域匹配与有效期：
  - `matchesRegion(ruleRegion, employeeRegion)`：省/市/区逐级匹配  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L501-L512)
  - `isWithinEffectPeriod(rule)`：生效起止日期判断  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L435-L442)
- 冲突检测与动作解析：
  - `detectConflicts(matchedRules)`：同一险种出现不同 action 即判定冲突  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L514-L536)
  - `resolveAction(action, employee)`：将 dispatch_ratio / specified_ratio / account_ratio 统一解析为可展示结构  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L538-L551)
  - `matchRules(employee, accountId)`：综合入口（筛 active + 排序 + 匹配 + 冲突判断 + 合并动作）  
    参考：[region-social-insurance-rules.html](file:///Users/athur/PycharmProjects/qyy/prototype/region-social-insurance-rules.html#L553-L586)

### 5.4 台账对账：差异计算 + 导入/导出

对账页体现了典型的“前端数据处理流水线”：筛选 → 计算差异 → 渲染 → 分页。
- `getFilteredSystemRecords()`：按筛选条件过滤系统记录  
  参考：[unified.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html#L1206-L1216)
- `calculateDifferences()`：用 `Map` 以 `(idCard, insuranceType, billingMonth)` 作为 key 计算系统多/台账多  
  参考：[unified.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html#L1219-L1263)
- `renderDiffTable()` / `renderPagination()` / `renderAll()`：渲染差异列表与分页状态  
  参考：[unified.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/unified.html#L1301-L1382)
- Excel 导入/导出依赖 `xlsx`（见第 7 节依赖）  

---

## 6. Claude Skills 自动化（.claude/skills）

仓库提供的技能用于在真实「青阳云系统」中执行操作（需要浏览器自动化环境）。

### 6.1 技能清单

| 技能 | 用途 | 文档 |
|---|---|---|
| qingyang-login | 自动打开登录页并登录 | [.claude/skills/qingyang-login/SKILL.md](file:///Users/athur/PycharmProjects/qyy/.claude/skills/qingyang-login/SKILL.md) |
| qingyang-switch-hro | 从 EHR 切换到 HRO 维度（客户组织） | [.claude/skills/qingyang-switch-hro/SKILL.md](file:///Users/athur/PycharmProjects/qyy/.claude/skills/qingyang-switch-hro/SKILL.md) |

### 6.2 技能运行依赖（配置约定）

技能文档约定从环境变量读取登录信息，示例见：[CLAUDE.md](file:///Users/athur/PycharmProjects/qyy/CLAUDE.md#L67-L75)

注意：文档中示例密码等属于演示/内网环境信息；在真实环境中应避免在仓库中写入敏感信息。

---

## 7. 依赖关系与外部依赖

### 7.1 模块依赖图（概念）

```text
prototype/<module>/*.html
  ├─(link) styles/qingyang-variables.css
  ├─(link) styles/qingyang-base.css
  ├─(link) styles/qingyang-components.css
  ├─(link) styles/qingyang-forms.css
  ├─or single-link snapshot: styles/qingyang-design-system.css
  └─(optional script) 外部 CDN 依赖（如 xlsx）

docs/superpowers/*  → 为未来工程化/后端落地提供规格与计划（当前仓库未落地对应代码）
.claude/skills/*    → 依赖浏览器自动化（Playwright MCP / Browser tools）
```

### 7.2 外部依赖（CDN/远程资源）

- Excel 处理库：`xlsx@0.18.5`
  引用点：[summary.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html#L16)
- Google Fonts：Plus Jakarta Sans（设计系统首选），Inter 作为回退字体
  示例：[summary.html](file:///Users/athur/PycharmProjects/qyy/prototype/reconciliation/summary.html#L7-L9)、[qingyang-hro-design-system.md](file:///Users/athur/PycharmProjects/qyy/qingyang-hro-design-system.md#L24-L29)
- Figma MCP 捕获脚本（用于 html-to-design）：
  引用点：[policy.html](file:///Users/athur/PycharmProjects/qyy/prototype/calculator/policy.html#L2741)

---

## 8. 运行与验证方式

### 8.1 原型页面本地预览

统一方式：从项目根目录启动静态服务器（避免 CSS 相对路径失效）

```bash
python3 -m http.server 8080
```

然后访问：`http://localhost:8080/prototype/<module>/<page>.html`

例如：
- `http://localhost:8080/prototype/approval/template-management.html`
- `http://localhost:8080/prototype/reconciliation/summary.html`

上述方式与仓库当前约定一致：[CLAUDE.md](file:///Users/athur/PycharmProjects/qyy/CLAUDE.md#L133-L147)

### 8.2 设计系统预览

直接打开示例页：
- [styles/example.html](file:///Users/athur/PycharmProjects/qyy/styles/example.html)

### 8.3 自动化技能验证

在支持浏览器自动化的环境中触发技能（具体触发方式由使用的 Agent/IDE 决定），技能步骤参考：
- [qingyang-login/SKILL.md](file:///Users/athur/PycharmProjects/qyy/.claude/skills/qingyang-login/SKILL.md)
- [qingyang-switch-hro/SKILL.md](file:///Users/athur/PycharmProjects/qyy/.claude/skills/qingyang-switch-hro/SKILL.md)

---

## 9. 约定与最佳实践

### 9.1 原型开发约定（推荐做法）

- 优先复用设计系统组件与 token，避免在页面里硬编码颜色/间距。
- 页面级补丁样式建议聚焦“布局与业务差异”，不要把通用组件样式写回原型页。
- 交互脚本以“可读性优先”，数据结构与状态命名与 specs 保持一致，便于未来工程化迁移。
- 重要交互（如抽屉、弹窗、批量操作、导入校验）建议复用既有页面里的实现模式（见第 5 节）。

### 9.2 UI 规范

- Token 与组件解释见：[styles/README.md](file:///Users/athur/PycharmProjects/qyy/styles/README.md)
- 组件与页面布局模板见：[qingyang-hro-design-system.md](file:///Users/athur/PycharmProjects/qyy/qingyang-hro-design-system.md)

---

## 10. 已知不一致与缺口

- 本仓库是原型与文档仓库，不包含完整后端/前端工程化实现；`docs/superpowers/plans/` 中的后端或数据库内容应视为规划而非可直接运行代码。
- 本地代理配置文件（如 `.claude/settings.local.json`、`.codex/config.toml`）可能存在于工作目录，但应保持本地化，不纳入版本控制。
