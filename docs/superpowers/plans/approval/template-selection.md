---
title: 审批模板选择功能实现计划
module: approval
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 审批模板选择功能实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在"申请垫付"页面增加审批模板选择功能，用户可选择已同步至企业微信的垫付申请审批模板

**Architecture:**
- 后端：扩展现有 `GET /api/approval/templates` API，支持 `type`、`platform`、`sync_status` 参数过滤
- 前端：创建独立的审批模板选择组件HTML，使用青阳云设计系统样式
- 数据流：前端调用API获取模板列表 → 用户选择 → 提交时传入 `approval_template_id`

**Tech Stack:** Python FastAPI (后端), HTML/CSS (前端), 青阳云设计系统 (styles/)

---

## 文件结构

```
backend/approval/
├── api/templates.py          # 修改：扩展模板列表API支持过滤参数
├── models/approval_template.py  # 已有：ApprovalTemplate模型
prototype/
└── advance-payment-apply.html  # 新建：垫付申请页面原型（含审批模板选择）
styles/
├── qingyang-components.css   # 已有：卡片、表格、按钮等组件
├── qingyang-forms.css        # 已有：表单组件
└── qingyang-variables.css    # 已有：设计令牌
```

---

## Task 1: 扩展后端模板列表 API

**Files:**
- Modify: `backend/approval/api/templates.py`
- Test: `backend/approval/tests/test_templates.py`

- [ ] **Step 1: 查看现有 templates.py 实现**

```python
# backend/approval/api/templates.py
# 现有代码结构...
```

- [ ] **Step 2: 添加查询参数过滤支持**

在 `GET /templates` 端点中添加 `type`、`platform`、`sync_status` 查询参数：

```python
@router.get("/templates")
async def list_templates(
    type: Optional[str] = None,
    platform: Optional[str] = None,
    sync_status: Optional[str] = None
):
    query = db.query(ApprovalTemplate)
    if type:
        query = query.filter(ApprovalTemplate.type == type)
    if platform:
        query = query.filter(ApprovalTemplate.platform == platform)
    if sync_status:
        query = query.filter(ApprovalTemplate.sync_status == sync_status)
    return {"code": 0, "data": query.all()}
```

- [ ] **Step 3: 运行测试验证**

Run: `pytest backend/approval/tests/test_templates.py -v`

---

## Task 2: 创建垫付申请页面原型

**Files:**
- Create: `prototype/advance-payment-apply.html`
- Depend: `styles/qingyang-*.css`

- [ ] **Step 1: 创建页面HTML结构**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>申请垫付 - 青阳云HR SaaS</title>
  <link rel="stylesheet" href="../styles/qingyang-variables.css">
  <link rel="stylesheet" href="../styles/qingyang-base.css">
  <link rel="stylesheet" href="../styles/qingyang-components.css">
  <link rel="stylesheet" href="../styles/qingyang-forms.css">
</head>
<body>
  <!-- 顶部导航 -->
  <header class="qy-header">...</header>

  <main class="qy-container">
    <!-- 审批模板选择卡片 -->
    <div class="qy-card qy-approval-template-card">
      <div class="qy-approval-template-alert">
        <span class="qy-icon qy-icon-warning">⚠</span>
        请选择审批模板（必填）
      </div>
      <div class="qy-form-group">
        <label class="qy-label">* 审批模板</label>
        <select class="qy-select" id="approvalTemplate">
          <option value="">请选择审批模板</option>
        </select>
      </div>
      <div class="qy-approval-template-meta" id="templateMeta" style="display:none;">
        已同步至企业微信 | 版本：<span id="templateVersion"></span> |
        更新时间：<span id="templateUpdateTime"></span>
      </div>
    </div>

    <!-- 基础信息卡片 -->
    <div class="qy-card" id="basicInfoCard">
      <div class="qy-card__header">
        <span>基础信息</span>
        <button class="qy-btn qy-btn--text" id="toggleBasicInfo">折叠▴</button>
      </div>
      <div class="qy-card__body">
        <!-- 两列布局表单 -->
        <div class="qy-form-row">
          <div class="qy-form-group">...</div>
          <div class="qy-form-group">...</div>
        </div>
      </div>
    </div>

    <!-- 垫付明细卡片 -->
    <div class="qy-card" id="detailCard">...</div>

    <!-- 底部操作栏 -->
    <div class="qy-action-bar">...</div>
  </main>
</body>
</html>
```

- [ ] **Step 2: 添加CSS样式**

在 `qingyang-components.css` 中添加审批模板卡片样式：

```css
/* 审批模板选择卡片 */
.qy-approval-template-card {
  margin-bottom: var(--qy-space-4);
  border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-lg);
  overflow: hidden;
}

.qy-approval-template-alert {
  background: #FEF2F2;
  color: #DC2626;
  padding: var(--qy-space-3) var(--qy-space-4);
  font-size: var(--qy-font-size-14);
  display: flex;
  align-items: center;
  gap: var(--qy-space-2);
}

.qy-approval-template-meta {
  padding: var(--qy-space-2) var(--qy-space-4);
  font-size: var(--qy-font-size-12);
  color: var(--qy-text-muted);
  background: var(--qy-bg-secondary);
}
```

- [ ] **Step 3: 添加JavaScript交互逻辑**

```javascript
// 加载模板列表
async function loadApprovalTemplates() {
  const response = await fetch('/api/approval/templates?type=advance_apply&platform=wecom&sync_status=synced');
  const result = await response.json();
  const select = document.getElementById('approvalTemplate');

  if (result.data.length === 0) {
    select.innerHTML = '<option value="">暂无可用模板，请联系管理员配置</option>';
    return;
  }

  result.data.forEach(template => {
    const option = document.createElement('option');
    option.value = template.id;
    option.textContent = template.name;
    option.dataset.version = template.name.match(/v\d+/)?.[0] || 'v1';
    option.dataset.updateTime = template.last_sync_time;
    select.appendChild(option);
  });
}

// 模板选择变更
document.getElementById('approvalTemplate').addEventListener('change', function() {
  const meta = document.getElementById('templateMeta');
  if (this.value) {
    const selected = this.options[this.selectedIndex];
    document.getElementById('templateVersion').textContent = selected.dataset.version;
    document.getElementById('templateUpdateTime').textContent = selected.dataset.updateTime;
    meta.style.display = 'block';
  } else {
    meta.style.display = 'none';
  }
});
```

- [ ] **Step 4: 在浏览器中验证**

Run: `open prototype/advance-payment-apply.html`

---

## Task 3: 优化表单布局（两列+折叠）

**Files:**
- Modify: `prototype/advance-payment-apply.html`
- Modify: `styles/qingyang-components.css`

- [ ] **Step 1: 添加两列表单布局样式**

```css
/* 两列表单布局 */
.qy-form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--qy-space-6);
}

@media (max-width: 768px) {
  .qy-form-row {
    grid-template-columns: 1fr;
  }
}
```

- [ ] **Step 2: 添加卡片折叠功能**

```javascript
document.getElementById('toggleBasicInfo').addEventListener('click', function() {
  const body = document.querySelector('#basicInfoCard .qy-card__body');
  const isCollapsed = body.style.display === 'none';
  body.style.display = isCollapsed ? 'block' : 'none';
  this.textContent = isCollapsed ? '折叠▴' : '展开▾';
});
```

---

## Task 4: 金额千分位格式化

**Files:**
- Modify: `prototype/advance-payment-apply.html`

- [ ] **Step 1: 添加金额格式化函数**

```javascript
function formatCurrency(amount) {
  return '¥' + Number(amount).toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  });
}
```

---

## Task 5: 表单验证与提交

**Files:**
- Modify: `prototype/advance-payment-apply.html`

- [ ] **Step 1: 添加提交验证逻辑**

```javascript
document.querySelector('.qy-btn--primary').addEventListener('click', async function() {
  const templateId = document.getElementById('approvalTemplate').value;

  if (!templateId) {
    // 高亮提示条
    const alert = document.querySelector('.qy-approval-template-alert');
    alert.classList.add('is-highlight');
    setTimeout(() => alert.classList.remove('is-highlight'), 1000);

    // 聚焦下拉框
    document.getElementById('approvalTemplate').focus();
    return;
  }

  // 提交表单...
});
```

---

## Self-Review 检查清单

- [ ] Spec覆盖：审批模板选择、UI优化（卡片/两列/折叠/千分位）、API扩展
- [ ] 占位符检查：无TBD/TODO
- [ ] 类型一致性：API响应字段与前端使用一致
- [ ] 依赖关系：Task 2依赖Task 1的API完成
