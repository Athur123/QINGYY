---
title: 动态记录筛选栏 (Timeline Filters) 重构计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 动态记录筛选栏 (Timeline Filters) 重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在动态记录 (Timeline) 模块顶部添加内联下拉筛选器（时间、操作类型、字段、操作人），并优化头部样式使其适配紧凑排版。

**Architecture:** 
1. 增加 `.timeline-filters` 的 Flex 布局 CSS 及其子元素的紧凑输入框样式 (`.filter-control`)。
2. 更改 `.timeline-header` 结构，将原有的水平排列变更为垂直排列（上：标题；下：筛选栏）。
3. 插入包含 4 个筛选维度的 HTML。

**Tech Stack:** HTML5, CSS3

---

### Task 1: 编写筛选器 CSS 样式

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 更新 Timeline Header CSS**
在 `<style>` 中找到 `.timeline-header` (约 840 行左右)。将其原有样式：
```css
        .timeline-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
```
修改为支持垂直多行的布局：
```css
        .timeline-header {
            padding: 16px 20px;
            border-bottom: 1px solid var(--border-light);
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .timeline-header-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
```

- [ ] **Step 2: 添加紧凑筛选控件 CSS**
在紧接着 `.timeline-header` 后方，添加 `.timeline-filters` 及相关控件样式：
```css
        .timeline-filters {
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .filter-control {
            padding: 6px 12px;
            height: 32px;
            font-size: 13px;
            border: 1px solid var(--border);
            border-radius: var(--radius-sm);
            color: var(--text-primary);
            background-color: var(--bg-card);
            min-width: 140px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .filter-control:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
```

- [ ] **Step 3: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: add css for timeline header and inline filters"
```

---

### Task 2: 插入筛选栏 HTML 结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换 Timeline Header HTML**
在 `#tab-timeline` 面板中找到现有的 `.timeline-header`：
```html
            <div class="timeline-header">
                <div class="timeline-title">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    动态记录
                    <span class="timeline-count">20条</span>
                </div>

            </div>
```
替换为带有筛选器的新结构：
```html
            <div class="timeline-header">
                <div class="timeline-header-top">
                    <div class="timeline-title">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <circle cx="12" cy="12" r="10"/>
                            <polyline points="12 6 12 12 16 14"/>
                        </svg>
                        动态记录
                        <span class="timeline-count">20条</span>
                    </div>
                </div>
                
                <div class="timeline-filters">
                    <input type="month" class="filter-control" aria-label="筛选时间" title="选择月份">
                    
                    <select class="filter-control" aria-label="筛选操作类型">
                        <option value="">全部操作类型</option>
                        <option value="onboard">员工入职</option>
                        <option value="edit">修改人员档案</option>
                        <option value="transfer">部门调动</option>
                        <option value="regular">转正审批</option>
                        <option value="tax">个税报送</option>
                    </select>

                    <select class="filter-control" aria-label="筛选操作人">
                        <option value="">全部操作人</option>
                        <option value="admin">系统管理员</option>
                        <option value="hr">张HR</option>
                        <option value="manager">王主管</option>
                        <option value="system">系统自动触发</option>
                    </select>
                    
                    <select class="filter-control" aria-label="筛选变更字段">
                        <option value="">全部变更字段</option>
                        <option value="phone">手机号码</option>
                        <option value="dept">所属部门</option>
                        <option value="status">员工状态</option>
                        <option value="politic">政治面貌</option>
                    </select>
                </div>
            </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: implement inline dropdown filters for audit log timeline"
```