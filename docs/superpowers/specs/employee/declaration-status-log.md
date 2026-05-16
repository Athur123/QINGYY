---
title: 人员报送状态扩展设计方案 (Audit Log - Declaration Status)
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 人员报送状态扩展设计方案 (Audit Log - Declaration Status)

## 1. 目标
在已有的动态记录 (Timeline) 中，为“修改人员档案”操作增加报送维度的状态展示。
用户可以对人员档案进行编辑，但**编辑后不一定立即报送**，或者可能**报送失败**。因此，需要在现有的“修改人员档案”日志节点中，明确呈现本次操作的**报送状态**。

## 2. 状态定义与展示

当发生档案修改时，事件标题统一为：**修改人员档案**。
我们需要在日志头部的元信息 (`.timeline-meta`) 或是下方的说明文字 (`.timeline-note`) 中增加一个显著的徽标（Badge）来标识报送状态。

**可能的状态枚举：**
1. **未报送 / 暂不报送**: 灰色 Badge (`tag-gray`)
2. **报送成功**: 绿色 Badge (`tag-green`)
3. **报送失败**: 红色 Badge (`info-card-badge` 或类似危险色)
4. **报送中**: 蓝色 Badge (`tag-blue`)

## 3. UI 结构调整 (HTML/CSS)

在原有的“修改人员档案”节点中，我们可以在 `.timeline-header-row` 的末尾（紧挨着时间），或者在操作人旁边插入一个状态 Badge。

**调整后的节点结构示例：**
```html
<div class="timeline-item">
    <div class="timeline-dot blue"></div> <!-- 节点颜色代表事件类型：修改为蓝色 -->
    <div class="timeline-content">
        <div class="timeline-header-row">
            <span class="timeline-event">修改人员档案</span>
            <span class="tag tag-gray" style="margin-left: 8px;">未报送</span> <!-- 新增的报送状态标识 -->
            <span class="timeline-meta">操作人: 张HR (管理员)</span>
            <span class="timeline-date">2026-04-22 14:30:00</span>
        </div>
        <div class="timeline-body">
            <!-- 原有的修改明细 -->
            <ul class="change-list">
                <!-- 字段变更列表... -->
            </ul>
        </div>
    </div>
</div>
```

为了让演示更加丰满，我将在现有的 Timeline 中：
1. 更新当前的“修改人员档案”节点，为其添加“**未报送**”状态。
2. 复制并新增一个“修改人员档案”节点，为其添加“**报送成功**”状态（附带额外的税务系统响应提示）。

## 4. 下一步
请确认上述在“修改人员档案”标题旁增加状态 Badge 的方案。确认后我将直接生成代码实施计划并执行修改。