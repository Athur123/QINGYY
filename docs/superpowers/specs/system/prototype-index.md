# Prototype Index Design

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 作者 | Codex |
| 日期 | 2026-05-12 |
| 版本 | v1.0 |
| 范围 | 新增青阳云 HRO 原型总入口页 |

## 背景

当前原型按业务模块存放在 `prototype/` 下，模块包括对账复核、社保计算、员工管理、参保配置、结算方案、审批管理、系统。页面数量较多，且部分文件是历史迭代或演示版本，缺少一个统一浏览入口。

## 目标

新增 `prototype/index.html`，作为整个青阳云 HRO 原型项目的浏览入口。用户从项目根目录启动静态服务后，可访问 `http://localhost:8080/prototype/` 查看所有模块和页面链接。

## 非目标

- 不新增各模块目录级 `index.html`。
- 不移动、不重命名现有原型文件。
- 不改现有业务原型页面内容。
- 不把已废弃页面恢复为现行入口。

## 信息架构

入口页按业务模块分组展示页面：

| 模块 | 目录 | 说明 |
| --- | --- | --- |
| 对账复核 | `prototype/reconciliation/` | 展示现行汇总页、明细核对页，并单独标记历史废弃页 |
| 社保计算 | `prototype/calculator/` | 展示计算器、政策、地区规则、二级户、参保档案、智能公式识别等页面 |
| 员工管理 | `prototype/employee/` | 展示员工详情、异动采集、费用明细、档案版本、异动列表等页面 |
| 参保配置 | `prototype/insurance-config/` | 展示参保规则向导、字段配置相关页面 |
| 结算方案 | `prototype/settlement/` | 展示结算计划、账单明细、费用分摊、垫付、归属固化等页面 |
| 审批管理 | `prototype/approval/` | 展示审批模板管理页面 |
| 系统 | `prototype/system/` | 展示日志、系统操作日志、汇总统计演示页面 |

## 页面状态

页面卡片使用以下状态标签帮助识别优先级：

| 状态 | 含义 |
| --- | --- |
| 主线 | 当前模块优先查看的主要页面 |
| 迭代 | 历史迭代或备选方案页面，仍可查看 |
| 演示 | 用于验证组件、交互或业务规则的演示页 |
| 已废弃 | 已明确不作为现行原型使用，仅保留历史参考 |

## 交互要求

- 页面链接使用相对路径，确保从 `prototype/index.html` 打开时能直接跳转。
- 每个页面卡片展示页面标题、文件路径、状态标签和简短说明。
- 顶部展示项目名称、入口说明、模块数量和页面数量。
- 保持静态 HTML，无构建依赖。
- 使用现有青阳云设计系统 CSS 文件：`../styles/qingyang-variables.css`、`../styles/qingyang-base.css`、`../styles/qingyang-components.css`、`../styles/qingyang-forms.css`。
- 页面清单和状态标签应优先来自 `prototype/shared/prototype-nav.js`，避免入口页与主线页面导航分叉。

## 验收标准

- 访问 `http://localhost:8080/prototype/` 能看到总入口页。
- 入口页列出 7 个业务模块。
- 入口页包含所有现有原型 HTML 页面链接。
- `prototype/reconciliation/obsolete/index.html` 被标记为已废弃。
- 所有链接对应的本地 HTML 文件存在。
