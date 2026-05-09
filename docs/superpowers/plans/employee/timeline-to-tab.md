# 动态记录 Tab 化重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将原本在右侧边栏展示的“动态记录”模块移入左侧主 Tab 区域中，作为第 12 个 Tab 存在，并彻底移除双列网格布局，使页面成为单列全宽结构。

**Architecture:** 
1. 移除 `.content-layout` 的 CSS 网格定义，使其表现为普通块级元素（或者直接将其简化为 `display: block`）。
2. 在 `.tabs-nav` 尾部增加 `data-tab="11"` 的“动态记录”按钮。
3. 将 `<section class="timeline-section">` 从 `<div class="summary-section">` 剪切，用一个 `<div class="tab-panel">` 包裹后，放入 `.tab-content` 的末尾。
4. 移除多余的“查看全部”折叠逻辑和无用的右侧边栏包裹层。

**Tech Stack:** HTML, CSS, JavaScript (原生)

---

### Task 1: 更新 CSS 布局以移除侧边栏

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 移除 `.content-layout` 的两列网格布局**
找到 CSS 中的 `.content-layout`：
```css
        /* 左右布局容器 */
        .content-layout {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 24px;
            align-items: start;
        }
```
修改为单列块级（或直接保留 `display: block`，移除 `grid-template-columns` 和 `gap`）：
```css
        /* 主体内容布局容器 (已转为单列) */
        .content-layout {
            display: block;
            width: 100%;
        }
```

- [ ] **Step 2: 移除右侧边栏相关 CSS（可选清理）**
如果 CSS 中有专门针对 `.summary-section` 的样式，可以一并删除。同时找到并移除对 `.timeline-section` 原本右侧面板专属的样式（如固定宽度限制等），因为现在它将要在主区域全宽展示。

修改 `.timeline-section`：
```css
        .timeline-section {
            background: var(--bg-card);
            border-radius: var(--radius-md);
            padding: 24px;
            border: 1px solid var(--border);
            height: 100%; /* 移除原来可能的限制，或保持原样即可 */
        }
```
*注：由于放入 Tab 中，我们其实可以直接把它的边框和背景去掉，与外层 `.tab-panel` 融合，或者保留作为信息卡片。这里我们保留原有的卡片外观。*

- [ ] **Step 3: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: remove two-column grid layout for content-layout"
```

---

### Task 2: 增加新的 Tab 导航项

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 在 `.tabs-nav` 中追加按钮**
在 HTML 结构中，找到 `<div class="tabs-nav">`。
在 `<button class="tab-item" data-tab="10">参保档案</button>` 的下一行，插入：
```html
                            <button class="tab-item" data-tab="11">动态记录</button>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add dynamic records tab navigation item"
```

---

### Task 3: 移动并重构 Timeline HTML 结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 移动 `.timeline-section`**
1. 找到页面底部的 `<div class="summary-section">` 及其包含的 `<section class="timeline-section" id="timelineSection">`。
2. 将整个 `<section class="timeline-section" id="timelineSection">...</section>` 剪切出来。
3. 删除空的 `<div class="summary-section"></div>`。
4. 删除包裹左侧内容的 `<div class="detail-section">` 闭合标签 `</div><!-- /.detail-section -->` 及其开标签（不再需要内层包裹）。
5. 将剪切出的 timeline 内容用 `<div class="tab-panel">` 包裹，粘贴到 `.tab-content` 内部的最后面（在参保档案面板之后，最后的 `</div>` 之前）。

结构应该变为：
```html
        <div class="content-layout">
            <!-- Tab导航 -->
            <section class="tabs-container">
                <div class="tabs-header">...</div>
                <div class="tab-content">
                    <!-- 基础信息Tab -->
                    <div class="tab-panel active">...</div>
                    <!-- 其他现有的Tab面板 -->
                    ...
                    <!-- 参保档案 Tab 面板 (这里通常是一个占位的空 div 或已有内容) -->
                    <div class="tab-panel">
                        <div class="empty-state">
                            <div class="empty-icon">...</div>
                            <p>暂无参保档案信息</p>
                        </div>
                    </div>

                    <!-- 新增的 动态记录 Tab -->
                    <div class="tab-panel">
                        <section class="timeline-section" id="timelineSection">
                            <!-- 原有的 timeline 内容 -->
                            <div class="timeline-header">...</div>
                            <div class="timeline-list">...</div>
                        </section>
                    </div>
                </div> <!-- /.tab-content -->
            </section>
        </div> <!-- /.content-layout -->
```

- [ ] **Step 2: 移除 Timeline 的折叠逻辑（可选/推荐）**
因为在独立的 Tab 中，不再受限于右侧栏的高度。
1. 移除 HTML 中的 `<button class="timeline-toggle" onclick="toggleTimeline()">...</button>`。
2. 移除 CSS 中对于 `.timeline-hidden` 的 `display: none` 控制（或者直接在 HTML 的 `timeline-item` 节点上删除 `timeline-hidden` 类）。
3. 删除 JavaScript 中底部的 `function toggleTimeline()` 声明。

- [ ] **Step 3: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: move timeline section into a new tab panel"
```