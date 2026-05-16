---
title: 员工详情页 - 动态记录 Tab 化设计方案
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 员工详情页 - 动态记录 Tab 化设计方案

## 1. 背景与目标
在先前的重构中，我们已经将员工核心信息提取到了顶部通栏（`.employee-hero-panel`）。当前页面布局中，下方的 `.content-layout` 仍采用左右分栏 (`1fr 320px`)，右侧仅剩下一个“动态记录”模块 (`.timeline-section`)。
用户要求**移除右侧边栏，将“动态记录”作为一个普通的 Tab 展示**。这可以进一步简化页面结构，使内容区完全聚焦于单一信息的呈现。

## 2. 架构设计

### 2.1 布局结构的扁平化
- **移除左右分栏**：删除包裹在 `.detail-section` 外层的 `<div class="content-layout">`，或者将其 `grid-template-columns` 修改为单一的 `1fr`（或直接去掉网格布局）。
- **删除右侧容器**：移除 `<div class="summary-section">` 容器。

### 2.2 Tab 导航扩展
- 在原有的 `.tabs-nav` 中追加一个新的 `<button class="tab-item" data-tab="11">动态记录</button>`。
- 考虑到 Tab 数量已经达到 12 个，原有的响应式截断（超过容器宽度放入“更多”下拉菜单）逻辑将继续生效。

### 2.3 动态记录面板化
- 将原来的 `<section class="timeline-section">` 移动到 `.tab-content` 容器内。
- 使用包裹层 `<div class="tab-panel" id="tab-timeline">` 包裹它。
- **样式调整**：
  - 移除原 `.timeline-section` 的边框和圆角（因为 `.tab-content` 可能已经提供了容器，或者保持卡片样式与其他 Tab 统一）。
  - 取消或调整原有的“查看全部/收起” (`.timeline-toggle`) 按钮逻辑。既然它已经成为了一个独立的 Tab，它可以独占一整页的高度，无需折叠隐藏，可以直接展示所有动态或提供分页/无限滚动。

### 2.4 JavaScript 逻辑适配
- 确保现有的 `switchTab` 逻辑能够覆盖到新增加的第 12 个 Tab。
- 移除与右侧边栏相关的、可能存在的 Sticky 定位逻辑（如果有的话）。

## 3. 下一步
请确认上述设计是否符合您的预期？确认后我将生成具体的代码实施计划并执行修改。