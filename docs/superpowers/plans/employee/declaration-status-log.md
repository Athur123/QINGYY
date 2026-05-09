# 增加编辑人员档案的报送状态展示计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在“动态记录”时间轴中的“修改人员档案”事件标题旁边，增加对应的报送状态徽标（如“未报送”、“报送成功”）。

**Architecture:** 
1. 找到目前的“修改人员档案”记录节点。
2. 在其 `.timeline-event` 标题旁边，插入一个使用 `.tag` 样式的状态徽标。
3. 复制当前的修改记录节点，并制作两份不同的日志示例：
   - 示例一：修改人员档案，但“暂不报送”（显示灰色 tag）。
   - 示例二：修改人员档案，并“报送成功”（显示绿色 tag），附带税务响应说明。

**Tech Stack:** HTML5

---

### Task 1: 扩展 Timeline HTML 内容以展示不同报送状态

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换现有的“修改人员档案”并新增示例**
定位到 `<!-- 1. 修改档案 -->` 部分的 `.timeline-item`。
将其整体替换为两个不同的修改节点，展示“未报送”和“报送成功”两种状态。

```html
                <!-- 1. 修改档案 (暂不报送) -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">修改人员档案</span>
                            <span class="tag tag-gray" style="margin-left: 4px;">未报送</span>
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

                <!-- 1.1 修改档案 (报送成功) -->
                <div class="timeline-item">
                    <div class="timeline-dot blue"></div>
                    <div class="timeline-content">
                        <div class="timeline-header-row">
                            <span class="timeline-event">修改人员档案</span>
                            <span class="tag tag-green" style="margin-left: 4px;">报送成功</span>
                            <span class="timeline-meta">操作人: 王主管</span>
                            <span class="timeline-date">2026-04-10 10:15:00</span>
                        </div>
                        <div class="timeline-body">
                            <p class="timeline-note" style="margin-bottom: 8px;">修改了员工核心基础信息，并同步触发了人员信息报送。税务局接口返回：处理成功。</p>
                            <ul class="change-list">
                                <li class="change-item">
                                    <span class="change-field">学历</span>
                                    <span class="change-val old">本科</span>
                                    <span class="change-arrow">
                                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                            <line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>
                                        </svg>
                                    </span>
                                    <span class="change-val new">硕士</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
```

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "feat: add submission status tags to employee profile modification audit logs"
```