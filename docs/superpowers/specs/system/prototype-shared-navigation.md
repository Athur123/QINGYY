---
title: Prototype Shared Navigation Design
module: system
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# Prototype Shared Navigation Design

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 作者 | Codex |
| 日期 | 2026-05-12 |
| 版本 | v1.0 |
| 范围 | 主线原型页面共享导航改造 |

## 背景

当前 `prototype/` 下的原型页面以静态 HTML 为主，各页面导航结构不统一：

- 部分页面使用 `qy-sidebar` 作为主侧边栏。
- 部分页面使用 `.sidebar` / `.sidebar-nav` 作为主侧边栏。
- 部分页面只有顶部导航或业务内容侧栏。
- 部分历史迭代页的导航和现行页面不同步。

已新增的 `prototype/index.html` 可以作为全项目浏览入口，但如果各主线原型页继续手写导航，后续新增、废弃、调整页面时仍然需要多处维护。

## 目标

建立一套适合静态 HTML 原型仓库的共享导航机制：

- 使用一份共享导航数据维护模块、页面、路径、状态和主线标记。
- `prototype/index.html` 从共享数据渲染总入口。
- 第一阶段只接入现行主线页面中可承载主导航的页面。
- 不要求历史迭代页、演示页、废弃页同步改造。

## 非目标

- 不引入构建工具、前端框架或包管理依赖。
- 不改造所有历史迭代页面。
- 不移动、不重命名现有原型页面。
- 不统一每个页面的完整布局，只统一“原型浏览导航入口”。
- 不把业务信息侧栏误替换为项目主导航。

## 第一阶段覆盖页面

| 模块 | 页面 |
| --- | --- |
| 对账复核 | `prototype/reconciliation/summary.html` |
| 对账复核 | `prototype/reconciliation/unified.html` |
| 社保计算 | `prototype/calculator/index.html` |
| 社保计算 | `prototype/calculator/policy.html` |
| 社保计算 | `prototype/calculator/region-rules.html` |
| 社保计算 | `prototype/calculator/sub-account.html` |
| 员工管理 | `prototype/employee/detail.html` |
| 员工管理 | `prototype/employee/change-field.html` |
| 员工管理 | `prototype/employee/cost-detail.html` |
| 参保配置 | `prototype/insurance-config/stepper.html` |
| 参保配置 | `prototype/insurance-config/field-collection.html` |
| 结算方案 | `prototype/settlement/plan.html` |
| 结算方案 | `prototype/settlement/detail.html` |
| 结算方案 | `prototype/settlement/cost-allocation.html` |
| 审批管理 | `prototype/approval/template-management.html` |
| 系统 | `prototype/system/log-viewer.html` |
| 系统 | `prototype/system/sys-log.html` |

## 共享文件

### `prototype/shared/prototype-nav.js`

负责维护导航数据和渲染函数。建议暴露到 `window.QYPrototypeNav`，避免模块化加载限制，使页面可以通过普通 `<script>` 引入。

数据至少包含：

| 字段 | 说明 |
| --- | --- |
| `id` | 页面唯一标识，例如 `reconciliation.summary` |
| `moduleId` | 模块标识，例如 `reconciliation` |
| `moduleName` | 模块中文名 |
| `title` | 页面标题 |
| `path` | 相对 `prototype/` 根目录的页面路径 |
| `status` | `main`、`iteration`、`demo`、`obsolete` |
| `isMain` | 是否主线页面 |
| `description` | 页面用途说明 |

### `prototype/shared/prototype-nav.css`

负责共享导航样式，避免把同一段样式复制到每个主线页面。

核心样式包含：

- 左侧导航容器。
- 模块分组。
- 页面链接。
- 当前页面高亮。
- 返回总入口链接。
- 小屏幕下的紧凑展示。

## 页面接入方式

主线页面通过以下方式接入共享导航：

```html
<link rel="stylesheet" href="../shared/prototype-nav.css">
<div data-prototype-nav data-current="reconciliation.summary"></div>
<script src="../shared/prototype-nav.js"></script>
```

页面位于模块目录下时，`shared` 目录相对路径为 `../shared/`。`prototype/index.html` 位于 `prototype/` 根目录，应使用 `shared/prototype-nav.js`。

第一阶段存在两种接入形态：

| 形态 | 适用页面 | 挂载方式 |
| --- | --- | --- |
| 左侧共享导航 | 页面已有可安全替换的项目级主侧栏，或页面主布局可稳定承载左侧导航 | `<div data-prototype-nav data-root="../" data-current="PAGE_ID"></div>` |
| 顶部紧凑入口 | 页面没有项目级主侧栏，或左侧区域是业务筛选、员工信息、结算步骤等局部内容 | `<div class="prototype-nav-compact" data-prototype-nav data-root="../" data-current="PAGE_ID"></div>` |

`prototype/system/log-viewer.html` 的历史侧栏结构较深，第一阶段以共享导航接入为准，并通过页面级样式隐藏旧项目侧栏，避免大范围重写页面内容。

## 渲染规则

- 默认只渲染 `isMain = true` 的主线页面。
- 当前页面通过 `data-current` 高亮。
- 导航顶部固定展示“青阳云 HRO 原型”和“返回总入口”。
- 模块按固定顺序展示：对账复核、社保计算、员工管理、参保配置、结算方案、审批管理、系统。
- 链接路径根据当前页面所在深度自动转换，确保从模块页面可以跳转到其他模块页面。
- `prototype/index.html` 可以展示所有页面，主线页、迭代页、演示页和废弃页由共享数据中的 `status` 区分。

## 主线页面改造原则

- 对已有主导航的页面，替换原手写主导航为共享导航挂载点。
- 对没有主导航或左侧为业务信息侧栏的页面，优先增加 `prototype-nav-compact` 顶部紧凑导航入口，不强行改布局。
- 页面主体业务内容、交互脚本和业务样式保持不变。
- 如页面存在移动端侧栏交互，第一阶段不扩展复杂抽屉，只保证桌面浏览入口一致。

## 验收标准

- `prototype/index.html` 的模块和页面卡片来自共享导航数据。
- 第一阶段覆盖的主线页面可以看到统一原型导航入口。
- 当前页面在共享导航中高亮。
- 从任一已接入主线页面可以跳转回 `prototype/index.html`。
- 从任一已接入主线页面可以跳转到其他主线页面。
- 历史迭代页、演示页、废弃页未被误改为主线页。
- 所有导航链接对应本地 HTML 文件存在。
