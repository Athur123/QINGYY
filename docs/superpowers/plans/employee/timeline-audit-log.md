---
title: 动态记录 (Audit Log Timeline) 重构计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 动态记录 (Audit Log Timeline) 重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将原本仅展示简略日期的 Timeline 模块，重构为一个包含详细“操作人、时间、类型、变更内容 (旧值 -> 新值)”的审计日志流。

**Architecture:** 
- 修改 `.timeline-item` 内部的 HTML 结构，增加 `.timeline-header-row` (用于展示标题、操作人、精确时间) 和 `.timeline-body` (用于展示变更明细)。
- 添加一套新的 CSS 类用于渲染变更前后的字段比对（`.change-list`, `.old-val`, `.new-val` 等）。
- 提供入职、编辑档案、部门调动、离职等多种类型的静态样例。

**Tech Stack:** HTML5, CSS3 (原生 Flexbox)

---

### Task 1: 编写 Timeline Audit Log 相关的 CSS 样式

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 添加新的 Timeline CSS**
在 `<style>` 标签的 `/* 动态记录 */` 部分（约 860 行左右），添加或修改以下样式：

```css
        .timeline-item {
            display: flex;
            gap: 16px;
            padding: 16px 0;
            border-bottom: 1px solid var(--border-light);
            position: relative;
        }

        .timeline-item::before {
            content: '';
            position: absolute;
            left: 4.5px; /* 10px dot / 2 - 0.5px line width */
            top: 36px;
            bottom: -16px;
            width: 1px;
            background: var(--border-light);
            z-index: 0;
        }

        .timeline-item:last-child::before {
            display: none;
        }

        .timeline-dot {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--primary);
            margin-top: 6px;
            flex-shrink: 0;
            position: relative;
            z-index: 1;
        }

        .timeline-dot.orange { background: var(--warning); }
        .timeline-dot.green { background: var(--success); }
        .timeline-dot.blue { background: var(--primary); }
        .timeline-dot.red { background: var(--danger); }

        .timeline-content {
            flex: 1;
            min-width: 0;
        }

        .timeline-header-row {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 12px;
            margin-bottom: 8px;
        }

        .timeline-event {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
        }

        .timeline-meta {
            font-size: 13px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .timeline-meta::before {
            content: '';
            display: block;
            width: 4px;
            height: 4px;
            border-radius: 50%;
            background: var(--border);
        }

        .timeline-meta:first-of-type::before {
            display: none;
        }

        .timeline-date {
            font-size: 13px;
            color: var(--text-muted);
            margin-left: auto;
        }

        .timeline-body {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-sm);
            padding: 12px 16px;
            margin-top: 8px;
        }

        .change-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .change-item {
            font-size: 13px;
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }

        .change-field {
            color: var(--text-secondary);
            min-width: 80px;
        }

        .change-val {
            font-family: 'SF Mono', Monaco, monospace;
            padding: 2px 6px;
            border-radius: 4px;
            background: var(--border-light);
            color: var(--text-primary);
        }

        .change-val.old {
            text-decoration: line-through;
            color: var(--text-muted);
            background: transparent;
            padding: 0;
        }

        .change-val.new {
            background: #ECFDF5;
            color: #059669;
        }

        .change-arrow {
            color: var(--text-muted);
            display: flex;
            align-items: center;
        }
        
        .timeline-note {
            font-size: 13px;
            color: var(--text-primary);
            line-height: 1.5;
            margin: 0;
        }
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: add css for detailed timeline audit logs"
```

---

### Task 2: 替换 Timeline 的 HTML 结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 删除旧的 `.timeline-list` 内容**
找到 `<div class="timeline-list">`，删除其内部所有的 `<div class="timeline-item">...</div>`。

- [ ] **Step 2: 插入详细的审计日志样例**
将以下结构插入到 `<div class="timeline-list">` 中：

```html
                <!-- 1. 修改档案 -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">修改人员档案</span>
                            <span class="timeline-meta">操作人: 张HR (管理员)</span>
                            <span class="timeline-date">2026-04-22 14:30:00</span>
                        </div>
                        <div class="timeline-body">
                            <ul class="change-list">
                                <li class="change-item">
                                    <span class="change-field">手机号码</span>
                                    <span class="change-val old">13800138000</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">18575504349</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">政治面貌</span>
                                    <span class="change-val old">群众</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">中共党员</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 2. 个税报送 -->
                <div class="timeline-item">
                    <div class="timeline-dot green"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">人员个税报送</span>
                            <span class="timeline-meta">操作人: 系统自动触发</span>
                            <span class="timeline-meta">渠道: 薪税系统接口</span>
                            <span class="timeline-date">2026-03-15 02:00:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note">2026年3月个税申报数据已成功同步至税务局接口，申报状态：<strong>申报成功</strong>。</p>
                        </div>
                    </div>
                </div>

                <!-- 3. 部门调动 -->
                <div class="timeline-item">
                    <div class="timeline-dot orange"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">部门调动</span>
                            <span class="timeline-meta">操作人: 李总监</span>
                            <span class="timeline-date">2026-02-01 10:15:30</span>
                        </div>
                        <div class="timeline-body">
                            <ul class="change-list">
                                <li class="change-item">
                                    <span class="change-field">所属部门</span>
                                    <span class="change-val old">研发中心 / 前端部</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">创新业务部 / 架构组</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">汇报对象</span>
                                    <span class="change-val old">王主管</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">李总监</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 4. 转正 -->
                <div class="timeline-item">
                    <div class="timeline-dot green"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">转正审批通过</span>
                            <span class="timeline-meta">操作人: 王主管</span>
                            <span class="timeline-date">2025-08-25 16:00:00</span>
                        </div>
                        <div class="timeline-body">
                            <ul class="change-list">
                                <li class="change-item">
                                    <span class="change-field">员工状态</span>
                                    <span class="change-val old">试用期</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">正式</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>

                <!-- 5. 首次入职 -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">员工入职</span>
                            <span class="timeline-meta">操作人: 张HR</span>
                            <span class="timeline-date">2025-02-25 09:00:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note">创建员工档案，完成首次入职登记。</p>
                        </div>
                    </div>
                </div>
```

- [ ] **Step 3: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: implement detailed audit log timeline structure and examples"
```

---

### Task 3: 适配移动端样式

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 添加移动端响应式 CSS**
在 `<style>` 标签的 `@media (max-width: 768px)` 中添加：
```css
            .timeline-header-row {
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }
            .timeline-date {
                margin-left: 0;
            }
            .timeline-meta::before {
                display: none;
            }
            .timeline-meta {
                flex-direction: column;
                align-items: flex-start;
                gap: 2px;
            }
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: add mobile responsive styles for timeline audit log"
```