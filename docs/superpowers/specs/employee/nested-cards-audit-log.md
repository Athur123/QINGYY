# 批量明细记录展示设计方案 (Audit Log - Nested Cards for Multiple Entities)

## 1. 目标
解决家庭成员、工作经历、紧急联系人、教育经历等**多条目（Collection）**数据在被新增、删除、编辑、或者批量导入时，在 Timeline（动态记录）中的呈现问题。
在一个统一的 Timeline 节点（如“批量导入教育经历”或“修改家庭成员”）内，使用**嵌套卡片组 (Nested Cards)** 的形式，清晰地区分每个实体的变更动作和具体字段。

## 2. 需求分析与结构设计

### 2.1 嵌套卡片 (Nested Card)
在 `.timeline-body` 内部，我们不再仅仅使用单个 `.change-list`。如果操作涉及多个条目（比如一次导入新增了2个家庭成员，编辑了1个），我们会展示 3 个小的子卡片（`.sub-record-card`）。

### 2.2 子卡片结构
每个 `.sub-record-card` 需要包含：
- **头部 (`.sub-record-header`)**：
  - **操作标识**: 比如 `<span class="tag tag-green">新增</span>` / `<span class="tag tag-blue">编辑</span>` / `<span class="tag tag-red">删除</span>`
  - **对象标识**: 比如 `家庭成员：李四` / `教育经历：北京大学`
- **内容 (`.sub-record-body`)**：
  - 如果是**新增**：仅展示新增字段的最终值（无需旧值划线）。
  - 如果是**编辑**：展示标准的 `旧值 -> 新值` (`.change-list`)。
  - 如果是**删除**：仅展示被删除的关键信息（或整行划线）。

## 3. UI/CSS 结构草图

### 3.1 CSS 扩展
```css
.sub-record-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 12px;
}

.sub-record-card {
    background: var(--bg-page);
    border: 1px solid var(--border-light);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.sub-record-header {
    padding: 10px 16px;
    border-bottom: 1px solid var(--border-light);
    background: rgba(0, 0, 0, 0.02); /* 轻微区分头部 */
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
}

.sub-record-body {
    padding: 12px 16px;
}

/* 调整现有的 change-list 以适应无背景的子卡片内部 */
.sub-record-body .change-list {
    background: transparent;
    padding: 0;
    border: none;
}
```

### 3.2 HTML 示例 (修改/导入家庭成员)
```html
<div class="timeline-item">
    <div class="timeline-dot blue"></div>
    <div class="timeline-content">
        <div class="timeline-header-row">
            <span class="timeline-event">更新家庭成员</span>
            <span class="timeline-meta">操作人: 张HR</span>
            <span class="timeline-date">2026-04-22 10:00:00</span>
        </div>
        <div class="timeline-body">
            <p class="timeline-note">批量更新了员工的家庭成员及紧急联系人信息。</p>
            
            <div class="sub-record-list">
                <!-- 卡片1：新增 -->
                <div class="sub-record-card">
                    <div class="sub-record-header">
                        <span class="tag tag-green">新增</span>
                        <span>家庭成员：李四 (父亲)</span>
                    </div>
                    <div class="sub-record-body">
                        <ul class="change-list">
                            <li class="change-item">
                                <span class="change-field">联系电话:</span>
                                <span class="change-val new" style="background: transparent;">13800001111</span>
                            </li>
                            <li class="change-item">
                                <span class="change-field">工作单位:</span>
                                <span class="change-val new" style="background: transparent;">无锡市某某公司</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- 卡片2：编辑 -->
                <div class="sub-record-card">
                    <div class="sub-record-header">
                        <span class="tag tag-blue">编辑</span>
                        <span>紧急联系人：王五 (配偶)</span>
                    </div>
                    <div class="sub-record-body">
                        <ul class="change-list">
                            <li class="change-item">
                                <span class="change-field">联系电话:</span>
                                <span class="change-val old">13900002222</span>
                                <span class="change-arrow">...</span>
                                <span class="change-val new">18600003333</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <!-- 卡片3：删除 -->
                <div class="sub-record-card">
                    <div class="sub-record-header">
                        <span class="tag tag-red">删除</span>
                        <span>家庭成员：赵六 (兄弟姐妹)</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

## 4. 下一步
确认上述“嵌套卡片组”样式设计及包含新增/编辑/删除的多条目示例后，我将为您在页面中增加这个 CSS 和展示样例。