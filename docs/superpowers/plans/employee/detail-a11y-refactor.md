# 员工详情页 UX与无障碍(A11y)重构计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复 `prototype/employee-detail-redesign.html` 中的 UX 架构缺陷和无障碍规范（A11y）问题，包括调整主卡片位置、替换具有点击事件的 `div` 为 `button`、修复表单 `label` 关联等。

**Architecture:** 
1. 提取 `.employee-hero-panel` 从右侧边栏（`.summary-section`）移动到页面最顶部的通栏位置。
2. 移除 CSS 中性能不佳的 `transition: all`，替换为具体属性。
3. 批量修正 Tab 项 HTML 语义，将 `<div class="tab-item">` 替换为 `<button class="tab-item">`，以符合 Web Interface Guidelines 要求。
4. 为模态框中的表单 `<label>` 增加 `for` 属性，并为对应的 `<input>` / `<select>` 增加 `id` 属性。

**Tech Stack:** HTML5, CSS3 (原生)

---

### Task 1: 调整主卡片布局至顶部

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 提取 `.employee-hero-panel` HTML 结构**
将 `<section class="employee-hero-panel">...</section>` 从 `<div class="summary-section">` 内部剪切，并粘贴到 `<main class="main-content">` 内部的最顶部（紧挨着 `<main class="main-content">` 的下一行，在 `<div class="content-layout">` 之前）。

- [ ] **Step 2: 删除无用的右侧摘要区外壳**
在将 `employee-hero-panel` 和 `timeline-section` 移出或重组后，如果右侧边栏没有其他内容，需进行清理。
为了保持简单，我们暂时只将 `.employee-hero-panel` 移动到最顶部。将 `<section class="timeline-section" id="timelineSection">` 移动到 `.detail-section` 内部的底部，或者作为一个独立的区域。
目前计划：将 `.employee-hero-panel` 放在 `<div class="content-layout">` 的上方。

```html
<!-- 原结构 -->
    <main class="main-content">
        <div class="content-layout">
            <div class="detail-section">...</div>
            <div class="summary-section">
                <section class="employee-hero-panel">...</section>
                <section class="timeline-section">...</section>
            </div>
        </div>

<!-- 新结构 -->
    <main class="main-content">
        <section class="employee-hero-panel">...</section>
        <div class="content-layout">
            <div class="detail-section">...</div>
            <div class="summary-section">
                <section class="timeline-section">...</section>
            </div>
        </div>
```

- [ ] **Step 3: 调整 `.content-layout` 的 CSS**
将 `content-layout` 的布局列宽从 `1fr 380px` 修改为 `1fr 320px`（因为顶部主卡片已经移出，右侧现在只有动态记录，不需要太宽）。

```css
        /* 左右布局容器 */
        .content-layout {
            display: grid;
            grid-template-columns: 1fr 320px;
            gap: 24px;
            align-items: start;
        }
```

- [ ] **Step 4: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: move employee hero panel to top level"
```

---

### Task 2: 修复 `transition: all` 反模式

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 替换 CSS 中的 `transition: all`**
搜索文件中的 `transition: all 0.2s;`，将其替换为明确的属性。

1. 对于 `.btn` (行 59)：改为 `transition: background-color 0.2s, border-color 0.2s, color 0.2s;`
2. 对于 `.btn-hero` (行 280)：改为 `transition: background-color 0.2s, border-color 0.2s, color 0.2s;`
3. 对于 `.modal-close` (行 513)：改为 `transition: background-color 0.2s, color 0.2s;`
4. 对于 `.form-input` (行 559)：改为 `transition: border-color 0.2s, box-shadow 0.2s;`
5. 对于 `.tab-item` (行 602)：改为 `transition: color 0.2s, border-color 0.2s;`
6. 对于 `.tab-more` (行 641)：改为 `transition: background-color 0.2s, color 0.2s;`
7. 对于 `.info-card-header` (行 770)：如果存在，改为 `transition: background-color 0.2s;`

- [ ] **Step 2: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "style: replace transition all with explicit properties"
```

---

### Task 3: 修复 Tab 导航的 HTML 语义 (Accessibility)

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 将 `<div class="tab-item">` 替换为 `<button class="tab-item">`**
在 `.tabs-nav` 容器内，将所有 `div` 改为 `button`。

```html
                        <div class="tabs-nav">
                            <button class="tab-item active" data-tab="0">基础信息</button>
                            <button class="tab-item" data-tab="1">合同信息</button>
                            <button class="tab-item" data-tab="2">银行卡信息</button>
                            <button class="tab-item" data-tab="3">教育经历</button>
                            <button class="tab-item" data-tab="4">工作经历</button>
                            <button class="tab-item" data-tab="5">家庭成员</button>
                            <button class="tab-item" data-tab="6">紧急联系人</button>
                            <button class="tab-item" data-tab="7">员工证书</button>
                            <button class="tab-item" data-tab="8">个人材料</button>
                            <button class="tab-item" data-tab="9">薪税档案</button>
                            <button class="tab-item" data-tab="10">参保档案</button>
                        </div>
```

- [ ] **Step 2: 调整 `.tab-item` 的 CSS 样式以重置 button 默认样式**
在 `.tab-item` 的 CSS 类中，确保添加 `background: none; border: none; border-bottom: 2px solid transparent; font-family: inherit;`，以防止原生的 button 背景和边框干扰设计。

```css
        .tab-item {
            padding: 16px 20px;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            background: none;
            border: none;
            border-bottom: 2px solid transparent;
            font-family: inherit;
            transition: color 0.2s, border-color 0.2s;
            white-space: nowrap;
        }
```

- [ ] **Step 3: 将“更多”下拉触发器也改为 button**
```html
                        <button class="tab-more hidden" id="tabMore">
                            更多
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <polyline points="6 9 12 15 18 9"/>
                            </svg>
                            <div class="tab-more-dropdown" id="tabMoreDropdown"></div>
                        </button>
```

```css
        .tab-more {
            background: none;
            border: none;
            font-family: inherit;
            /* 保留其他原有样式 */
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 16px 20px;
            font-size: 14px;
            font-weight: 500;
            color: var(--text-secondary);
            cursor: pointer;
            transition: background-color 0.2s, color 0.2s;
            position: relative;
        }
```

- [ ] **Step 4: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "refactor: use button tags for interactive tab elements"
```

---

### Task 4: 修复表单 Label 关联性 (Accessibility)

**Files:**
- Modify: `prototype/employee-detail-redesign.html`

- [ ] **Step 1: 修改“添加合同”模态框中的 HTML**
为每个 label 添加 `for` 属性，并为对应的 input/select 添加 `id` 属性。
查找 `document.getElementById('addContract')` 处的模板字符串：

```javascript
        // 添加合同
        document.getElementById('addContract')?.addEventListener('click', function() {
            openModal('添加合同', `
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label required" for="contract-no">合同编号</label>
                        <input type="text" id="contract-no" class="form-input" placeholder="HT2026000001">
                    </div>
                    <div class="form-group">
                        <label class="form-label required" for="contract-type">合同类型</label>
                        <select id="contract-type" class="form-input">
                            <option>劳动合同</option>
                            <option>实习协议</option>
                            <option>劳务协议</option>
                        </select>
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label required" for="contract-start">开始日期</label>
                        <input type="date" id="contract-start" class="form-input" value="2026-01-01">
                    </div>
                    <div class="form-group">
                        <label class="form-label required" for="contract-end">结束日期</label>
                        <input type="date" id="contract-end" class="form-input" value="2029-01-01">
                    </div>
                </div>
                <div class="form-group">
                    <label class="form-label" for="contract-note">备注</label>
                    <textarea id="contract-note" class="form-input" rows="3" placeholder="请输入备注信息"></textarea>
                </div>
            `);
        });
```

- [ ] **Step 2: 修改“添加银行卡”模态框中的 HTML**
查找 `document.getElementById('addBankCard')` 处的模板字符串并应用相同的修改：

```javascript
        // 添加银行卡
        document.getElementById('addBankCard')?.addEventListener('click', function() {
            openModal('添加银行卡', `
                <div class="form-group">
                    <label class="form-label required" for="bank-account">银行卡号</label>
                    <input type="text" id="bank-account" class="form-input" placeholder="6222024000061234567">
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label required" for="bank-name">开户银行</label>
                        <input type="text" id="bank-name" class="form-input" placeholder="中国工商银行">
                    </div>
                    <div class="form-group">
                        <label class="form-label required" for="bank-branch">开户支行</label>
                        <input type="text" id="bank-branch" class="form-input" placeholder="深圳分行">
                    </div>
                </div>
                <div class="form-row">
                    <div class="form-group">
                        <label class="form-label required" for="bank-user">开户姓名</label>
                        <input type="text" id="bank-user" class="form-input" placeholder="请输入姓名">
                    </div>
                    <div class="form-group">
                        <label class="form-label required" for="bank-id">证件号码</label>
                        <input type="text" id="bank-id" class="form-input" placeholder="身份证号码">
                    </div>
                </div>
                <div class="form-group" style="display:flex;align-items:center;gap:8px;">
                    <input type="checkbox" id="is-default" checked>
                    <label class="form-label" for="is-default" style="margin-bottom:0;">设为默认</label>
                </div>
            `);
        });
```

- [ ] **Step 3: 批量修改其他模态框**
使用类似的方法修改 `addEducation`, `addWork`, `addFamily`, `addEmergency` 中的 label 和 input 的 for/id 关联。

- [ ] **Step 4: 为装饰性 SVG 添加 aria-hidden**
在全局搜索所有的 `<svg`（特别是那些没有在 `<button>` 或 `<a aria-label>` 里的装饰性图标），添加 `aria-hidden="true"`。
由于此项较多，至少在 `.info-card-title svg`、`.tab-more svg` 等明显的纯装饰性 SVG 上添加。

- [ ] **Step 5: Commit**
```bash
git add prototype/employee-detail-redesign.html
git commit -m "fix: improve accessibility with explicit form labels and aria attributes"
```