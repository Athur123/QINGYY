---
title: 个税报送业务日志混合展示计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 个税报送业务日志混合展示计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在现有的员工动态记录 (Timeline) 中，追加“修改报送信息”和“导入报送信息”这两种与个税档案强相关的日志节点，并在筛选器中增加对应选项。

**Architecture:** 
1. 扩展 `.timeline-filters` 的“操作类型”选项。
2. 在 `.timeline-list` 中插入两个全新的 `<div class="timeline-item">` 节点，分别演示修改个税附加扣除字段（带状态标签）以及批量导入个税信息的场景。

**Tech Stack:** HTML5

---

### Task 1: 扩展筛选器操作类型

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 增加操作类型选项**
找到 `.timeline-filters` 中的 `aria-label="筛选操作类型"` 下拉框。
在最后添加两个选项：
```html
                        <option value="tax_edit">修改报送信息</option>
                        <option value="tax_import">导入报送信息</option>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add tax operation types to timeline filters"
```

---

### Task 2: 插入个税相关的操作日志

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 插入“导入报送信息”与“修改报送信息”节点**
在 `#tab-timeline` 的 `.timeline-list` 中，将以下两个节点插入到合适的位置（比如在“人员报送”和“部门调动”之间，以保持时间上的递减顺序，假设日期在 2026-03 附近）：

```html
                <!-- 1.2 导入报送信息 -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">导入报送信息</span>
                            <span class="timeline-meta">操作人: 财务-李明</span>
                            <span class="timeline-meta">渠道: 批量导入</span>
                            <span class="timeline-date">2026-03-20 11:30:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note">通过模板文件 <code>2026年3月专项附加扣除导入模板.xlsx</code> 更新了员工的个税附加扣除信息。导入状态：<strong style="color: var(--success);">导入成功</strong>。</p>
                        </div>
                    </div>
                </div>

                <!-- 1.3 修改报送信息 -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">修改报送信息</span>
                            <span class="tag tag-gray" style="margin-left: 4px;">待报送</span>
                            <span class="timeline-meta">操作人: 财务-李明</span>
                            <span class="timeline-date">2026-03-18 15:45:00</span>
                        </div>
                        <div class="timeline-body">
                            <ul class="change-list">
                                <li class="change-item">
                                    <span class="change-field" style="min-width: 120px;">残疾烈属孤老人员</span>
                                    <span class="change-val old">否</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">是</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field" style="min-width: 120px;">烈属证号</span>
                                    <span class="change-val old" style="text-decoration: none;">-</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">LS123456789</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: append tax profile edit and import logs to the timeline"
```