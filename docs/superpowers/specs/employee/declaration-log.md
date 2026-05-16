---
title: 人员报送日志设计重构 (Audit Log - Employee Declaration)
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 人员报送日志设计重构 (Audit Log - Employee Declaration)

## 1. 目标
纠正前一个设计中的误区，将原本的“人员个税报送”事件变更为“**人员报送**”事件（即将员工的入职、离职等基础信息向税局或其他监管系统进行人员信息的登记报送）。

## 2. 字段展示设计

当系统记录一次“人员报送”时，该时间轴节点的 `.timeline-body` 中将展示相关的核心人员报送字段，而不再是个税金额字段。

**需要包含的字段（参考标准人员报送信息）：**
1. **报送主体**: 如 `无锡优派人力资源服务有限公司`
2. **姓名**: 如 `曾强勇`
3. **证件类型**: 如 `居民身份证`
4. **证件号码**: 如 `43102319950825181X`
5. **任职受雇从业类型**: 如 `雇员` / `实习生`
6. **任职受雇从业日期**: 如 `2025-02-25`
7. **人员状态**: 如 `正常`
8. **报送状态**: 如 `报送成功` (高亮显示)

## 3. UI 结构与修改

将原有的个税相关 HTML 替换为人员报送相关：

```html
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
            <span class="change-val" style="background: transparent; padding: 0; font-family: 'SF Mono', monospace;">43102319950825181X</span>
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
```

## 4. 实施范围
在 `prototype/employee-detail-redesign.html` 文件中：
1. 找到对应的下拉筛选框，将 `<option value="tax">个税报送</option>` 修改为 `<option value="declaration">人员报送</option>`。
2. 找到对应的 Timeline 节点，将标题“人员个税报送”修改为“人员报送”。
3. 替换 `timeline-body` 为上述 HTML 结构。

请确认上述设计和字段，确认后我将开始实施。