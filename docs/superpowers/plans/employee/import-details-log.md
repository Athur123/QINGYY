---
title: 增加导入报送信息明细的实施计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 增加导入报送信息明细的实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `prototype/employee-detail-redesign.html` 中的“导入报送信息”节点，补充显示该员工在导入时实际更新的字段级明细（专项附加扣除等）。

**Architecture:** 
- 找到对应的 `.timeline-body`。
- 修改其提示文本，删除“导入状态：导入成功”字样。
- 追加带有灰色背景的 `<ul class="change-list">` 以展示 3 个附加扣除字段的“旧值 -> 新值”比对情况。

**Tech Stack:** HTML5

---

### Task 1: 补充导入报送信息的明细结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换“导入报送信息”的 Body 内容**
定位到 `<!-- 1.2 导入报送信息 -->` 下方的 `.timeline-body`：
```html
                        <div class="timeline-body">
                            <p class="timeline-note">通过模板文件 <code>2026年3月专项附加扣除导入模板.xlsx</code> 更新了员工的个税附加扣除信息。导入状态：<strong style="color: var(--success);">导入成功</strong>。</p>
                        </div>
```
将其替换为以下包含 `change-list` 明细的内容：
```html
                        <div class="timeline-body">
                            <p class="timeline-note" style="margin-bottom: 12px;">通过模板文件 <code>2026年3月专项附加扣除导入模板.xlsx</code> 更新了员工的个税附加扣除信息。</p>
                            <ul class="change-list" style="background: var(--bg-page); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-light);">
                                <li class="change-item">
                                    <span class="change-field" style="min-width: 160px;">专项附加扣除-子女教育</span>
                                    <span class="change-val old">否</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">是</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field" style="min-width: 160px;">专项附加扣除-住房贷款利息</span>
                                    <span class="change-val old">否</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">是</span>
                                </li>
                                <li class="change-item">
                                    <span class="change-field" style="min-width: 160px;">专项附加扣除-赡养老人</span>
                                    <span class="change-val old" style="text-decoration: none; color: var(--text-primary);">是</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new" style="background: transparent; color: var(--text-primary);">是</span>
                                </li>
                            </ul>
                        </div>
```
*(注意：第三个“赡养老人”展示的是导入前后值一致的场景，所以未划掉线也没有绿底高亮)*

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add detailed field changes to import tax declaration log"
```