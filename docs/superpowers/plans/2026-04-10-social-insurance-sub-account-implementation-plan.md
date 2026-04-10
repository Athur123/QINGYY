# 社保二级户实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在参保规则编辑页面新增"二级户管理"Tab，实现二级户的增删改查功能。

**Architecture:** 基于青阳云HRO现有设计系统，在参保规则编辑页（`/socialSecurity/page`）的Tab结构中新增二级户管理Tab。数据通过现有参保规则API或新增子账户API管理。

**Tech Stack:** 
- 前端：React/Vue（取决于现有技术栈）
- 样式：复用 `styles/qingyang-*.css` 设计系统
- 数据：localStorage 模拟（原型阶段）

---

## 文件结构

```
prototype/
└── social-insurance-sub-account.html    # 新建：二级户功能原型

styles/
├── qingyang-variables.css                # 已存在
├── qingyang-components.css               # 已存在：qy-table, qy-btn, qy-modal, qy-tab
├── qingyang-forms.css                    # 已存在：qy-input, qy-select
└── qingyang-insurance-rule.css          # 新建（如需要）：参保规则专属样式
```

---

## Task 1: 创建二级户管理Tab原型

**Files:**
- Create: `prototype/social-insurance-sub-account.html`

- [ ] **Step 1: 创建基础页面结构（复用参保规则编辑页布局）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>参保规则编辑 - 二级户管理 - 青阳云</title>
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <link rel="stylesheet" href="../styles/qingyang-forms.css">
    <style>
        /* 页面专属样式 */
        .page-container { max-width: 1200px; margin: 0 auto; padding: 24px; }
        .page-header { display: flex; align-items: center; gap: 16px; margin-bottom: 24px; }
        .page-title { font-size: 18px; font-weight: 600; }
        
        /* Tab导航 */
        .tab-nav { display: flex; gap: 4px; border-bottom: 1px solid var(--qy-border-light); margin-bottom: 24px; }
        .tab-item { padding: 12px 20px; cursor: pointer; border-bottom: 2px solid transparent; color: var(--qy-text-secondary); transition: all 0.2s; }
        .tab-item:hover { color: var(--qy-text-primary); }
        .tab-item.active { color: var(--qy-primary-600); border-bottom-color: var(--qy-primary-600); font-weight: 500; }
        
        /* 二级户表格 */
        .sub-account-list { background: var(--qy-bg-primary); border-radius: var(--qy-radius-lg); border: 1px solid var(--qy-border-light); overflow: hidden; }
        .list-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border-bottom: 1px solid var(--qy-border-light); }
        .list-count { font-size: 14px; color: var(--qy-text-secondary); }
        .qy-table { width: 100%; border-collapse: collapse; }
        .qy-table th { text-align: left; padding: 12px 16px; background: var(--qy-bg-secondary); font-weight: 500; font-size: 13px; color: var(--qy-text-secondary); border-bottom: 1px solid var(--qy-border-light); }
        .qy-table td { padding: 14px 16px; border-bottom: 1px solid var(--qy-border-light); font-size: 13px; }
        .qy-table tr:last-child td { border-bottom: none; }
        .qy-table .action-btns { display: flex; gap: 8px; }
    </style>
</head>
<body>
    <div class="page-container">
        <!-- 页面标题 -->
        <div class="page-header">
            <button class="qy-btn qy-btn--text" id="btn-back">← 返回</button>
            <h1 class="page-title">编辑参保规则</h1>
        </div>
        
        <!-- Tab导航 -->
        <div class="tab-nav">
            <div class="tab-item" data-tab="basic">基本信息</div>
            <div class="tab-item" data-tab="insurance">参保险种</div>
            <div class="tab-item" data-tab="config">规则配置</div>
            <div class="tab-item active" data-tab="sub-account">二级户管理</div>
        </div>
        
        <!-- 二级户管理内容 -->
        <div class="tab-content" id="tab-sub-account">
            <div class="sub-account-list">
                <div class="list-header">
                    <span class="list-count">二级户列表（共 <span id="sub-account-count">2</span> 个）</span>
                    <button class="qy-btn qy-btn--primary" id="btn-add">+ 新增二级户</button>
                </div>
                <table class="qy-table">
                    <thead>
                        <tr>
                            <th>二级户名称</th>
                            <th>用工单位编码</th>
                            <th>用工单位全称</th>
                            <th>工伤保险费率</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody id="sub-account-tbody">
                        <!-- 动态填充 -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 底部操作栏 -->
        <div class="action-bar" style="margin-top: 24px; display: flex; justify-content: flex-end; gap: 12px;">
            <button class="qy-btn qy-btn--secondary" id="btn-cancel">取消</button>
            <button class="qy-btn qy-btn--primary" id="btn-save">保存</button>
        </div>
    </div>
    
    <!-- 新增/编辑弹窗 -->
    <div class="modal-overlay" id="modal-form">
        <div class="modal-container" style="max-width: 500px;">
            <div class="modal-header" style="padding: 20px; border-bottom: 1px solid var(--qy-border-light); display: flex; justify-content: space-between; align-items: center;">
                <h3 id="modal-title" style="font-size: 16px; font-weight: 600;">新增二级户</h3>
                <button class="qy-btn qy-btn--text" id="btn-close-modal">×</button>
            </div>
            <div class="modal-body" style="padding: 20px;">
                <div class="form-group" style="margin-bottom: 16px;">
                    <label class="qy-label">* 二级户名称</label>
                    <input type="text" class="qy-input" id="input-name" placeholder="如：XX公司-普通工种" style="width: 100%;">
                </div>
                <div class="form-group" style="margin-bottom: 16px;">
                    <label class="qy-label">* 用工单位编码</label>
                    <input type="text" class="qy-input" id="input-code" placeholder="请输入用工单位编码" style="width: 100%;">
                </div>
                <div class="form-group" style="margin-bottom: 16px;">
                    <label class="qy-label">* 用工单位全称</label>
                    <input type="text" class="qy-input" id="input-company" placeholder="请输入用工单位全称" style="width: 100%;">
                </div>
                <div class="form-group" style="margin-bottom: 16px;">
                    <label class="qy-label">* 工伤保险费率</label>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <input type="number" class="qy-input" id="input-rate" placeholder="0.00" style="width: 120px;" step="0.01" min="0" max="100">
                        <span>%</span>
                    </div>
                </div>
            </div>
            <div class="modal-footer" style="padding: 16px 20px; border-top: 1px solid var(--qy-border-light); display: flex; justify-content: flex-end; gap: 12px;">
                <button class="qy-btn qy-btn--secondary" id="btn-modal-cancel">取消</button>
                <button class="qy-btn qy-btn--primary" id="btn-modal-confirm">确定</button>
            </div>
        </div>
    </div>
</body>
</html>
```

- [ ] **Step 2: 实现Tab切换逻辑**

```javascript
// Tab切换
const tabItems = document.querySelectorAll('.tab-item');
tabItems.forEach(item => {
    item.addEventListener('click', () => {
        tabItems.forEach(t => t.classList.remove('active'));
        item.classList.add('active');
        // 实际项目中切换Tab内容显示
    });
});
```

- [ ] **Step 3: 实现二级户列表渲染**

```javascript
// 预置示例数据
const subAccounts = [
    { id: 'SA001', name: '北京软件技术公司-普通工种', companyCode: 'BJ001', companyName: '北京软件技术公司', injuryRate: 0.5 },
    { id: 'SA002', name: '北京软件技术公司-高危工种', companyCode: 'BJ001', companyName: '北京软件技术公司', injuryRate: 1.5 }
];

// 渲染列表
function renderSubAccountList() {
    const tbody = document.getElementById('sub-account-tbody');
    const countSpan = document.getElementById('sub-account-count');
    tbody.innerHTML = subAccounts.map(acc => `
        <tr>
            <td>${acc.name}</td>
            <td>${acc.companyCode}</td>
            <td>${acc.companyName}</td>
            <td>${acc.injuryRate}%</td>
            <td class="action-btns">
                <button class="qy-btn qy-btn--text" onclick="editSubAccount('${acc.id}')">编辑</button>
                <button class="qy-btn qy-btn--text" onclick="deleteSubAccount('${acc.id}')">删除</button>
            </td>
        </tr>
    `).join('');
    countSpan.textContent = subAccounts.length;
}
```

- [ ] **Step 4: 实现新增/编辑弹窗**

```javascript
const modal = document.getElementById('modal-form');
const modalTitle = document.getElementById('modal-title');
let editingId = null;

// 打开新增弹窗
document.getElementById('btn-add').addEventListener('click', () => {
    editingId = null;
    modalTitle.textContent = '新增二级户';
    clearForm();
    modal.classList.add('active');
});

// 打开编辑弹窗
window.editSubAccount = function(id) {
    const acc = subAccounts.find(a => a.id === id);
    if (!acc) return;
    editingId = id;
    modalTitle.textContent = '编辑二级户';
    document.getElementById('input-name').value = acc.name;
    document.getElementById('input-code').value = acc.companyCode;
    document.getElementById('input-company').value = acc.companyName;
    document.getElementById('input-rate').value = acc.injuryRate;
    modal.classList.add('active');
};

// 关闭弹窗
function closeModal() {
    modal.classList.remove('active');
    clearForm();
}
document.getElementById('btn-close-modal').addEventListener('click', closeModal);
document.getElementById('btn-modal-cancel').addEventListener('click', closeModal);

// 清空表单
function clearForm() {
    document.getElementById('input-name').value = '';
    document.getElementById('input-code').value = '';
    document.getElementById('input-company').value = '';
    document.getElementById('input-rate').value = '';
}
```

- [ ] **Step 5: 实现保存逻辑**

```javascript
document.getElementById('btn-modal-confirm').addEventListener('click', () => {
    const name = document.getElementById('input-name').value.trim();
    const companyCode = document.getElementById('input-code').value.trim();
    const companyName = document.getElementById('input-company').value.trim();
    const injuryRate = parseFloat(document.getElementById('input-rate').value);
    
    // 表单验证
    if (!name || !companyCode || !companyName || isNaN(injuryRate)) {
        alert('请填写所有必填字段');
        return;
    }
    if (injuryRate < 0 || injuryRate > 100) {
        alert('工伤保险费率必须在0~100之间');
        return;
    }
    
    if (editingId) {
        // 更新
        const index = subAccounts.findIndex(a => a.id === editingId);
        if (index !== -1) {
            subAccounts[index] = { ...subAccounts[index], name, companyCode, companyName, injuryRate };
        }
    } else {
        // 新增
        subAccounts.push({
            id: 'SA' + Date.now(),
            name, companyCode, companyName, injuryRate
        });
    }
    
    renderSubAccountList();
    closeModal();
});
```

- [ ] **Step 6: 实现删除逻辑**

```javascript
window.deleteSubAccount = function(id) {
    if (!confirm('删除后不可恢复，是否确认？')) return;
    const index = subAccounts.findIndex(a => a.id === id);
    if (index !== -1) {
        subAccounts.splice(index, 1);
        renderSubAccountList();
    }
};
```

- [ ] **Step 7: 初始化页面**

```javascript
// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    renderSubAccountList();
});
```

- [ ] **Step 8: 提交**

```bash
git add prototype/social-insurance-sub-account.html
git commit -m "feat: add social insurance sub-account prototype

- Create sub-account management tab prototype
- Support CRUD operations for sub-accounts
- Include modal form for add/edit
- Validate injury rate (0-100)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 与参保规则编辑页集成

**Files:**
- Modify: `prototype/social-insurance-sub-account.html`（扩展现有Tab结构）

此任务在实际项目中需要修改参保规则编辑页面的源代码。原型已验证UI方案。

**集成要点：**
1. 在参保规则编辑页的Tab组件中添加"二级户管理"Tab
2. Tab内容复用本原型中的列表和弹窗结构
3. 二级户数据通过 `parentRuleId` 与主参保规则关联
4. 保存时应与主规则一并提交

---

## Task 3: API设计（如需后端）

**Files:**
- 新增API端点（如后端在当前仓库）:

```
POST   /api/insurance/rules/{ruleId}/sub-accounts    # 新增二级户
GET    /api/insurance/rules/{ruleId}/sub-accounts     # 获取二级户列表
PUT    /api/insurance/rules/{ruleId}/sub-accounts/{id} # 更新二级户
DELETE /api/insurance/rules/{ruleId}/sub-accounts/{id} # 删除二级户
```

**Request/Response 示例：**

```json
// POST /api/insurance/rules/R001/sub-accounts
{
    "name": "XX公司-普通工种",
    "companyCode": "10001",
    "companyName": "XX科技有限公司",
    "injuryRate": 0.5
}

// Response
{
    "code": 200,
    "data": {
        "id": "SA001",
        "parentRuleId": "R001",
        "name": "XX公司-普通工种",
        "companyCode": "10001",
        "companyName": "XX科技有限公司",
        "injuryRate": 0.5
    }
}
```

---

## 自检清单

- [x] Spec覆盖：UI设计、交互逻辑、数据模型均已覆盖
- [x] 占位符检查：无TBD/TODO占位符
- [x] 类型一致性：字段名称在所有任务中保持一致

---

## 执行选项

**1. Subagent-Driven（推荐）** - 每任务派遣新子agent，快速迭代

**2. Inline Execution** - 本会话执行，带检查点

选择哪种方式？
