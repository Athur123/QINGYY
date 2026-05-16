---
title: 员工详情页主卡片（Hero Section）优化实现计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 员工详情页主卡片（Hero Section）优化实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有的高占用、渐变背景的员工主卡片及顶部导航重构为紧凑的、白底的、网格化布局的信息面板，以提升首屏空间利用率。

**Architecture:**
- 移除原有的 `.top-nav` 和 `.employee-hero` 结构及其对应的 CSS。
- 引入新的 `.employee-hero-panel` 结构，将“返回”操作、页面操作按钮（编辑、导出）以及员工核心信息整合在同一个白底面板中。
- 采用 CSS Flexbox 和 CSS Grid 实现内部的紧凑横向排版。

**Tech Stack:** HTML5, 原生 CSS, SVG 图标

---

### Task 1: 清理旧的结构与样式

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/prototype/employee-detail-redesign.html`

- [ ] **Step 1: 删除旧的 CSS 样式**
删除 `<style>` 标签内的以下相关区块：
- `/* 顶部导航 */` 及其下的 `.top-nav`, `.back-btn`, `.page-title`, `.nav-actions` 样式。
- `/* 员工主卡片 */` 及其下的 `.employee-hero`, `.hero-content`, `.avatar-large`, `.hero-info`, `.hero-name`, `.hero-meta`, `.hero-stats`, `.stat-item`, `.stat-value`, `.stat-label`, `.hero-actions`, `.btn-hero` 等相关样式。

- [ ] **Step 2: 删除旧的 HTML 结构**
在 `<body>` 中：
- 找到并删除 `<nav class="top-nav">...</nav>`。
- 找到并删除 `<section class="employee-hero">...</section>`。

- [ ] **Step 3: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: remove old hero section and top nav"
```

---

### Task 2: 编写新的 CSS 样式

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/prototype/employee-detail-redesign.html`

- [ ] **Step 1: 添加新的 CSS 代码**
在 `<style>` 标签的合适位置（原主卡片样式所在处）插入以下代码：

```css
        /* 整合式主卡片面板 */
        .employee-hero-panel {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            border: 1px solid var(--border);
            margin-bottom: 16px;
            overflow: hidden;
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-light);
            background: var(--bg-card);
        }

        .panel-header-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 14px;
            cursor: pointer;
            transition: color 0.2s;
        }

        .back-link:hover {
            color: var(--primary);
        }

        .back-link svg {
            width: 16px;
            height: 16px;
        }

        .divider-vertical {
            width: 1px;
            height: 16px;
            background: var(--border);
        }

        .employee-name-header {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 0;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
            background: var(--border-light);
            color: var(--text-secondary);
        }

        .status-badge.active {
            background: #ECFDF5;
            color: #059669;
        }

        .panel-header-right {
            display: flex;
            gap: 8px;
        }

        .panel-body {
            padding: 20px;
            display: flex;
            gap: 24px;
            align-items: center;
        }

        .avatar-medium {
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--primary-light);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            font-weight: 600;
            flex-shrink: 0;
        }

        .employee-meta-grid {
            flex: 1;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px 24px;
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
        }

        .meta-label {
            color: var(--text-secondary);
            min-width: 60px;
        }

        .meta-value {
            color: var(--text-primary);
            font-weight: 500;
        }

        .meta-value-light {
            color: var(--text-muted);
            font-size: 12px;
            margin-left: 4px;
            font-weight: 400;
        }
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: add new employee hero panel css"
```

---

### Task 3: 插入新的 HTML 结构

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/prototype/employee-detail-redesign.html`

- [ ] **Step 1: 添加新的面板 HTML**
在 `<main class="main-content">` 内部，在 `<!-- Tab导航 -->` (`<section class="tabs-container">`) 之前，插入以下代码：

```html
        <!-- 新的白底信息面板 -->
        <section class="employee-hero-panel">
            <div class="panel-header">
                <div class="panel-header-left">
                    <a class="back-link">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M19 12H5M12 19l-7-7 7-7"/>
                        </svg>
                        返回花名册
                    </a>
                    <div class="divider-vertical"></div>
                    <h2 class="employee-name-header">
                        曾强勇
                        <span class="status-badge active">在职</span>
                        <span class="tag tag-orange">退休返聘</span>
                        <span class="tag tag-green">正式</span>
                    </h2>
                </div>
                <div class="panel-header-right">
                    <button class="btn btn-secondary">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
                        </svg>
                        导出档案
                    </button>
                    <button class="btn btn-primary">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                        编辑信息
                    </button>
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
                        <span class="meta-value">2025-02-25 <span class="meta-value-light">(司龄: 13个月)</span></span>
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
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add compact white hero panel HTML"
```

---

### Task 4: 调整整体页面间距 (Spacing Tuning)

**Files:**
- Modify: `/Users/athur/PycharmProjects/qyy/prototype/employee-detail-redesign.html`

- [ ] **Step 1: 调整 `.main-content` 的 padding**
将 `.main-content` 的 `padding: 24px;` 修改为 `padding: 16px 24px;`。

- [ ] **Step 2: 调整 `.tabs-container` 的外边距**
检查 `.tabs-container` 的 `margin-bottom`，如有需要，可将其稍微减小以配合整体紧凑感（可选，若已合适则跳过）。

- [ ] **Step 3: 响应式适配微调**
在 `@media (max-width: 768px)` 媒体查询中，添加或修改针对新面板的样式：
```css
            .panel-header {
                flex-direction: column;
                align-items: flex-start;
                gap: 16px;
            }
            .panel-header-right {
                width: 100%;
            }
            .panel-header-right .btn {
                flex: 1;
                justify-content: center;
            }
            .panel-body {
                flex-direction: column;
                align-items: flex-start;
            }
```

- [ ] **Step 4: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: adjust overall spacing and responsive layout for new hero panel"
```