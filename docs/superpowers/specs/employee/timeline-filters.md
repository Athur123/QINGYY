---
title: 动态记录 (Audit Log) 筛选栏设计方案
module: employee
type: spec
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 动态记录 (Audit Log) 筛选栏设计方案

## 1. 目标
在员工详情页的“动态记录” Tab 中，提供针对审计日志的筛选功能。
用户需要支持的筛选维度包括：**时间、操作类型、字段、操作人**。
视觉上采用紧凑的**内联下拉筛选 (Inline Dropdowns)** 方案。

## 2. 结构与位置设计

在 `.timeline-header` 区域进行扩展。
原结构仅有：
```html
<div class="timeline-header">
    <div class="timeline-title">动态记录 <span class="timeline-count">20条</span></div>
</div>
```

新结构将分为上下两部分（或左右两部分，视空间而定），推荐采用顶部对齐的方式：
```html
<div class="timeline-header" style="flex-direction: column; align-items: stretch; gap: 16px;">
    <!-- 第一行：标题 -->
    <div class="timeline-title">
        <svg>...</svg>
        动态记录
        <span class="timeline-count">20条</span>
    </div>
    
    <!-- 第二行：筛选操作区 (Inline Dropdowns) -->
    <div class="timeline-filters" style="display: flex; gap: 12px; flex-wrap: wrap;">
        <!-- 时间筛选 (Date Picker) -->
        <input type="date" class="form-input filter-input" placeholder="选择时间">
        
        <!-- 操作类型筛选 -->
        <select class="form-input filter-select">
            <option value="">全部操作类型</option>
            <option value="onboard">员工入职</option>
            <option value="edit">修改人员档案</option>
            <option value="transfer">部门调动</option>
            <option value="regular">转正审批</option>
            <option value="tax">个税报送</option>
        </select>
        
        <!-- 变更字段筛选 -->
        <select class="form-input filter-select">
            <option value="">全部字段</option>
            <option value="phone">手机号码</option>
            <option value="dept">所属部门</option>
            <option value="status">员工状态</option>
            <!-- 更多字段... -->
        </select>

        <!-- 操作人筛选 -->
        <select class="form-input filter-select">
            <option value="">全部操作人</option>
            <option value="admin">系统管理员</option>
            <option value="hr">张HR</option>
            <option value="manager">王主管</option>
            <option value="system">系统自动触发</option>
        </select>
    </div>
</div>
```

## 3. UI 细节与 CSS
1. 重用已有的 `.form-input` 样式类以保持设计统一性。
2. 增加 `.filter-select` / `.filter-input` 限定宽度（如 `min-width: 140px; max-width: 200px;`）和高度，使其比标准的表单输入框更紧凑（例如加上 `padding: 6px 12px; height: 32px;`）。
3. 使用 `flex-wrap: wrap` 确保在窄屏设备下筛选条件能自然折行。

---
请确认这个内联下拉筛选的布局和维度设计是否符合您的预期？确认后我将开始实施。