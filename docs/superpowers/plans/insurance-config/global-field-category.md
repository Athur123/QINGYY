# 全局字段配置：自定义分类（多选） Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在全局字段管理页中增加“自定义分类（多选）”，支持列表展示与筛选，以及在新增/编辑抽屉中选择/创建分类（分类非必填）。

**Architecture:** 在纯静态原型页内新增 `categories` 字典与字段的 `categoryIds` 多选关联；列表渲染分类 tag、筛选按包含关系过滤；抽屉提供轻量多选选择器（搜索+创建+已选标签）。

**Tech Stack:** HTML + CSS + Vanilla JS（现有原型风格与青阳云 design tokens）

---

## Files Overview

**Modify**
- [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

**Docs (already done)**
- [2026-04-28-global-field-config-category-multiselect-design.md](file:///Users/athur/PycharmProjects/qyy/docs/superpowers/specs/2026-04-28-global-field-config-category-multiselect-design.md)

---

### Task 1: 建立分类数据模型与字段关联

**Files:**
- Modify: [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

- [ ] **Step 1: 为原型新增 categories 数据源**

在 `<script>` 的 Data 区域新增：

```js
let categories = [
  { id: 1, name: '合同' },
  { id: 2, name: '证件' },
  { id: 3, name: '银行' },
  { id: 4, name: '社保' },
];
let nextCategoryId = 5;
```

- [ ] **Step 2: 为 fields 补充 categoryIds（示例数据）**

将 `fields` 每条数据补齐 `categoryIds: []`（允许为空），并为部分字段填充示例：

```js
{ id: 2, code: 'contract_start_date', ..., categoryIds: [1], ... }
{ id: 4, code: 'id_card_front', ..., categoryIds: [2], ... }
{ id: 9, code: 'bank_account', ..., categoryIds: [3], ... }
{ id: 8, code: 'social_security_card', ..., categoryIds: [4], ... }
```

- [ ] **Step 3: 确保复制/保存逻辑携带 categoryIds**

需要修改：
- `saveField()`：读写 `categoryIds`
- `openAddDrawer()` / `openEditDrawer()`：初始化/回填分类选择
- `duplicateField()`：复制字段时同步复制 `categoryIds`

- [ ] **Step 4: 自测（控制台）**

打开 HTML 后执行：
- 新建字段保存后 `fields` 中应包含 `categoryIds`
- 复制字段后新字段应保留原分类

---

### Task 2: 列表增加“分类”列与渲染规则（最多 2 个 + “+N”）

**Files:**
- Modify: [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

- [ ] **Step 1: 表头新增“分类”列**

在表头 `<th>` 中插入一列（建议放在“值来源”和“自动获取路径”之间或“字段名称”之后，按现有列宽微调）：

```html
<th style="width: 180px;">分类</th>
```

- [ ] **Step 2: 增加分类名称映射与渲染函数**

在 Utils 或 Render 附近新增 helper：

```js
function normalizeCategoryName(name) {
  return (name || '').trim().replace(/\s+/g, ' ').toLowerCase();
}

function getCategoryById(id) {
  return categories.find(c => c.id === id);
}

function renderCategoryCell(categoryIds = []) {
  if (!categoryIds.length) return '<span style="color:var(--qy-text-disabled);">-</span>';
  const names = categoryIds.map(id => getCategoryById(id)?.name).filter(Boolean);
  if (!names.length) return '<span style="color:var(--qy-text-disabled);">-</span>';
  const shown = names.slice(0, 2);
  const rest = names.length - shown.length;
  const title = names.join('、');
  const tags = shown.map(n => `<span class="tag tag--gray" title="${esc(title)}">${esc(n)}</span>`).join(' ');
  const more = rest > 0 ? ` <span class="tag tag--gray" title="${esc(title)}">+${rest}</span>` : '';
  return tags + more;
}
```

- [ ] **Step 3: 行渲染中输出分类列**

在 `renderTable()` 的 `tbody.innerHTML = filtered.map(...)` 行模板中插入：

```html
<td>${renderCategoryCell(f.categoryIds)}</td>
```

- [ ] **Step 4: 样式对齐**

复用现有 `.tag` / `.tag--gray`，必要时补一个更适合分类的颜色（仍使用 design tokens）。

- [ ] **Step 5: 自测**

验证：
- 0 个分类显示 `-`
- 1-2 个分类显示 1-2 个 tag
- ≥3 个显示前 2 个 + `+N`，hover title 展示全量

---

### Task 3: 列表新增“分类筛选”（与现有筛选组合生效）

**Files:**
- Modify: [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

- [ ] **Step 1: 筛选区新增分类筛选控件**

在 `.filter-bar` 内新增控件（先用原生 `<select>`，保持原型轻量）：

```html
<select class="filter-select" id="filter-category" onchange="renderTable()">
  <option value="">全部分类</option>
</select>
```

- [ ] **Step 2: 渲染分类筛选选项**

在 Init 或 `renderTable()` 前新增：

```js
function renderCategoryFilterOptions() {
  const sel = document.getElementById('filter-category');
  if (!sel) return;
  const current = sel.value;
  sel.innerHTML = ['<option value="">全部分类</option>']
    .concat(categories.map(c => `<option value="${c.id}">${esc(c.name)}</option>`))
    .join('');
  sel.value = current;
}
```

并在 `renderTable()` 前调用一次、以及新增分类后调用。

- [ ] **Step 3: 过滤逻辑加入分类**

在 `renderTable()` 和 `getFilteredIds()` 的 filter 条件中加入：

```js
const filterCategory = document.getElementById('filter-category')?.value || '';
const filterCategoryId = filterCategory ? Number(filterCategory) : null;
...
if (filterCategoryId && !(f.categoryIds || []).includes(filterCategoryId)) return false;
```

- [ ] **Step 4: 自测**

验证组合筛选：
- 分类 + 关键字
- 分类 + 类型
- 分类 + 来源

---

### Task 4: 抽屉新增“分类（多选 + 可创建）”选择器

**Files:**
- Modify: [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

- [ ] **Step 1: 抽屉表单新增分类表单项（非必填）**

建议放在“字段类型/值来源”之后、“自动获取路径”之前：

```html
<div class="form-group">
  <label class="form-label">分类</label>
  <div id="categoryPicker"></div>
  <div class="form-hint">可选：用于在业务模块中更快筛选与定位字段</div>
</div>
```

- [ ] **Step 2: 实现 categoryPicker 结构（已选 tags + 输入框 + 建议列表）**

新增状态：

```js
let selectedCategoryIds = [];
let categoryQuery = '';
```

新增渲染函数：

```js
function renderCategoryPicker() {
  const el = document.getElementById('categoryPicker');
  if (!el) return;
  const selected = selectedCategoryIds.map(id => getCategoryById(id)).filter(Boolean);
  const q = (categoryQuery || '').trim();
  const qNorm = normalizeCategoryName(q);
  const suggestions = q
    ? categories.filter(c => !selectedCategoryIds.includes(c.id) && normalizeCategoryName(c.name).includes(qNorm))
    : categories.filter(c => !selectedCategoryIds.includes(c.id)).slice(0, 6);
  const existsExact = q && categories.some(c => normalizeCategoryName(c.name) === qNorm);

  el.innerHTML = `
    <div style="display:flex; flex-wrap:wrap; gap:8px; align-items:center; padding:8px; border:1px solid var(--qy-border-medium); border-radius: var(--qy-radius-md); background: var(--qy-bg-primary);">
      ${selected.map(c => `
        <span class="tag tag--gray" title="${esc(c.name)}" style="display:inline-flex; align-items:center; gap:6px;">
          ${esc(c.name)}
          <button type="button" class="qy-btn-action qy-btn-action--text" style="height:18px; padding:0 6px;" onclick="removeCategory(${c.id})">×</button>
        </span>
      `).join('')}
      <input id="categoryInput" class="form-input" style="height:28px; width:180px; border:none; outline:none; box-shadow:none; padding:0; background:transparent;" placeholder="搜索或创建分类" value="${esc(categoryQuery)}">
    </div>
    <div id="categorySuggest" style="margin-top:8px; display:${(q || suggestions.length) ? 'block' : 'none'};">
      ${q && !existsExact ? `<button type="button" class="qy-btn-action qy-btn-action--text" onclick="createAndSelectCategory('${q.replace(/'/g, \"\\\\'\")}')">创建分类：${esc(q)}</button>` : ''}
      ${suggestions.map(c => `<button type="button" class="qy-btn-action qy-btn-action--text" onclick="selectCategory(${c.id})">${esc(c.name)}</button>`).join(' ')}
    </div>
  `;

  const input = document.getElementById('categoryInput');
  if (input) {
    input.oninput = e => { categoryQuery = e.target.value; renderCategoryPicker(); };
    input.onkeydown = e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        const v = (categoryQuery || '').trim();
        if (!v) return;
        createAndSelectCategory(v);
      }
    };
  }
}
```

新增操作函数：

```js
function selectCategory(id) {
  if (!selectedCategoryIds.includes(id)) selectedCategoryIds.push(id);
  categoryQuery = '';
  renderCategoryPicker();
}

function removeCategory(id) {
  selectedCategoryIds = selectedCategoryIds.filter(x => x !== id);
  renderCategoryPicker();
}

function createAndSelectCategory(name) {
  const raw = (name || '').trim();
  if (!raw) return;
  const norm = normalizeCategoryName(raw);
  const existing = categories.find(c => normalizeCategoryName(c.name) === norm);
  if (existing) {
    selectCategory(existing.id);
    return;
  }
  const c = { id: nextCategoryId++, name: raw };
  categories.push(c);
  renderCategoryFilterOptions();
  selectCategory(c.id);
}
```

- [ ] **Step 3: 抽屉打开时初始化 selectedCategoryIds**

在 `openAddDrawer()`：

```js
selectedCategoryIds = [];
categoryQuery = '';
renderCategoryPicker();
```

在 `openEditDrawer(id)`：

```js
selectedCategoryIds = [...(f.categoryIds || [])];
categoryQuery = '';
renderCategoryPicker();
```

- [ ] **Step 4: saveField() 写入 categoryIds**

在 `saveField()` 读取分类：

```js
const categoryIds = [...selectedCategoryIds];
```

并在保存时 `Object.assign` / `fields.push` 中带上 `categoryIds`。

- [ ] **Step 5: 自测**

验证：
- 可多选
- 可搜索
- 回车创建并自动选中
- 同名不重复创建（忽略大小写/空格）
- 编辑字段回显分类
- 保存后列表分类列同步更新

---

### Task 5: 手工验收与回归检查

**Files:**
- Modify: [field-collection-config-demo.html](file:///Users/athur/PycharmProjects/qyy/prototype/field-collection-config-demo.html)

- [ ] **Step 1: 回归核心流程**

逐条检查：
- 新增字段（无分类/有分类/多分类）
- 编辑字段（分类回显、增删分类）
- 分类筛选与其他筛选组合
- 复制字段（分类跟随）
- 删除/批量删除（不受分类影响）
- 引用弹窗（不受分类影响）
- 拖拽排序（不受分类影响）

- [ ] **Step 2: 浏览器控制台无报错**

打开页面，确保 Console 无红色错误。

---

## Self-Review Checklist (Plan)
- 覆盖 spec：分类字典、字段多选、列表列展示、分类筛选、抽屉内创建/选择、非必填
- 无占位符：所有步骤含具体代码与插入点
- 命名一致：`categories/nextCategoryId/categoryIds/selectedCategoryIds`

