---
title: 个税申报日志详细展示设计 (Audit Log - Tax Details)
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 个税申报日志详细展示设计 (Audit Log - Tax Details)

## 1. 目标
扩展 `prototype/employee-detail-redesign.html` 中的时间轴（Timeline）记录，将原本简略的“人员个税报送”事件升级为**结构化、高密度**的详细申报信息列表。
采用**普通行列表 (List)** 形式，与现有的档案修改记录 (`.change-list`) 的紧凑度保持一致。

## 2. 字段展示设计

当系统记录一次“个税申报”时，该时间轴节点的 `.timeline-body` 中将展示以下核心申报字段。为了使信息层次分明，部分关键金额可考虑使用货币高亮样式。

**需要包含的字段：**
1. **税款所属期**: 如 `2026年03月`
2. **申报主体**: 如 `无锡优派人力资源服务有限公司`
3. **本期收入额**: 如 `¥23,000.00`
4. **本期免税收入**: 如 `¥0.00`
5. **本期扣除(五险一金)**: 如 `¥2,500.00`
6. **专项附加扣除**: 如 `¥3,000.00` (子女教育等)
7. **应纳税所得额**: 如 `¥17,500.00`
8. **应扣缴税额**: 如 `¥525.00`

## 3. UI 结构 (HTML/CSS)

我们将复用已有的 `.change-list` 样式类，并创建一个不带箭头的普通键值对形式，以保持整体视觉风格的统一。

```html
<!-- 示例结构 -->
<div class="timeline-body">
    <p class="timeline-note" style="margin-bottom: 12px;">2026年3月个税申报数据已成功同步至税务局接口，申报状态：<strong>申报成功</strong>。</p>
    <ul class="change-list" style="background: var(--bg-page); padding: 12px; border-radius: var(--radius-sm);">
        <li class="change-item">
            <span class="change-field">税款所属期:</span>
            <span class="change-val">2026-03</span>
        </li>
        <li class="change-item">
            <span class="change-field">申报主体:</span>
            <span class="change-val">无锡优派人力资源服务有限公司</span>
        </li>
        <li class="change-item">
            <span class="change-field">本期收入额:</span>
            <span class="change-val" style="color: var(--text-primary); font-weight: 500;">¥23,000.00</span>
        </li>
        <!-- 更多字段... -->
    </ul>
</div>
```
*注：为了让个税明细表看起来更像一个报表区域，我们会给这组列表加一个浅灰色的底色块 `background: var(--bg-page)`，使其在白色的卡片内有一个视觉区隔。*

## 4. 下一步
确认上述字段及样式设计无误后，我将直接编写并执行更新计划，修改页面中的“个税报送”节点。