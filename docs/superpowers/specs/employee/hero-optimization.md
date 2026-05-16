---
title: 员工详情页 - 员工主卡片（Hero Section）优化设计方案
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 员工详情页 - 员工主卡片（Hero Section）优化设计方案

## 1. 目标与背景
当前在 `prototype/employee-detail-redesign.html` 中的员工主卡片（`.employee-hero`）高度过大，挤占了下方 Tab 导航及核心信息（如基础信息、合同等）的首屏展示空间。用户选择了**方案 C：白底信息面板**，希望通过**合并顶部导航**、**调整卡片内部布局**以及**调整页面整体间距**，将这部分区域进一步压缩，使主卡片为白底边框，与下方内容视觉更统一，信息网格化分布。

## 2. 优化方案概述

### 2.1 整合顶部导航与主卡片 (Top Nav Integration)
- **移除独立的 `.top-nav`**：取消固定在顶部的深色或高对比度的独立导航栏。
- **将导航元素融入面板**：
  - 左上角：放置“返回花名册”面包屑/按钮。
  - 右上角：放置“导出档案”、“编辑信息”等操作按钮。
- **取消粘性定位 (Sticky)**：不再需要占用屏幕顶部的固定空间，让内容随页面滚动。

### 2.2 重构卡片内部布局 (Internal Layout Restructuring) - 方案 C (白底信息面板)
- **视觉风格**：去除原来的线性渐变背景 (`linear-gradient`) 和装饰性的伪元素 (`::before`, `::after`)。改用白底 (`background: var(--bg-card)`) 和浅色边框 (`border: 1px solid var(--border)`)，使其看起来像一个普通的、高密度的信息卡片。
- **网格化/横向排列**：
  - **头部区域 (Header)**：包含返回按钮、员工姓名、状态标签（在职、退休返聘等）、右上角的操作按钮。
  - **内容区域 (Body)**：
    - 左侧：头像 (缩小尺寸，如 56px 或 64px)。
    - 中间：关键元数据（如手机号、部门、职位等）以横向或紧凑的 2 列网格排列。
    - 右侧：统计数据（司龄、年龄等）弱化展示，或整合到元数据中。
- **精简次要信息**：确保首屏只展示最高频、最重要的身份识别信息。

### 2.3 调整页面整体间距 (Spacing Optimization)
- **主容器 (`.main-content`)**：可以保持或略微减小 padding（例如 16px - 24px）。
- **面板内边距 (`padding`)**：减小面板内部的上下留白，例如从 `32px` 减小到 `16px 20px`。
- **元素间距 (`gap`)**：减小行与行、列与列之间的间距。
- **字体大小 (`font-size`)**：适当缩小非标题文字的字号。

## 3. 实施细节 (Implementation Plan)

### 3.1 HTML 结构调整
```html
<main class="main-content">
    <!-- 新的白底信息面板 (整合了导航和主卡片) -->
    <section class="employee-hero-panel">
        <div class="panel-header">
            <div class="panel-header-left">
                <a class="back-link">
                    <svg>...</svg> 返回
                </a>
                <h2 class="employee-name">
                    曾强勇
                    <span class="status-badge active">在职</span>
                    <span class="tag tag-orange">退休返聘</span>
                    <span class="tag tag-green">正式</span>
                </h2>
            </div>
            <div class="panel-header-right">
                <button class="btn btn-secondary">导出</button>
                <button class="btn btn-primary">编辑</button>
            </div>
        </div>
        <div class="panel-body">
            <div class="avatar-medium">曾</div>
            <div class="employee-meta-grid">
                <div class="meta-item">
                    <span class="meta-label">手机号码:</span>
                    <span class="meta-value">18575504349</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">入职日期:</span>
                    <span class="meta-value">2025-02-25 (司龄: 13个月)</span>
                </div>
                <div class="meta-item">
                    <span class="meta-label">年龄/性别:</span>
                    <span class="meta-value">30岁 / 男</span>
                </div>
                 <div class="meta-item">
                    <span class="meta-label">国籍:</span>
                    <span class="meta-value">中国</span>
                </div>
            </div>
        </div>
    </section>

    <!-- 下方的 Tabs 保持不变，但间距调整 -->
    <section class="tabs-container">...
```

### 3.2 CSS 样式调整
- 删除旧的 `.top-nav`, `.employee-hero` 及其相关样式。
- 添加新的 `.employee-hero-panel`, `.panel-header`, `.panel-body`, `.employee-meta-grid` 等样式，使用白底、灰字、细边框，符合整体设计系统。

## 4. 确认
该规范文档（Spec）已更新。下一步是调用 `writing-plans` 技能生成具体的实施步骤并应用到 HTML 文件中。