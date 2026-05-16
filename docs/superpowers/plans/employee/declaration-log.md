---
title: 人员报送日志设计重构计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 人员报送日志设计重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `prototype/employee-detail-redesign.html` 中的“人员个税报送”事件变更为“人员报送”事件，并更新相关的下拉选项和详细的字段明细（姓名、证件、主体等）。

**Architecture:** 
1. 在 `.timeline-filters` 中将 `<option value="tax">个税报送</option>` 替换为 `<option value="declaration">人员报送</option>`。
2. 找到时间轴中原本写着“人员个税报送”的 `<div class="timeline-item">`，将其标题和内部的 `.timeline-body` 替换为最新设计的包含 8 个关键人员信息的 `.change-list`。

**Tech Stack:** HTML5

---

### Task 1: 更新筛选器选项

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 修改下拉选项**
找到 `aria-label="筛选操作类型"` 的 `<select>` 标签。
将 `<option value="tax">个税报送</option>` 修改为 `<option value="declaration">人员报送</option>`。

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: update filter option from tax to employee declaration"
```

---

### Task 2: 替换 Timeline Item 内容

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换“人员个税报送”节点**
找到带有 `<span class="timeline-event">人员个税报送</span>` 的 `<div class="timeline-item">`。
将其标题和 `.timeline-body` 部分替换为：
```html
                <!-- 2. 人员报送 -->
                <div class="timeline-item">
                    <div class="timeline-dot green"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">人员报送</span>
                            <span class="timeline-meta">操作人: 系统自动触发</span>
                            <span class="timeline-meta">渠道: 薪税系统接口</span>
                            <span class="timeline-date">2026-03-15 02:00:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note" style="margin-bottom: 12px;">员工基础信息已成功向税务局完成人员信息采集报送。</p>
                            <ul class="change-list" style="background: var(--bg-page); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-light);">
                                <li class="change-item">
                                    <span class="change-field">报送主体:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">无锡优派人力资源服务有限公司</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">姓名:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-weight: 500; color: var(--text-primary);">曾强勇</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">证件类型:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">居民身份证</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">证件号码:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-family: 'SF Mono', Monaco, monospace;">43102319950825181X</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">任职受雇类型:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">雇员</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">任职受雇日期:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">2025-02-25</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">人员状态:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">正常</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">报送状态:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-weight: 600; color: var(--success);">报送成功</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: replace tax declaration audit log with employee declaration"
```