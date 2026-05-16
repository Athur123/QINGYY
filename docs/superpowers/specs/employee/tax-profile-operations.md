---
title: 个税档案操作记录设计 (Audit Log - Tax Profile Operations)
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 个税档案操作记录设计 (Audit Log - Tax Profile Operations)

## 1. 目标
在已有的员工动态记录 (Timeline) 中，追加支持与“个税档案”相关的系列操作日志。
所有的记录都混合在同一个时间轴内展示，但在**筛选器**和**日志卡片**中体现其特有的业务属性。

## 2. 需求分析与操作类型
用户指出，个税档案的维护包括多种动作：
1. **修改人员档案** (已实现)
2. **人员报送** (已实现)
3. **修改报送信息**: 针对即将在个税系统中报送的具体业务字段的修改。
4. **导入报送信息**: 通过 Excel 等外部文件批量导入/更新个税报送数据。

## 3. UI 扩展与修改

### 3.1 筛选器扩展
在现有的“操作类型”下拉框 (`<select aria-label="筛选操作类型">`) 中，追加以下选项：
- `<option value="tax_edit">修改报送信息</option>`
- `<option value="tax_import">导入报送信息</option>`

### 3.2 日志节点示例增加
在 `.timeline-list` 中插入两个新的节点以展示这些操作：

**示例 1：导入报送信息**
- 节点颜色：蓝色 (`timeline-dot blue`)
- 标题：`导入报送信息`
- 内容：展示通过 Excel 导入的文件名及导入结果汇总。
```html
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
```

**示例 2：修改报送信息**
- 节点颜色：蓝色 (`timeline-dot blue`)
- 标题：`修改报送信息`
- 状态标签：带有一个 `tag-gray` (未报送) 或者 `tag-green` (报送成功) 标签（沿用我们之前的逻辑，因为修改了报送信息，后续还需要报送）。
- 内容：展示个税特有字段的旧值与新值比对。
```html
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
                    <span class="change-field">残疾烈属孤老人员:</span>
                    <span class="change-val old">否</span>
                    <span class="change-arrow">...</span>
                    <span class="change-val new">是</span>
                </li>
                <li class="change-item">
                    <span class="change-field">烈属证号:</span>
                    <span class="change-val old">无</span>
                    <span class="change-arrow">...</span>
                    <span class="change-val new">LS123456789</span>
                </li>
            </ul>
        </div>
    </div>
</div>
```

## 4. 下一步
请确认上述筛选器选项的补充，以及这两类新增个税操作日志的样式排版设计。确认后我将直接生成代码实施计划并执行修改。