---
title: 地区社保规则配置 - 实现计划
module: calculator
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 地区社保规则配置 - 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建地区社保规则配置的HTML原型，包含规则列表页、新建/编辑页（含条件组合构建器）、规则匹配算法模拟、员工参保预览页集成。

**Architecture:** 基于现有青阳云HRO设计系统，使用原生HTML/CSS/JS实现。新增独立页面 `region-social-insurance-rules.html`，复用 `styles/` 下的CSS组件库。

**Tech Stack:** 原生HTML + CSS + JavaScript，复用 `styles/qingyang-*.css` 设计系统组件。

---

## 文件结构

```
prototype/
└── region-social-insurance-rules.html    # 新建：规则配置主页面

styles/
├── qingyang-variables.css                 # 已存在：设计令牌
├── qingyang-components.css                # 已存在：UI组件
└── qingyang-forms.css                     # 已存在：表单组件

数据：
- 使用 localStorage 模拟后端数据
- 预置3-5条示例规则数据
```

---

## Task 1: 创建规则列表页原型

**Files:**
- Create: `prototype/region-social-insurance-rules.html`

- [ ] **Step 1: 创建基础页面结构**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>地区社保规则配置 - 青阳云</title>
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <link rel="stylesheet" href="../styles/qingyang-forms.css">
</head>
<body>
    <div class="app-container">
        <!-- 复用现有侧边栏 -->
        <aside class="sidebar">...</aside>
        <!-- 主内容区 -->
        <main class="main-content">
            <header class="page-header">
                <h1>地区社保规则配置</h1>
                <button class="qy-btn qy-btn--primary" id="btn-new-rule">+ 新建规则</button>
            </header>
            <!-- 筛选栏 -->
            <div class="filter-bar">
                <select id="filter-region" class="qy-select">
                    <option value="">全部地区</option>
                    <option value="gd-gz-th">广东省/广州市/天河区</option>
                    <!-- 更多选项 -->
                </select>
                <select id="filter-status" class="qy-select">
                    <option value="">全部状态</option>
                    <option value="active">生效</option>
                    <option value="inactive">停用</option>
                    <option value="draft">草稿</option>
                </select>
            </div>
            <!-- 规则列表表格 -->
            <table class="qy-table">
                <thead>
                    <tr>
                        <th>地区</th>
                        <th>版本</th>
                        <th>状态</th>
                        <th>条件摘要</th>
                        <th>动作摘要</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="rule-list-body">
                    <!-- 动态填充 -->
                </tbody>
            </table>
        </main>
    </div>
</body>
</html>
```

- [ ] **Step 2: 预置示例规则数据**

```javascript
// 预置3条示例规则
const mockRules = [
    {
        id: 'R001',
        region: { province: '广东省', city: '广州市', district: '天河区' },
        name: '天河区派遣员工特殊规则',
        version: 3,
        status: 'active',
        priority: 1,
        conditions: [
            { field: 'employeeType', operator: 'in', value: ['派遣员工'] },
            { field: 'projectId', operator: 'in', value: ['项目A'] }
        ],
        actions: {
            '工伤': { type: 'dispatch_ratio' },
            '养老': { type: 'specified_ratio', value: 14 },
            '医疗': { type: 'account_ratio' }
        },
        effectStart: '2026-01-01',
        effectEnd: '2026-12-31'
    },
    // ... 更多示例规则
];
```

- [ ] **Step 3: 实现列表渲染函数**

```javascript
function renderRuleList(rules) {
    const tbody = document.getElementById('rule-list-body');
    tbody.innerHTML = rules.map(rule => `
        <tr data-rule-id="${rule.id}">
            <td>${rule.region.province}/${rule.region.city}/${rule.region.district}</td>
            <td>v${rule.version}</td>
            <td><span class="qy-tag qy-tag--${getStatusType(rule.status)}">${getStatusText(rule.status)}</span></td>
            <td>${renderConditionSummary(rule.conditions)}</td>
            <td>${renderActionSummary(rule.actions)}</td>
            <td>
                <button class="qy-btn qy-btn--text" onclick="editRule('${rule.id}')">编辑</button>
                <button class="qy-btn qy-btn--text" onclick="toggleRule('${rule.id}')">${rule.status === 'active' ? '停用' : '启用'}</button>
                <button class="qy-btn qy-btn--text" onclick="cloneRule('${rule.id}')">复制</button>
                <button class="qy-btn qy-btn--text" onclick="showHistory('${rule.id}')">历史</button>
            </td>
        </tr>
    `).join('');
}
```

- [ ] **Step 4: 测试列表渲染**

在浏览器中打开页面，验证：
- 表格正确渲染3条示例规则
- 筛选下拉框可用
- 操作按钮显示正确

- [ ] **Step 5: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: add region social insurance rules list prototype"
```

---

## Task 2: 创建规则新建/编辑页（Modal）

**Files:**
- Modify: `prototype/region-social-insurance-rules.html`

- [ ] **Step 1: 添加 Modal 容器**

```html
<!-- 新建/编辑规则 Modal -->
<div class="qy-modal" id="rule-modal" style="display: none;">
    <div class="qy-modal__backdrop" onclick="closeModal()"></div>
    <div class="qy-modal__container qy-modal__container--lg">
        <div class="qy-modal__header">
            <h2 id="modal-title">新建地区社保规则</h2>
            <button class="qy-modal__close" onclick="closeModal()">×</button>
        </div>
        <div class="qy-modal__body">
            <!-- Step 1: 选择地区 -->
            <div class="form-section">
                <h3>Step 1: 选择地区</h3>
                <div class="qy-form-row">
                    <div class="qy-form-group">
                        <label>省级</label>
                        <select id="region-province" class="qy-select">
                            <option value="">请选择</option>
                            <option value="广东省">广东省</option>
                            <option value="湖南省">湖南省</option>
                        </select>
                    </div>
                    <div class="qy-form-group">
                        <label>市级</label>
                        <select id="region-city" class="qy-select" disabled>
                            <option value="">请先选择省级</option>
                        </select>
                    </div>
                    <div class="qy-form-group">
                        <label>区级</label>
                        <select id="region-district" class="qy-select" disabled>
                            <option value="">请先选择市级</option>
                        </select>
                    </div>
                </div>
            </div>
            <!-- Step 2: 配置条件 -->
            <div class="form-section">
                <h3>Step 2: 配置条件</h3>
                <div id="condition-builder">
                    <!-- 动态条件组 -->
                </div>
                <button class="qy-btn qy-btn--secondary" onclick="addConditionGroup()">+ 添加条件组</button>
            </div>
            <!-- Step 3: 配置动作 -->
            <div class="form-section">
                <h3>Step 3: 配置动作</h3>
                <table class="qy-table qy-table--simple">
                    <thead>
                        <tr>
                            <th>险种</th>
                            <th>动作类型</th>
                            <th>比例值</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>工伤</td>
                            <td>
                                <select class="qy-select action-type" data-insurance="工伤">
                                    <option value="dispatch_ratio">派遣单位比例</option>
                                    <option value="specified_ratio">指定比例</option>
                                    <option value="account_ratio">参保户头比例</option>
                                </select>
                            </td>
                            <td><input type="number" class="qy-input specified-value" style="display:none" step="0.01"></td>
                        </tr>
                        <!-- 其他险种类似 -->
                    </tbody>
                </table>
            </div>
            <!-- Step 4: 基本信息 -->
            <div class="form-section">
                <h3>Step 4: 基本信息</h3>
                <div class="qy-form-row">
                    <div class="qy-form-group">
                        <label>规则名称</label>
                        <input type="text" id="rule-name" class="qy-input">
                    </div>
                    <div class="qy-form-group">
                        <label>优先级</label>
                        <input type="number" id="rule-priority" class="qy-input" value="1">
                    </div>
                </div>
                <div class="qy-form-row">
                    <div class="qy-form-group">
                        <label>生效开始日期</label>
                        <input type="date" id="effect-start" class="qy-input">
                    </div>
                    <div class="qy-form-group">
                        <label>生效结束日期</label>
                        <input type="date" id="effect-end" class="qy-input">
                    </div>
                </div>
            </div>
        </div>
        <div class="qy-modal__footer">
            <button class="qy-btn qy-btn--secondary" onclick="closeModal()">取消</button>
            <button class="qy-btn qy-btn--secondary" onclick="saveAsDraft()">保存为草稿</button>
            <button class="qy-btn qy-btn--primary" onclick="publishRule()">发布</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 实现条件构建器组件**

```javascript
// 条件构建器状态
let conditionGroups = [
    {
        id: 1,
        logicalType: 'AND',
        conditions: [
            { field: 'employeeType', operator: 'in', value: [] }
        ]
    }
];

function renderConditionBuilder() {
    const container = document.getElementById('condition-builder');
    container.innerHTML = conditionGroups.map((group, groupIndex) => `
        <div class="condition-group" data-group-id="${group.id}">
            <div class="condition-group-header">
                <select class="qy-select logical-type" onchange="updateGroupLogicalType(${group.id}, this.value)">
                    <option value="AND" ${group.logicalType === 'AND' ? 'selected' : ''}>AND</option>
                    <option value="OR" ${group.logicalType === 'OR' ? 'selected' : ''}>OR</option>
                </select>
                <button class="qy-btn qy-btn--text" onclick="removeConditionGroup(${group.id})">删除</button>
            </div>
            <div class="condition-items">
                ${group.conditions.map((cond, condIndex) => renderConditionItem(group.id, cond, condIndex)).join('')}
            </div>
            <button class="qy-btn qy-btn--text" onclick="addCondition(${group.id})">+ 添加条件</button>
        </div>
    `).join('');
}

function renderConditionItem(groupId, condition, condIndex) {
    const fields = [
        { value: 'employeeType', label: '员工类型', options: ['正式员工', '派遣员工', '实习生'] },
        { value: 'projectId', label: '所属项目', options: ['项目A', '项目B', '项目C'] },
        { value: 'customerId', label: '所属客户', options: ['客户X', '客户Y'] },
        { value: 'position', label: '岗位', options: ['技术岗', '销售岗', '管理岗'] },
        { value: 'level', label: '职级', options: ['P5', 'P6', 'P7'] }
    ];

    return `
        <div class="condition-item">
            <select class="qy-select condition-field" onchange="updateCondition(${groupId}, ${condIndex}, 'field', this.value)">
                ${fields.map(f => `<option value="${f.value}">${f.label}</option>`).join('')}
            </select>
            <select class="qy-select condition-operator">
                <option value="in">属于</option>
                <option value="notIn">不属于</option>
                <option value="=">等于</option>
                <option value="!=">不等于</option>
            </select>
            <select class="qy-select condition-value" multiple>
                ${fields.find(f => f.value === condition.field)?.options.map(opt =>
                    `<option value="${opt}" ${condition.value.includes(opt) ? 'selected' : ''}>${opt}</option>`
                ).join('')}
            </select>
            <button class="qy-btn qy-btn--text" onclick="removeCondition(${groupId}, ${condIndex})">删除</button>
        </div>
    `;
}
```

- [ ] **Step 3: 实现 Modal 打开/关闭逻辑**

```javascript
function openNewRuleModal() {
    document.getElementById('modal-title').textContent = '新建地区社保规则';
    document.getElementById('rule-modal').style.display = 'block';
    resetForm();
}

function openEditRuleModal(ruleId) {
    const rule = mockRules.find(r => r.id === ruleId);
    if (!rule) return;

    document.getElementById('modal-title').textContent = '编辑地区社保规则';
    // 填充表单数据
    fillFormWithRule(rule);
    document.getElementById('rule-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('rule-modal').style.display = 'none';
}

function resetForm() {
    // 重置所有表单字段
    document.getElementById('region-province').value = '';
    document.getElementById('rule-name').value = '';
    document.getElementById('rule-priority').value = '1';
    conditionGroups = [{ id: 1, logicalType: 'AND', conditions: [{ field: 'employeeType', operator: 'in', value: [] }] }];
    renderConditionBuilder();
}
```

- [ ] **Step 4: 实现动作类型的显示/隐藏联动**

```javascript
document.querySelectorAll('.action-type').forEach(select => {
    select.addEventListener('change', function() {
        const row = this.closest('tr');
        const valueInput = row.querySelector('.specified-value');
        if (this.value === 'specified_ratio') {
            valueInput.style.display = 'block';
        } else {
            valueInput.style.display = 'none';
        }
    });
});
```

- [ ] **Step 5: 测试 Modal 交互**

- 点击「新建规则」按钮，Modal 正确打开
- 选择省/市/区三级联动
- 添加/删除条件组
- 添加/删除条件项
- 选择动作类型时，比例值输入框正确显示/隐藏
- 点击保存，表单数据正确收集

- [ ] **Step 6: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: add rule create/edit modal with condition builder"
```

---

## Task 3: 实现规则匹配算法

**Files:**
- Modify: `prototype/region-social-insurance-rules.html` (添加 `<script>` 部分)

- [ ] **Step 1: 实现条件匹配函数**

```javascript
/**
 * 评估单个条件是否满足
 * @param {Object} condition - 条件对象
 * @param {Object} employee - 员工信息
 * @returns {boolean}
 */
function evaluateCondition(condition, employee) {
    const { field, operator, value } = condition;
    const employeeValue = employee[field];

    if (operator === 'in') {
        return value.includes(employeeValue);
    } else if (operator === 'notIn') {
        return !value.includes(employeeValue);
    } else if (operator === '=') {
        return employeeValue === value;
    } else if (operator === '!=') {
        return employeeValue !== value;
    }
    return false;
}

/**
 * 评估条件组是否满足（同一组内按 logicalType 组合）
 * @param {Array} conditions - 条件数组
 * @param {string} logicalType - AND/OR
 * @param {Object} employee - 员工信息
 * @returns {boolean}
 */
function evaluateConditionGroup(conditions, logicalType, employee) {
    if (logicalType === 'AND') {
        return conditions.every(c => evaluateCondition(c, employee));
    } else {
        return conditions.some(c => evaluateCondition(c, employee));
    }
}

/**
 * 评估规则的所有条件是否满足
 * @param {Object} rule - 规则对象
 * @param {Object} employee - 员工信息
 * @returns {boolean}
 */
function evaluateRule(rule, employee) {
    // 条件组之间永远是 AND 关系
    return rule.conditions.every(group =>
        evaluateConditionGroup(group.conditions, group.logicalType, employee)
    );
}
```

- [ ] **Step 2: 实现规则匹配主函数**

```javascript
/**
 * 规则匹配主函数
 * @param {Object} employee - 员工信息
 * @param {string} accountId - 参保户头ID（用于获取地区）
 * @returns {Object} 匹配结果
 */
function matchRules(employee, accountId) {
    const account = getAccountById(accountId);
    const region = account?.region;

    // 1. 查找该地区的规则
    const regionRules = mockRules.filter(rule => {
        if (rule.status !== 'active') return false;
        if (!isWithinEffectPeriod(rule)) return false;
        return matchesRegion(rule.region, region);
    }).sort((a, b) => a.priority - b.priority);

    // 2. 条件匹配
    const matchedRules = regionRules.filter(rule => evaluateRule(rule, employee));

    // 3. 冲突检测
    const conflicts = detectConflicts(matchedRules);

    // 4. 执行动作
    const actions = {};
    if (conflicts.length > 0) {
        return { matched: false, conflicts, matchedRules };
    }

    matchedRules.forEach(rule => {
        Object.entries(rule.actions).forEach(([insuranceType, action]) => {
            actions[insuranceType] = resolveAction(action, employee);
        });
    });

    return {
        matched: matchedRules.length > 0,
        ruleId: matchedRules[0]?.id,
        ruleName: matchedRules[0]?.name,
        ruleVersion: matchedRules[0]?.version,
        actions,
        conflicts: []
    };
}

/**
 * 地区匹配（严格按区/市/省，不继承）
 */
function matchesRegion(ruleRegion, employeeRegion) {
    if (ruleRegion.district && ruleRegion.district !== employeeRegion.district) {
        return false;
    }
    if (ruleRegion.city && ruleRegion.city !== employeeRegion.city) {
        return false;
    }
    if (ruleRegion.province && ruleRegion.province !== employeeRegion.province) {
        return false;
    }
    return true;
}

/**
 * 检测冲突（同险种，不同规则动作不一致）
 */
function detectConflicts(matchedRules) {
    const conflicts = [];
    const insuranceTypes = ['工伤', '养老', '医疗', '失业', '生育', '公积金'];
    const actionKeys = ['type', 'value'];

    for (const type of insuranceTypes) {
        const typeActions = matchedRules.map(r => r.actions[type]).filter(Boolean);
        if (typeActions.length < 2) continue;

        // 检查是否有不同的动作
        const uniqueActions = new Set(typeActions.map(a => JSON.stringify(a)));
        if (uniqueActions.size > 1) {
            conflicts.push({
                insuranceType: type,
                rules: matchedRules.map(r => ({
                    id: r.id,
                    name: r.name,
                    priority: r.priority,
                    action: r.actions[type]
                }))
            });
        }
    }
    return conflicts;
}
```

- [ ] **Step 3: 实现动作解析函数**

```javascript
/**
 * 解析动作，返回实际的比例值
 */
function resolveAction(action, employee) {
    if (action.type === 'dispatch_ratio') {
        // 从员工所属派遣单位获取比例
        const dispatchUnit = getDispatchUnitById(employee.dispatchUnitId);
        return {
            type: 'dispatch_ratio',
            source: dispatchUnit?.name || '未知派遣单位',
            value: dispatchUnit?.workInjuryRatio || 0
        };
    } else if (action.type === 'specified_ratio') {
        return {
            type: 'specified_ratio',
            value: action.value
        };
    } else if (action.type === 'account_ratio') {
        // 从参保户头获取比例
        return {
            type: 'account_ratio',
            value: action.value || 0
        };
    }
}
```

- [ ] **Step 4: 编写测试用例验证匹配算法**

```javascript
// 测试用例
const testCases = [
    {
        name: '派遣员工+项目A -> 使用派遣单位比例',
        employee: { type: '派遣员工', projectId: '项目A', dispatchUnitId: 'DU001' },
        accountId: 'ACC001',
        expectedMatch: true,
        expectedAction: { '工伤': { type: 'dispatch_ratio', value: 0.6 } }
    },
    {
        name: '正式员工 -> 使用参保户头比例',
        employee: { type: '正式员工', projectId: '项目B', dispatchUnitId: 'DU001' },
        accountId: 'ACC001',
        expectedMatch: false  // 无匹配规则，使用默认
    },
    {
        name: '冲突检测 - 同一人匹配两条规则',
        employee: { type: '派遣员工', projectId: '项目A', dispatchUnitId: 'DU001', level: 'P5' },
        accountId: 'ACC001',
        expectedConflict: true
    }
];

function runTests() {
    testCases.forEach(tc => {
        const result = matchRules(tc.employee, tc.accountId);
        console.log(`Test: ${tc.name}`);
        console.log(`  Result:`, result);
        console.log(`  Expected match: ${tc.expectedMatch}, Actual: ${result.matched}`);
        if (tc.expectedAction) {
            console.log(`  Expected action: ${JSON.stringify(tc.expectedAction)}`);
            console.log(`  Actual actions: ${JSON.stringify(result.actions)}`);
        }
        if (tc.expectedConflict) {
            console.log(`  Expected conflict: true, Actual: ${result.conflicts.length > 0}`);
        }
        console.log('---');
    });
}
```

- [ ] **Step 5: 测试并修复问题**

运行测试用例，修复匹配算法中的bug。

- [ ] **Step 6: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: implement rule matching algorithm with conflict detection"
```

---

## Task 4: 创建员工参保预览页集成

**Files:**
- Modify: `prototype/region-social-insurance-rules.html` (添加参保预览部分)

- [ ] **Step 1: 添加参保预览 Modal**

```html
<!-- 员工参保预览 Modal -->
<div class="qy-modal" id="insurance-preview-modal" style="display: none;">
    <div class="qy-modal__backdrop" onclick="closePreviewModal()"></div>
    <div class="qy-modal__container">
        <div class="qy-modal__header">
            <h2>参保确认</h2>
            <button class="qy-modal__close" onclick="closePreviewModal()">×</button>
        </div>
        <div class="qy-modal__body">
            <div class="employee-info">
                <p><strong>员工：</strong><span id="preview-employee-name">张三</span></p>
                <p><strong>参保户头：</strong><span id="preview-account-name">广州天河标准户</span></p>
            </div>

            <!-- 冲突提示 -->
            <div class="qy-alert qy-alert--warning" id="conflict-alert" style="display: none;">
                <h4>⚠️ 规则冲突</h4>
                <p>员工同时匹配了多条规则，存在以下冲突：</p>
                <div id="conflict-details"></div>
            </div>

            <!-- 规则来源 -->
            <div class="rule-source" id="rule-source">
                <span class="qy-tag qy-tag--info">规则来源</span>
                <span id="rule-source-text"></span>
            </div>

            <!-- 参保明细 -->
            <table class="qy-table">
                <thead>
                    <tr>
                        <th>险种</th>
                        <th>比例来源</th>
                        <th>比例值</th>
                        <th>金额（元）</th>
                    </tr>
                </thead>
                <tbody id="preview-insurance-body">
                </tbody>
            </table>
        </div>
        <div class="qy-modal__footer">
            <button class="qy-btn qy-btn--secondary" onclick="closePreviewModal()">取消</button>
            <button class="qy-btn qy-btn--primary" id="btn-confirm-insurance" onclick="confirmInsurance()">确认参保</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 实现参保预览逻辑**

```javascript
/**
 * 打开参保预览
 */
function openInsurancePreview(employeeId, accountId) {
    const employee = getEmployeeById(employeeId);
    const account = getAccountById(accountId);

    if (!employee || !account) return;

    // 执行规则匹配
    const matchResult = matchRules(employee, accountId);

    // 渲染预览
    document.getElementById('preview-employee-name').textContent = `${employee.name} (${employee.id})`;
    document.getElementById('preview-account-name').textContent = account.name;

    if (matchResult.conflicts.length > 0) {
        // 显示冲突
        document.getElementById('conflict-alert').style.display = 'block';
        document.getElementById('conflict-details').innerHTML = matchResult.conflicts.map(c => `
            <p><strong>冲突${matchResult.conflicts.indexOf(c) + 1}：${c.insuranceType}</strong></p>
            <ul>
                ${c.rules.map(r => `<li>规则${r.name}（优先级${r.priority}）：${r.action.type}</li>`).join('')}
            </ul>
        `).join('');
        document.getElementById('btn-confirm-insurance').disabled = true;
    } else {
        document.getElementById('conflict-alert').style.display = 'none';
        document.getElementById('btn-confirm-insurance').disabled = false;
    }

    // 显示规则来源
    if (matchResult.matched) {
        document.getElementById('rule-source-text').textContent =
            `${account.region.province}/${account.region.city}/${account.region.district} 规则 v${matchResult.ruleVersion}`;
    } else {
        document.getElementById('rule-source-text').textContent = '使用参保户头默认比例（无匹配规则）';
    }

    // 渲染参保明细
    renderInsurancePreview(matchResult.actions, account);

    document.getElementById('insurance-preview-modal').style.display = 'block';
}

function renderInsurancePreview(actions, account) {
    const insuranceTypes = ['工伤', '养老', '医疗', '失业', '生育', '公积金'];
    const salary = 8000; // 模拟工资基数

    const tbody = document.getElementById('preview-insurance-body');
    tbody.innerHTML = insuranceTypes.map(type => {
        const action = actions[type] || { type: 'account_ratio', value: account.defaultRatios[type] };
        const ratio = action.value / 100;
        const amount = salary * ratio;

        let sourceText = '';
        if (action.type === 'dispatch_ratio') {
            sourceText = `${action.source}比例`;
        } else if (action.type === 'specified_ratio') {
            sourceText = '指定比例';
        } else {
            sourceText = '参保户头比例';
        }

        return `
            <tr>
                <td>${type}</td>
                <td>${sourceText}</td>
                <td>${action.value}%</td>
                <td>${amount.toFixed(2)}</td>
            </tr>
        `;
    }).join('');
}
```

- [ ] **Step 3: 添加模拟数据**

```javascript
// 模拟员工数据
const mockEmployees = [
    { id: 'E001', name: '张三', type: '派遣员工', projectId: '项目A', customerId: '客户X', position: '技术岗', level: 'P5', dispatchUnitId: 'DU001' },
    { id: 'E002', name: '李四', type: '正式员工', projectId: '项目B', customerId: '客户Y', position: '销售岗', level: 'P6', dispatchUnitId: null },
    { id: 'E003', name: '王五', type: '派遣员工', projectId: '项目A', customerId: '客户X', position: '技术岗', level: 'P5', dispatchUnitId: 'DU001' }
];

// 模拟参保户头数据
const mockAccounts = [
    {
        id: 'ACC001',
        name: '广州天河标准户',
        region: { province: '广东省', city: '广州市', district: '天河区' },
        defaultRatios: { '工伤': 0.4, '养老': 14, '医疗': 8, '失业': 0.5, '生育': 0.8, '公积金': 12 }
    }
];

// 模拟派遣单位数据
const mockDispatchUnits = [
    { id: 'DU001', name: '派遣单位A', workInjuryRatio: 0.6 },
    { id: 'DU002', name: '派遣单位B', workInjuryRatio: 0.5 }
];

// 辅助函数
function getEmployeeById(id) { return mockEmployees.find(e => e.id === id); }
function getAccountById(id) { return mockAccounts.find(a => a.id === id); }
function getDispatchUnitById(id) { return mockDispatchUnits.find(d => d.id === id); }
function isWithinEffectPeriod(rule) {
    const today = new Date();
    const start = rule.effectStart ? new Date(rule.effectStart) : null;
    const end = rule.effectEnd ? new Date(rule.effectEnd) : null;
    if (start && today < start) return false;
    if (end && today > end) return false;
    return true;
}
```

- [ ] **Step 4: 添加演示按钮**

```html
<!-- 在页面底部添加演示区域 -->
<div class="demo-section">
    <h3>参保预览演示</h3>
    <div class="demo-controls">
        <select id="demo-employee" class="qy-select">
            <option value="E001">张三（派遣员工+项目A）</option>
            <option value="E002">李四（正式员工）</option>
            <option value="E003">王五（派遣员工+项目A+P5）</option>
        </select>
        <select id="demo-account" class="qy-select">
            <option value="ACC001">广州天河标准户</option>
        </select>
        <button class="qy-btn qy-btn--primary" onclick="openInsurancePreviewDemo()">预览参保</button>
    </div>
</div>
```

- [ ] **Step 5: 测试参保预览功能**

测试场景：
1. 选择「张三」→ 点击预览 → 应显示使用了派遣单位A的0.6%工伤比例
2. 选择「李四」→ 点击预览 → 应显示使用参保户头默认比例（无匹配规则）
3. 选择「王五」→ 点击预览 → 应显示冲突提示（同时匹配两条规则）

- [ ] **Step 6: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: add insurance preview modal with rule matching integration"
```

---

## Task 5: 实现版本历史和回滚功能

**Files:**
- Modify: `prototype/region-social-insurance-rules.html`

- [ ] **Step 1: 添加版本历史 Modal**

```html
<!-- 版本历史 Modal -->
<div class="qy-modal" id="history-modal" style="display: none;">
    <div class="qy-modal__backdrop" onclick="closeHistoryModal()"></div>
    <div class="qy-modal__container qy-modal__container--lg">
        <div class="qy-modal__header">
            <h2 id="history-title">规则历史</h2>
            <button class="qy-modal__close" onclick="closeHistoryModal()">×</button>
        </div>
        <div class="qy-modal__body">
            <table class="qy-table">
                <thead>
                    <tr>
                        <th>版本</th>
                        <th>状态</th>
                        <th>修改时间</th>
                        <th>修改人</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody id="history-list-body">
                </tbody>
            </table>
            <div id="history-detail" class="history-detail" style="display: none;">
                <h4>版本详情</h4>
                <div id="history-detail-content"></div>
            </div>
        </div>
        <div class="qy-modal__footer">
            <button class="qy-btn qy-btn--secondary" onclick="closeHistoryModal()">关闭</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 实现版本历史逻辑**

```javascript
// 版本历史数据（模拟）
const ruleHistory = {
    'R001': [
        { version: 3, status: 'active', modifiedAt: '2026-04-10 10:00', modifiedBy: '张三',
          snapshot: { conditions: [...], actions: {...} } },
        { version: 2, status: 'inactive', modifiedAt: '2026-04-05 14:30', modifiedBy: '李四',
          snapshot: { conditions: [...], actions: {...} } },
        { version: 1, status: 'inactive', modifiedAt: '2026-04-01 09:00', modifiedBy: '王五',
          snapshot: { conditions: [...], actions: {...} } }
    ]
};

function showHistory(ruleId) {
    const history = ruleHistory[ruleId] || [];
    const rule = mockRules.find(r => r.id === ruleId);

    document.getElementById('history-title').textContent = `规则历史 - ${rule?.name || ruleId}`;

    const tbody = document.getElementById('history-list-body');
    tbody.innerHTML = history.map(h => `
        <tr>
            <td>v${h.version} ${h.status === 'active' ? '●' : ''}</td>
            <td>${h.status === 'active' ? '当前生效' : '已停用'}</td>
            <td>${h.modifiedAt}</td>
            <td>${h.modifiedBy}</td>
            <td>
                <button class="qy-btn qy-btn--text" onclick="viewHistoryVersion('${ruleId}', ${h.version})">查看</button>
                ${h.status !== 'active' ? `<button class="qy-btn qy-btn--text" onclick="rollback('${ruleId}', ${h.version})">回滚</button>` : ''}
            </td>
        </tr>
    `).join('');

    document.getElementById('history-modal').style.display = 'block';
}

function viewHistoryVersion(ruleId, version) {
    const history = ruleHistory[ruleId] || [];
    const snapshot = history.find(h => h.version === version);
    if (!snapshot) return;

    document.getElementById('history-detail').style.display = 'block';
    document.getElementById('history-detail-content').innerHTML = `
        <p><strong>地区：</strong>${snapshot.region?.province || ''}/${snapshot.region?.city || ''}/${snapshot.region?.district || ''}</p>
        <p><strong>条件：</strong>${JSON.stringify(snapshot.conditions)}</p>
        <p><strong>动作：</strong>${JSON.stringify(snapshot.actions)}</p>
    `;
}

function rollback(ruleId, version) {
    if (confirm(`确定回滚到 v${version} 版本吗？`)) {
        // 实际应用中这里会调用API
        alert(`已回滚到 v${version} 版本`);
        closeHistoryModal();
        renderRuleList(mockRules);
    }
}
```

- [ ] **Step 3: 测试版本历史功能**

- 点击某规则的「历史」按钮 → Modal 正确显示版本列表
- 点击「查看」→ 显示版本详情
- 点击「回滚」→ 确认后刷新列表

- [ ] **Step 4: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: add version history and rollback functionality"
```

---

## Task 6: 实现批量导入预览功能

**Files:**
- Modify: `prototype/region-social-insurance-rules.html`

- [ ] **Step 1: 添加批量导入 Modal**

```html
<!-- 批量导入预览 Modal -->
<div class="qy-modal" id="import-modal" style="display: none;">
    <div class="qy-modal__backdrop" onclick="closeImportModal()"></div>
    <div class="qy-modal__container qy-modal__container--lg">
        <div class="qy-modal__header">
            <h2>批量导入预览</h2>
            <button class="qy-modal__close" onclick="closeImportModal()">×</button>
        </div>
        <div class="qy-modal__body">
            <div class="import-summary">
                <p>共导入 <strong id="import-total">156</strong> 条，其中：</p>
                <ul>
                    <li>✅ <span id="import-success">140</span> 条规则匹配成功</li>
                    <li>⚠️ <span id="import-conflict">16</span> 条存在冲突</li>
                </ul>
            </div>

            <div class="conflict-list" id="conflict-list">
                <h4>冲突明细</h4>
                <table class="qy-table">
                    <thead>
                        <tr>
                            <th>员工</th>
                            <th>冲突险种</th>
                            <th>涉及规则</th>
                        </tr>
                    </thead>
                    <tbody id="conflict-list-body">
                    </tbody>
                </table>
            </div>
        </div>
        <div class="qy-modal__footer">
            <button class="qy-btn qy-btn--secondary" onclick="exportConflictDetail()">导出冲突明细</button>
            <button class="qy-btn qy-btn--secondary" onclick="processSuccessOnly()">仅处理成功项</button>
            <button class="qy-btn qy-btn--secondary" onclick="closeImportModal()">取消</button>
        </div>
    </div>
</div>
```

- [ ] **Step 2: 实现批量导入预览逻辑**

```javascript
// 模拟导入数据
const mockImportData = [
    { employeeId: 'E001', accountId: 'ACC001' },
    { employeeId: 'E002', accountId: 'ACC001' },
    { employeeId: 'E003', accountId: 'ACC001' }
];

function simulateBatchImport() {
    const results = { success: 0, conflicts: [] };

    mockImportData.forEach(data => {
        const employee = getEmployeeById(data.employeeId);
        const account = getAccountById(data.accountId);
        const matchResult = matchRules(employee, account.id);

        if (matchResult.conflicts.length > 0) {
            results.conflicts.push({
                employee,
                matchResult
            });
        } else {
            results.success++;
        }
    });

    // 显示预览
    document.getElementById('import-total').textContent = mockImportData.length;
    document.getElementById('import-success').textContent = results.success;
    document.getElementById('import-conflict').textContent = results.conflicts.length;

    // 渲染冲突列表
    const tbody = document.getElementById('conflict-list-body');
    tbody.innerHTML = results.conflicts.map(c => `
        <tr>
            <td>${c.employee.name}</td>
            <td>${c.matchResult.conflicts.map(ch => ch.insuranceType).join(', ')}</td>
            <td>${c.matchResult.conflicts[0]?.rules.map(r => r.name).join(', ')}</td>
        </tr>
    `).join('');

    document.getElementById('import-modal').style.display = 'block';
}

function processSuccessOnly() {
    alert('已处理 140 条成功记录');
    closeImportModal();
}

function exportConflictDetail() {
    alert('导出冲突明细 Excel');
}
```

- [ ] **Step 3: 测试批量导入预览**

- 调用 `simulateBatchImport()` → 显示预览 Modal
- 成功数和冲突数正确显示
- 冲突明细列表正确

- [ ] **Step 4: 提交**

```bash
git add prototype/region-social-insurance-rules.html
git commit -m "feat: add batch import preview with conflict detection"
```

---

## 验收标准检查清单

- [ ] 规则列表页正确渲染，预置3条示例规则
- [ ] 新建/编辑 Modal 可打开，表单完整
- [ ] 条件构建器支持添加/删除条件组，添加/删除条件项
- [ ] 动作配置支持险种选择和动作类型切换
- [ ] 规则匹配算法正确评估条件
- [ ] 冲突检测正确识别同险种不同规则
- [ ] 员工参保预览显示规则来源和实际比例
- [ ] 版本历史 Modal 显示历史版本列表
- [ ] 批量导入预览显示成功/冲突统计
- [ ] 所有交互符合青阳云设计系统风格

---

## 执行方式

**Plan complete and saved to `docs/superpowers/plans/2026-04-10-region-social-insurance-rule-plan.md`.**

**Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**
