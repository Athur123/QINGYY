---
title: 导入报送信息明细展示设计 (Audit Log - Import Details)
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 导入报送信息明细展示设计 (Audit Log - Import Details)

## 1. 目标
在“导入报送信息”这条日志中，增加详细的字段变更展示（只展示该员工相关的被更新的报送字段明细）。

## 2. 设计与展示内容

原本的日志仅有一句总结：
> 通过模板文件 `2026年3月专项附加扣除导入模板.xlsx` 更新了员工的个税附加扣除信息。导入状态：**导入成功**。

我们将在这句总结下方，追加一个 `.change-list`（带浅灰色背景，与“人员报送”明细风格一致），列出导入操作导致的具体字段值变动：
- **专项附加扣除-子女教育**: 否 -> 是
- **专项附加扣除-继续教育**: 否 -> 否 (无变化，或者省略)
- **专项附加扣除-住房贷款利息**: 否 -> 是
- **专项附加扣除-住房租金**: 否 -> 否
- **专项附加扣除-赡养老人**: 是 -> 是

**UI 结构示例：**
```html
<div class="timeline-body">
    <p class="timeline-note" style="margin-bottom: 12px;">通过模板文件 <code>2026年3月专项附加扣除导入模板.xlsx</code> 更新了员工的个税附加扣除信息。</p>
    <ul class="change-list" style="background: var(--bg-page); padding: 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-light);">
        <li class="change-item">
            <span class="change-field" style="min-width: 160px;">专项附加扣除-子女教育</span>
            <span class="change-val old">否</span>
            <span class="change-arrow">...</span>
            <span class="change-val new">是</span>
        </li>
        <li class="change-item">
            <span class="change-field" style="min-width: 160px;">专项附加扣除-住房贷款利息</span>
            <span class="change-val old">否</span>
            <span class="change-arrow">...</span>
            <span class="change-val new">是</span>
        </li>
        <li class="change-item">
            <span class="change-field" style="min-width: 160px;">专项附加扣除-赡养老人</span>
            <span class="change-val old" style="text-decoration: none;">是</span>
            <span class="change-arrow">...</span>
            <span class="change-val new">是</span>
        </li>
    </ul>
</div>
```
*(同时会移除原说明中的“导入状态：导入成功”，因为前面已经去除了报送状态的概念)*

## 3. 下一步
设计已确认，我将立即进入实施阶段，将这些明细补齐到页面中。