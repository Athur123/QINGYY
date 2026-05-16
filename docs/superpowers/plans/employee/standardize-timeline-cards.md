---
title: 统一异动记录为卡片样式实施计划
module: employee
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 统一异动记录为卡片样式实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 `prototype/employee-detail-redesign.html` 中的所有动态记录节点（如单条字段修改、个税报送、转正、入职等）都包裹进 `.sub-record-card`，并在头部标明“新增”、“编辑”等状态。

**Architecture:** 
1. 遍历现存的所有 `.timeline-item`。
2. 保持 `.timeline-event`, `.timeline-meta`, `.timeline-date` 不变。
3. 将 `.timeline-body` 内的 `.change-list` 或说明文字，放入一个新的 `.sub-record-list` > `.sub-record-card` 结构中。
4. 为每个卡片添加带有 `tag-green` (新增) 或 `tag-blue` (编辑) 的 `.sub-record-header`。

**Tech Stack:** HTML5

---

### Task 1: 统一所有记录节点的内部结构

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换 1. 修改档案 (暂不报送)**
将 `.timeline-body` 替换为卡片嵌套格式：
```html
                        <div class="timeline-body">
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>基础信息</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item">
                                                <span class="change-field">手机号码</span>
                                                <span class="change-val old">13800138000</span>
                                                <span class="change-arrow">
                                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                                                </span>
                                                <span class="change-val new">18575504349</span>
                                            </li>
                                            <li class="change-item">
                                                <span class="change-field">政治面貌</span>
                                                <span class="change-val old">群众</span>
                                                <span class="change-arrow">
                                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                                                </span>
                                                <span class="change-val new">中共党员</span>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 2: 替换 2. 人员报送**
```html
                        <div class="timeline-body">
                            <p class="timeline-note">员工基础信息已成功向税务局完成人员信息采集报送。</p>
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-green">新增</span>
                                        <span>人员报送信息</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item"><span class="change-field">报送主体:</span><span class="change-val" style="background: transparent; padding: 0;">无锡优派人力资源服务有限公司</span></li>
                                            <li class="change-item"><span class="change-field">姓名:</span><span class="change-val" style="background: transparent; padding: 0; font-weight: 500; color: var(--text-primary);">曾强勇</span></li>
                                            <li class="change-item"><span class="change-field">证件类型:</span><span class="change-val" style="background: transparent; padding: 0;">居民身份证</span></li>
                                            <li class="change-item"><span class="change-field">证件号码:</span><span class="change-val" style="background: transparent; padding: 0; font-family: 'SF Mono', Monaco, monospace;">43102319950825181X</span></li>
                                            <li class="change-item"><span class="change-field">任职受雇类型:</span><span class="change-val" style="background: transparent; padding: 0;">雇员</span></li>
                                            <li class="change-item"><span class="change-field">任职受雇日期:</span><span class="change-val" style="background: transparent; padding: 0;">2025-02-25</span></li>
                                            <li class="change-item"><span class="change-field">人员状态:</span><span class="change-val" style="background: transparent; padding: 0;">正常</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 3: 替换 1.2 导入报送信息**
```html
                        <div class="timeline-body">
                            <p class="timeline-note">通过模板文件 <code>2026年3月专项附加扣除导入模板.xlsx</code> 更新了员工的个税附加扣除信息。</p>
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>个税专项附加扣除</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item"><span class="change-field" style="min-width: 160px;">专项附加扣除-子女教育</span><span class="change-val old">否</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">是</span></li>
                                            <li class="change-item"><span class="change-field" style="min-width: 160px;">专项附加扣除-住房贷款利息</span><span class="change-val old">否</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">是</span></li>
                                            <li class="change-item"><span class="change-field" style="min-width: 160px;">专项附加扣除-赡养老人</span><span class="change-val old" style="text-decoration: none; color: var(--text-primary);">是</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new" style="background: transparent; color: var(--text-primary);">是</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 4: 替换 1.3 修改报送信息**
```html
                        <div class="timeline-body">
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>个税附加扣除</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item"><span class="change-field" style="min-width: 120px;">残疾烈属孤老人员</span><span class="change-val old">否</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">是</span></li>
                                            <li class="change-item"><span class="change-field" style="min-width: 120px;">烈属证号</span><span class="change-val old" style="text-decoration: none;">-</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">LS123456789</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 5: 替换 3. 部门调动**
```html
                        <div class="timeline-body">
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>任职信息</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item"><span class="change-field">所属部门</span><span class="change-val old">研发中心 / 前端部</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">创新业务部 / 架构组</span></li>
                                            <li class="change-item"><span class="change-field">汇报对象</span><span class="change-val old">王主管</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">李总监</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 6: 替换 4. 转正 & 5. 入职**
```html
                        <!-- 转正 body -->
                        <div class="timeline-body">
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-blue">编辑</span>
                                        <span>任职信息</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <ul class="change-list">
                                            <li class="change-item"><span class="change-field">员工状态</span><span class="change-val old">试用期</span><span class="change-arrow"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg></span><span class="change-val new">正式</span></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 入职 body -->
                        <div class="timeline-body">
                            <div class="sub-record-list">
                                <div class="sub-record-card">
                                    <div class="sub-record-header">
                                        <span class="tag tag-green">新增</span>
                                        <span>员工档案</span>
                                    </div>
                                    <div class="sub-record-body">
                                        <p class="timeline-note" style="margin: 0;">创建员工档案，完成首次入职登记。</p>
                                    </div>
                                </div>
                            </div>
                        </div>
```

- [ ] **Step 7: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: wrap all timeline logs in sub-record-cards with explicit action tags"
```