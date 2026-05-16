---
title: 批量多条目操作日志展示计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 批量多条目操作日志展示计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在动态记录 (Timeline) 中，增加一个支持“批量多条目（Collection）变更”的展现样式。通过嵌套子卡片 (`.sub-record-card`)，在同一个 Timeline 节点内展示多个家庭成员、教育经历等对象的新增、编辑和删除操作。

**Architecture:** 
1. 增加针对 `.sub-record-list`, `.sub-record-card`, `.sub-record-header`, 和 `.sub-record-body` 的 CSS 样式。
2. 在 Timeline 中插入一个模拟批量更新家庭成员及联系人的节点，演示同一个操作下包含三个子操作（新增一个家庭成员、编辑一个紧急联系人、删除一个家庭成员）的界面。

**Tech Stack:** HTML5, CSS3

---

### Task 1: 添加嵌套卡片的 CSS 样式

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 插入子卡片 CSS**
在 `<style>` 标签的末尾，添加针对 `sub-record` 相关的样式：
```css
        /* 嵌套子卡片 (用于批量多条目变更) */
        .sub-record-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 12px;
        }

        .sub-record-card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            overflow: hidden;
        }

        .sub-record-header {
            padding: 10px 16px;
            border-bottom: 1px solid var(--border-light);
            background: var(--bg-page);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            font-weight: 500;
            color: var(--text-primary);
        }

        .sub-record-body {
            padding: 12px 16px;
        }

        /* 调整子卡片内部的 change-list 样式 */
        .sub-record-body .change-list {
            background: transparent;
            padding: 0;
            border: none;
        }
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: add css for nested sub-record cards in timeline"
```

---

### Task 2: 插入批量操作日志节点示例

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 添加 HTML 示例**
在 `#tab-timeline` 的 `.timeline-list` 中，插入一个新的 `timeline-item`，模拟批量更新：

```html
                <!-- 1.4 批量更新 (家庭成员) -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">更新家庭及联系人信息</span>
                            <span class="timeline-meta">操作人: 张HR</span>
                            <span class="timeline-date">2026-03-10 14:00:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note">批量更新了员工的家庭成员及紧急联系人信息。</p>
                            
                            <div class="sub-record-list">
                                <!-- 卡片1：新增 -->
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-green">新增</span>
                                        <span>家庭成员：李四 (父亲)</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item">
                                                <span class="change-field">联系电话:</span>
                                                <span class="change-val new" style="background: transparent;">13800001111</span>
                                            </li>
                                            <li class="change-item">
                                                <span class="change-field">工作单位:</span>
                                                <span class="change-val new" style="background: transparent;">无锡市某某公司</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>

                                <!-- 卡片2：编辑 -->
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>紧急联系人：王五 (配偶)</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item">
                                                <span class="change-field">联系电话</span>
                                                <span class="change-val old">13900002222</span>
                                                <span class="change-arrow">
                                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                                        <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                                    </svg>
                                                </span>
                                                <span class="change-val new">18600003333</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>

                                <!-- 卡片3：删除 -->
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-red" style="color: var(--danger); background: rgba(239, 68, 68, 0.1);">删除</span>
                                        <span style="text-decoration: line-through; color: var(--text-muted);">家庭成员：赵六 (兄弟姐妹)</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add nested sub-record cards example for batch timeline operations"
```