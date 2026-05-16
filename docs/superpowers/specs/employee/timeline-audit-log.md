---
title: 动态记录 (Timeline) 模块详细设计与重构
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 动态记录 (Timeline) 模块详细设计与重构

## 1. 目标
在已有的“动态记录”Tab中，将原本仅有简单“日期+事件名称”的时间轴（Timeline）升级为一个**包含详尽变更信息的业务审计日志**。
这些记录将涵盖员工档案生命周期中的各类操作：入职、离职、调动、转正、重新入职、编辑档案、人员个税报送等。

## 2. 需求分析与数据结构
每个 Timeline 节点需要展示以下信息：
1. **操作时间**：精确到分钟（如 `2026-01-26 14:30`）。
2. **操作类型 / 变动原因**：例如 `转正审批`、`档案编辑`、`部门调动`。
3. **操作人**：谁执行了该操作（如 `系统管理员` 或 `HR-李四`）。
4. **变更内容详情**：如果修改了具体字段，展示“变更前”与“变更后”的对比。

## 3. UI 视觉设计 (Timeline 方案)

由于采用了时间轴形式，我们将在原本的基础上对 `.timeline-content` 进行扩展：

### 3.1 时间轴基础结构
- 左侧保持原有的带颜色的点（`timeline-dot`）和竖线（`border-left` 或嵌套结构）。
  - **颜色语义**：入职/转正 (Green), 调动/编辑 (Blue), 离职 (Orange/Red)。
- 右侧内容区变为一个**气泡卡片**或**结构化的块** (`timeline-card`)。

### 3.2 节点内容排版
```html
<div class="timeline-item">
    <div class="timeline-dot blue"></div>
    <div class="timeline-content">
        <div class="timeline-header-row">
            <span class="timeline-event">修改人员档案</span>
            <span class="timeline-meta">操作人: 张HR</span>
            <span class="timeline-date">2026-01-26 14:30:00</span>
        </div>
        <div class="timeline-body">
            <!-- 详细变更列表 -->
            <ul class="change-list">
                <li><span class="change-field">手机号码:</span> <span class="old-val">13800000000</span> <svg class="arrow">...</svg> <span class="new-val">18575504349</span></li>
                <li><span class="change-field">政治面貌:</span> <span class="old-val">群众</span> <svg class="arrow">...</svg> <span class="new-val">党员</span></li>
            </ul>
        </div>
    </div>
</div>
```

### 3.3 CSS 样式优化点
- 增加 `.timeline-header-row` 的 Flex 布局，使事件标题、操作人、时间横向对齐（移动端可折行）。
- 增加 `.change-list` 样式，用于清晰呈现 `A -> B` 的字段级变更。
- 为不同类型的事件（入职、调动、离职等）配备不同的背景色或边框标识，以增加可读性。

## 4. 实施范围
修改文件：`prototype/employee-detail-redesign.html`
范围：仅针对 ID 为 `tab-timeline` 下的 `.timeline-section` 内容进行静态原型的覆盖重写，展示至少 4 种不同类型的操作样例（如：入职、档案修改、部门调动、个税报送）。

---
请确认这份设计草案是否满足您对动态记录的要求？确认后我将进入实施阶段。