# 个税申报日志详细展示重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `prototype/employee-detail-redesign.html` 中的“人员个税报送”时间轴节点内容，由简单的一句话提示升级为带有深灰色背景的详细结构化数据列表，包括税期、收入、扣除、税额等金额明细。

**Architecture:** 
1. 在原有 `timeline-body` 中，保留 `<p class="timeline-note">`，并在其下方增加一个 `<ul class="change-list">`。
2. 为该 `change-list` 添加内联样式（或专用 CSS 类）以实现报表卡片式的展示。
3. 将相关的税务字段（收入、扣除项、应纳税所得额、应扣缴税额等）转化为 `<li class="change-item">` 键值对结构。

**Tech Stack:** HTML5, CSS3

---

### Task 1: 更新个税申报节点的 HTML 结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 找到并替换“个税报送”的 HTML**
在文件中搜索包含 `人员个税报送` 的 `<div class="timeline-item">` 块。
将其 `.timeline-body` 部分：
```html
                        <div class="timeline-body">
                            <p class="timeline-note">2026年3月个税申报数据已成功同步至税务局接口，申报状态：<strong>申报成功</strong>。</p>
                        </div>
```
替换为以下结构化的列表代码：
```html
                        <div class="timeline-body">
                            <p class="timeline-note" style="margin-bottom: 12px;">2026年3月个税申报数据已成功同步至税务局接口，申报状态：<strong style="color: var(--success);">申报成功</strong>。</p>
                            <ul class="change-list" style="background: var(--bg-page); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-light);">
                                <li class="change-item">
                                    <span class="change-field">税款所属期:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">2026-03</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">申报主体:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">无锡优派人力资源服务有限公司</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">本期收入额:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-weight: 600; color: var(--text-primary);">¥23,000.00</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">本期免税收入:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">¥0.00</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">专项扣除(社保):</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">¥2,500.00</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">专项附加扣除:</span>
                                    <span class="change-val" style="background: transparent; padding: 0;">¥3,000.00</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">应纳税所得额:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-weight: 500;">¥17,500.00</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field">应扣缴税额:</span>
                                    <span class="change-val" style="background: transparent; padding: 0; font-weight: 600; color: var(--danger);">¥525.00</span>
                                </li>
                            </ul>
                        </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: enhance tax declaration audit log with detailed structured fields"
```