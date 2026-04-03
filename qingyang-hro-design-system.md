# 青阳云HRO设计系统 v1.0

> **类型**: B2B SaaS / 企业级人力资源管理系统  
> **风格**: Professional / Clean / Efficient  
> **版本**: v1.0  
> **日期**: 2026-04-03

---

## 快速开始

### 引入设计系统

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题 - 青阳云HRO</title>
  
  <!-- 字体 -->
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- 设计系统CSS -->
  <link rel="stylesheet" href="../styles/qingyang-design-system.css">
</head>
<body>
  <!-- 页面内容 -->
</body>
</html>
```

### CSS变量（必须）

```css
:root {
  /* ========== 主色板 ========== */
  --qy-primary-50:  #EFF6FF;
  --qy-primary-100: #DBEAFE;
  --qy-primary-200: #BFDBFE;
  --qy-primary-300: #93C5FD;
  --qy-primary-400: #60A5FA;
  --qy-primary-500: #2563EB;  /* 主色 */
  --qy-primary-600: #1D4ED8;
  --qy-primary-700: #1E40AF;

  /* ========== 语义色 ========== */
  --qy-success-50:  #F0FDF4;
  --qy-success-500: #22C55E;
  --qy-success-600: #16A34A;
  
  --qy-warning-50:  #FFF7ED;
  --qy-warning-500: #F97316;  /* 注意：对比度不足，需配图标 */
  --qy-warning-600: #EA580C;  /* 推荐用于文字 */
  
  --qy-error-50:    #FEF2F2;
  --qy-error-500:   #EF4444;
  --qy-error-600:   #DC2626;

  /* ========== 中性色 ========== */
  --qy-bg-primary:   #FFFFFF;
  --qy-bg-secondary: #F8FAFC;
  --qy-bg-tertiary:  #F1F5F9;
  
  --qy-text-primary:   #1E293B;   /* 11.5:1 对比度 */
  --qy-text-secondary: #64748B;   /* 5.7:1 对比度 */
  --qy-text-muted:     #94A3B8;   /* 3.3:1 对比度，仅用于占位符 */
  --qy-text-disabled:  #CBD5E1;
  
  --qy-border-light:   #E2E8F0;
  --qy-border-medium:  #CBD5E1;
  --qy-border-focus:   #60A5FA;

  /* ========== 字体 ========== */
  --qy-font-family: "Plus Jakarta Sans", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  
  --qy-font-size-xs:   11px;
  --qy-font-size-sm:   12px;
  --qy-font-size-base: 14px;   /* 正文 */
  --qy-font-size-md:   14px;
  --qy-font-size-lg:   16px;
  --qy-font-size-xl:   20px;
  --qy-font-size-2xl:  24px;

  --qy-font-weight-normal:  400;
  --qy-font-weight-medium:  500;
  --qy-font-weight-semibold: 600;
  --qy-font-weight-bold:    700;

  --qy-line-height-tight: 1.3;
  --qy-line-height-normal: 1.5;
  --qy-line-height-relaxed: 1.6;

  /* ========== 间距（4px基准） ========== */
  --qy-space-1: 4px;
  --qy-space-2: 8px;
  --qy-space-3: 12px;
  --qy-space-4: 16px;
  --qy-space-5: 20px;
  --qy-space-6: 24px;
  --qy-space-8: 32px;
  --qy-space-10: 40px;
  --qy-space-12: 48px;

  /* ========== 圆角 ========== */
  --qy-radius-sm: 4px;
  --qy-radius-md: 8px;
  --qy-radius-lg: 12px;
  --qy-radius-xl: 16px;
  --qy-radius-full: 9999px;

  /* ========== 阴影 ========== */
  --qy-shadow-sm: 0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02);
  --qy-shadow-md: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
  --qy-shadow-card: 0 2px 8px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.03);
  --qy-shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);

  /* ========== 过渡 ========== */
  --qy-transition-fast: 150ms ease;
  --qy-transition-normal: 200ms ease;
  --qy-transition-slow: 300ms ease;

  /* ========== 焦点环 ========== */
  --qy-focus-ring: 0 0 0 3px var(--qy-primary-100);
  --qy-focus-ring-offset: 2px;

  /* ========== 布局 ========== */
  --qy-sidebar-width: 220px;
  --qy-header-height: 52px;
  --qy-content-padding: 24px;
}
```

---

## 基础样式

### 重置与基础

```css
/* ========== 重置 ========== */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  font-family: var(--qy-font-family);
  font-size: var(--qy-font-size-base);
  line-height: var(--qy-line-height-relaxed);
  color: var(--qy-text-primary);
  background-color: var(--qy-bg-secondary);
}

/* ========== Skip Link ========== */
.qy-skip-link {
  position: absolute;
  top: -100%;
  left: 50%;
  transform: translateX(-50%);
  padding: var(--qy-space-2) var(--qy-space-4);
  background: var(--qy-primary-500);
  color: white;
  border-radius: var(--qy-radius-md);
  z-index: 9999;
  transition: top var(--qy-transition-fast);
}

.qy-skip-link:focus {
  top: var(--qy-space-4);
}

/* ========== Focus States ========== */
*:focus-visible {
  outline: none;
  box-shadow: var(--qy-focus-ring);
}

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 组件库

### 1. 按钮 Button

#### 主按钮 Primary

```html
<button class="qy-btn qy-btn--primary">主要操作</button>
<button class="qy-btn qy-btn--primary" disabled>禁用状态</button>
```

```css
.qy-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--qy-space-2);
  padding: 0 var(--qy-space-4);
  font-family: inherit;
  font-size: var(--qy-font-size-base);
  font-weight: var(--qy-font-weight-medium);
  line-height: 1;
  border: 1px solid transparent;
  border-radius: var(--qy-radius-md);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
  white-space: nowrap;
}

/* 尺寸 */
.qy-btn--sm {
  height: 28px;
  font-size: var(--qy-font-size-sm);
}

.qy-btn--md {
  height: 32px;
}

.qy-btn--lg {
  height: 40px;
  padding: 0 var(--qy-space-5);
}

/* 主按钮 */
.qy-btn--primary {
  height: 32px;
  background: var(--qy-primary-500);
  color: white;
}

.qy-btn--primary:hover:not(:disabled) {
  background: var(--qy-primary-600);
}

.qy-btn--primary:active:not(:disabled) {
  background: var(--qy-primary-700);
}

.qy-btn--primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 次按钮 */
.qy-btn--secondary {
  height: 32px;
  background: white;
  border-color: var(--qy-border-medium);
  color: var(--qy-text-secondary);
}

.qy-btn--secondary:hover:not(:disabled) {
  background: var(--qy-bg-secondary);
  border-color: var(--qy-border-light);
}

/* 文字按钮 */
.qy-btn--text {
  height: 32px;
  background: transparent;
  color: var(--qy-primary-500);
}

.qy-btn--text:hover:not(:disabled) {
  background: var(--qy-primary-50);
}

/* 危险按钮 */
.qy-btn--danger {
  height: 32px;
  background: var(--qy-error-500);
  color: white;
}

.qy-btn--danger:hover:not(:disabled) {
  background: var(--qy-error-600);
}
```

#### 行内操作按钮 Row Action

```html
<button class="qy-btn-action qy-btn-action--primary">参保</button>
<button class="qy-btn-action qy-btn-action--warning">减员</button>
<button class="qy-btn-action qy-btn-action--text">详情</button>
```

```css
.qy-btn-action {
  display: inline-flex;
  align-items: center;
  height: 24px;
  padding: 0 var(--qy-space-3);
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  border: 1px solid;
  border-radius: var(--qy-radius-full);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
}

.qy-btn-action--primary {
  background: var(--qy-primary-50);
  border-color: var(--qy-primary-200);
  color: var(--qy-primary-600);
}

.qy-btn-action--warning {
  background: var(--qy-warning-50);
  border-color: var(--qy-warning-200);
  color: var(--qy-warning-600);
}

.qy-btn-action--text {
  background: transparent;
  border-color: transparent;
  color: var(--qy-primary-500);
}

.qy-btn-action:hover {
  filter: brightness(0.95);
}
```

---

### 2. 输入框 Input

```html
<div class="qy-form-group">
  <label class="qy-label" for="email">邮箱地址</label>
  <input class="qy-input" id="email" type="email" placeholder="请输入邮箱">
  <span class="qy-help-text">用于接收系统通知</span>
</div>

<div class="qy-form-group">
  <label class="qy-label" for="name">姓名 <span class="qy-required">*</span></label>
  <input class="qy-input qy-input--error" id="name" type="text" aria-invalid="true" aria-describedby="name-error">
  <span class="qy-error-text" id="name-error">请输入姓名</span>
</div>
```

```css
.qy-form-group {
  display: flex;
  flex-direction: column;
  gap: var(--qy-space-2);
}

.qy-label {
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-primary);
}

.qy-required {
  color: var(--qy-error-500);
  margin-left: var(--qy-space-1);
}

.qy-input {
  height: 32px;
  padding: 0 var(--qy-space-3);
  font-family: inherit;
  font-size: var(--qy-font-size-base);
  color: var(--qy-text-primary);
  background: var(--qy-bg-secondary);
  border: 1px solid var(--qy-border-medium);
  border-radius: var(--qy-radius-md);
  transition: all var(--qy-transition-fast);
}

.qy-input:hover:not(:disabled) {
  border-color: var(--qy-border-focus);
}

.qy-input:focus {
  outline: none;
  border-color: var(--qy-primary-400);
  box-shadow: var(--qy-focus-ring);
}

.qy-input::placeholder {
  color: var(--qy-text-muted);
}

.qy-input:disabled {
  background: var(--qy-bg-tertiary);
  color: var(--qy-text-disabled);
  cursor: not-allowed;
}

.qy-input--error {
  border-color: var(--qy-error-500);
}

.qy-input--error:focus {
  box-shadow: 0 0 0 3px var(--qy-error-50);
}

.qy-help-text {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
}

.qy-error-text {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-error-500);
}

/* 大尺寸 */
.qy-input--lg {
  height: 40px;
  padding: 0 var(--qy-space-4);
}
```

---

### 3. 下拉选择 Select

```html
<div class="qy-select-wrapper">
  <select class="qy-select">
    <option value="">请选择</option>
    <option value="1">选项1</option>
    <option value="2">选项2</option>
  </select>
</div>
```

```css
.qy-select-wrapper {
  position: relative;
}

.qy-select-wrapper::after {
  content: '';
  position: absolute;
  right: var(--qy-space-3);
  top: 50%;
  transform: translateY(-50%);
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
  border-top: 4px solid var(--qy-text-secondary);
  pointer-events: none;
}

.qy-select {
  appearance: none;
  width: 100%;
  height: 32px;
  padding: 0 var(--qy-space-8) 0 var(--qy-space-3);
  font-family: inherit;
  font-size: var(--qy-font-size-base);
  color: var(--qy-text-primary);
  background: var(--qy-bg-secondary);
  border: 1px solid var(--qy-border-medium);
  border-radius: var(--qy-radius-md);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
}

.qy-select:focus {
  outline: none;
  border-color: var(--qy-primary-400);
  box-shadow: var(--qy-focus-ring);
}
```

---

### 4. 卡片 Card

```html
<div class="qy-card">
  <div class="qy-card__header">
    <h3 class="qy-card__title">卡片标题</h3>
    <span class="qy-card__extra">额外信息</span>
  </div>
  <div class="qy-card__body">
    卡片内容区域
  </div>
  <div class="qy-card__footer">
    <button class="qy-btn qy-btn--secondary">取消</button>
    <button class="qy-btn qy-btn--primary">确认</button>
  </div>
</div>

<!-- KPI卡片 -->
<button class="qy-kpi-card" aria-pressed="false">
  <span class="qy-kpi-card__value">275</span>
  <span class="qy-kpi-card__label">全部</span>
</button>
```

```css
.qy-card {
  background: var(--qy-bg-primary);
  border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-lg);
  box-shadow: var(--qy-shadow-card);
}

.qy-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--qy-space-4) var(--qy-space-5);
  border-bottom: 1px solid var(--qy-border-light);
}

.qy-card__title {
  font-size: var(--qy-font-size-lg);
  font-weight: var(--qy-font-weight-semibold);
  color: var(--qy-text-primary);
}

.qy-card__extra {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
}

.qy-card__body {
  padding: var(--qy-space-5);
}

.qy-card__footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--qy-space-3);
  padding: var(--qy-space-4) var(--qy-space-5);
  border-top: 1px solid var(--qy-border-light);
}

/* KPI卡片 */
.qy-kpi-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: 120px;
  padding: var(--qy-space-4);
  background: white;
  border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-md);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
}

.qy-kpi-card:hover {
  background: var(--qy-bg-secondary);
}

.qy-kpi-card[aria-pressed="true"] {
  background: var(--qy-primary-50);
  border-color: var(--qy-primary-200);
}

.qy-kpi-card__value {
  font-size: 24px;
  font-weight: var(--qy-font-weight-bold);
  color: var(--qy-text-primary);
  font-variant-numeric: tabular-nums;
}

.qy-kpi-card[aria-pressed="true"] .qy-kpi-card__value {
  color: var(--qy-primary-600);
}

.qy-kpi-card__label {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
  margin-top: var(--qy-space-1);
}
```

---

### 5. 标签 Tag

```html
<span class="qy-tag">默认标签</span>
<span class="qy-tag qy-tag--primary">主要</span>
<span class="qy-tag qy-tag--success">成功</span>
<span class="qy-tag qy-tag--warning">警告</span>
<span class="qy-tag qy-tag--error">错误</span>
<span class="qy-tag qy-tag--dot qy-tag--success">带圆点</span>
```

```css
.qy-tag {
  display: inline-flex;
  align-items: center;
  height: 22px;
  padding: 0 var(--qy-space-3);
  font-size: var(--qy-font-size-xs);
  font-weight: var(--qy-font-weight-medium);
  border-radius: var(--qy-radius-full);
  white-space: nowrap;
}

.qy-tag--default {
  background: var(--qy-bg-secondary);
  color: var(--qy-text-secondary);
}

.qy-tag--primary {
  background: var(--qy-primary-50);
  color: var(--qy-primary-600);
}

.qy-tag--success {
  background: var(--qy-success-50);
  color: var(--qy-success-600);
}

.qy-tag--warning {
  background: var(--qy-warning-50);
  color: var(--qy-warning-600);
}

.qy-tag--error {
  background: var(--qy-error-50);
  color: var(--qy-error-600);
}

/* 带圆点 */
.qy-tag--dot::before {
  content: '';
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-right: 6px;
}

.qy-tag--success.qy-tag--dot::before {
  background: var(--qy-success-500);
}

.qy-tag--warning.qy-tag--dot::before {
  background: var(--qy-warning-500);
}

.qy-tag--error.qy-tag--dot::before {
  background: var(--qy-error-500);
}
```

---

### 6. 提示 Alert

```html
<div class="qy-alert qy-alert--info">
  <span class="qy-alert__icon">ℹ️</span>
  <span class="qy-alert__content">信息提示内容</span>
  <button class="qy-alert__close" aria-label="关闭">×</button>
</div>

<div class="qy-alert qy-alert--warning qy-alert--banner">
  <span class="qy-alert__content">256人未参保</span>
  <a href="#" class="qy-alert__action">查看详情</a>
  <button class="qy-alert__close" aria-label="关闭">×</button>
</div>
```

```css
.qy-alert {
  display: flex;
  align-items: center;
  gap: var(--qy-space-3);
  padding: var(--qy-space-3) var(--qy-space-4);
  border-radius: var(--qy-radius-md);
  border-left: 3px solid;
}

.qy-alert--info {
  background: var(--qy-primary-50);
  border-left-color: var(--qy-primary-500);
}

.qy-alert--success {
  background: var(--qy-success-50);
  border-left-color: var(--qy-success-500);
}

.qy-alert--warning {
  background: var(--qy-warning-50);
  border-left-color: var(--qy-warning-500);
}

.qy-alert--error {
  background: var(--qy-error-50);
  border-left-color: var(--qy-error-500);
}

.qy-alert--banner {
  border-left: none;
  border: 1px solid;
  border-radius: var(--qy-radius-md);
}

.qy-alert--banner.qy-alert--warning {
  background: var(--qy-warning-50);
  border-color: #FED7AA;
}

.qy-alert__content {
  flex: 1;
  font-size: var(--qy-font-size-sm);
}

.qy-alert__action {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-primary-500);
  text-decoration: none;
}

.qy-alert__action:hover {
  text-decoration: underline;
}

.qy-alert__close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  font-size: 16px;
  color: var(--qy-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  border-radius: var(--qy-radius-sm);
}

.qy-alert__close:hover {
  background: rgba(0,0,0,0.05);
}
```

---

### 7. 表格 Table

```html
<div class="qy-table-container" role="region" aria-label="数据表格" tabindex="0">
  <table class="qy-table">
    <thead>
      <tr>
        <th class="qy-table__checkbox">
          <input type="checkbox" aria-label="全选">
        </th>
        <th>姓名</th>
        <th>部门</th>
        <th>状态</th>
        <th class="qy-table__actions">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="qy-table__checkbox">
          <input type="checkbox" aria-label="选择张三">
        </td>
        <td>张三</td>
        <td>技术部</td>
        <td><span class="qy-tag qy-tag--success">在职</span></td>
        <td class="qy-table__actions">
          <button class="qy-btn-action qy-btn-action--text">编辑</button>
          <button class="qy-btn-action qy-btn-action--text">详情</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.qy-table-container {
  overflow-x: auto;
  border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-lg);
}

.qy-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--qy-font-size-sm);
}

.qy-table thead {
  background: var(--qy-bg-secondary);
}

.qy-table th {
  padding: var(--qy-space-3) var(--qy-space-4);
  font-weight: var(--qy-font-weight-semibold);
  font-size: var(--qy-font-size-xs);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--qy-text-secondary);
  text-align: left;
  white-space: nowrap;
}

.qy-table td {
  padding: var(--qy-space-3) var(--qy-space-4);
  border-bottom: 1px solid var(--qy-border-light);
}

.qy-table tbody tr {
  transition: background var(--qy-transition-fast);
}

.qy-table tbody tr:hover {
  background: var(--qy-bg-secondary);
}

.qy-table tbody tr:last-child td {
  border-bottom: none;
}

/* 复选框列 */
.qy-table__checkbox {
  width: 44px;
  text-align: center;
}

/* 操作列 */
.qy-table__actions {
  width: 120px;
  white-space: nowrap;
}

.qy-table__actions > * + * {
  margin-left: var(--qy-space-2);
}

/* 行选中态 */
.qy-table tbody tr.is-selected {
  background: var(--qy-primary-50);
}

/* 斑马纹（可选） */
.qy-table--striped tbody tr:nth-child(even) {
  background: #FAFBFC;
}

.qy-table--striped tbody tr:nth-child(even):hover {
  background: var(--qy-bg-secondary);
}

/* 行高 */
.qy-table--compact td {
  padding: var(--qy-space-2) var(--qy-space-4);
}

.qy-table--comfortable td {
  padding: var(--qy-space-4);
}
```

---

### 8. 分页 Pagination

```html
<nav class="qy-pagination" aria-label="分页">
  <span class="qy-pagination__total">共 275 条</span>
  <div class="qy-pagination__pages">
    <button class="qy-pagination__btn" disabled aria-label="上一页">‹</button>
    <button class="qy-pagination__btn qy-pagination__btn--active" aria-current="page">1</button>
    <button class="qy-pagination__btn">2</button>
    <button class="qy-pagination__btn">3</button>
    <span class="qy-pagination__ellipsis">...</span>
    <button class="qy-pagination__btn">28</button>
    <button class="qy-pagination__btn" aria-label="下一页">›</button>
  </div>
  <div class="qy-pagination__options">
    <select class="qy-select qy-select--sm" aria-label="每页条数">
      <option>10条/页</option>
      <option selected>20条/页</option>
      <option>50条/页</option>
      <option>100条/页</option>
    </select>
    <span class="qy-pagination__jump">
      跳至 <input type="text" class="qy-input qy-input--sm" style="width: 48px;"> 页
    </span>
  </div>
</nav>
```

```css
.qy-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--qy-space-4) 0;
}

.qy-pagination__total {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
}

.qy-pagination__pages {
  display: flex;
  align-items: center;
  gap: var(--qy-space-1);
}

.qy-pagination__btn {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
  padding: 0 var(--qy-space-2);
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--qy-radius-sm);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
}

.qy-pagination__btn:hover:not(:disabled) {
  background: var(--qy-bg-secondary);
  color: var(--qy-text-primary);
}

.qy-pagination__btn--active {
  background: var(--qy-primary-500) !important;
  color: white !important;
}

.qy-pagination__btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.qy-pagination__ellipsis {
  color: var(--qy-text-muted);
  padding: 0 var(--qy-space-1);
}

.qy-pagination__options {
  display: flex;
  align-items: center;
  gap: var(--qy-space-4);
}

.qy-pagination__jump {
  display: flex;
  align-items: center;
  gap: var(--qy-space-2);
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
}
```

---

### 9. 分段控制器 Segmented Control

```html
<div class="qy-segmented" role="tablist" aria-label="状态筛选">
  <button class="qy-segmented__item is-active" role="tab" aria-selected="true">
    全部 <span class="qy-segmented__badge">202</span>
  </button>
  <button class="qy-segmented__item" role="tab" aria-selected="false">
    已参保 <span class="qy-segmented__badge">1</span>
  </button>
  <button class="qy-segmented__item" role="tab" aria-selected="false">
    未参保 <span class="qy-segmented__badge">256</span>
  </button>
</div>
```

```css
.qy-segmented {
  display: inline-flex;
  padding: 2px;
  background: var(--qy-bg-secondary);
  border-radius: var(--qy-radius-md);
}

.qy-segmented__item {
  display: flex;
  align-items: center;
  gap: var(--qy-space-2);
  height: 32px;
  padding: 0 var(--qy-space-4);
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-secondary);
  background: transparent;
  border: none;
  border-radius: var(--qy-radius-sm);
  cursor: pointer;
  transition: all var(--qy-transition-fast);
  white-space: nowrap;
}

.qy-segmented__item:hover:not(.is-active) {
  color: var(--qy-text-primary);
}

.qy-segmented__item.is-active {
  background: white;
  color: var(--qy-text-primary);
  box-shadow: var(--qy-shadow-sm);
}

.qy-segmented__badge {
  display: inline-flex;
  align-items: center;
  height: 16px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: var(--qy-font-weight-semibold);
  background: var(--qy-bg-tertiary);
  border-radius: var(--qy-radius-full);
}

.qy-segmented__item.is-active .qy-segmented__badge {
  background: var(--qy-primary-100);
  color: var(--qy-primary-600);
}
```

---

### 10. 空状态 Empty State

```html
<div class="qy-empty">
  <div class="qy-empty__icon">
    <svg>...</svg>
  </div>
  <h3 class="qy-empty__title">暂无数据</h3>
  <p class="qy-empty__description">当前列表为空，请点击下方按钮添加</p>
  <button class="qy-btn qy-btn--primary">添加数据</button>
</div>
```

```css
.qy-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--qy-space-12) var(--qy-space-6);
  text-align: center;
}

.qy-empty__icon {
  width: 64px;
  height: 64px;
  margin-bottom: var(--qy-space-4);
  color: var(--qy-text-muted);
}

.qy-empty__icon svg {
  width: 100%;
  height: 100%;
}

.qy-empty__title {
  font-size: var(--qy-font-size-md);
  font-weight: var(--qy-font-weight-semibold);
  color: var(--qy-text-primary);
  margin-bottom: var(--qy-space-2);
}

.qy-empty__description {
  font-size: var(--qy-font-size-sm);
  color: var(--qy-text-secondary);
  margin-bottom: var(--qy-space-5);
  max-width: 400px;
}
```

---

## 页面布局模板

### 标准列表页

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题 - 青阳云HRO</title>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../styles/qingyang-design-system.css">
</head>
<body>
  <!-- Skip Link -->
  <a href="#main-content" class="qy-skip-link">跳转到主要内容</a>

  <div class="qy-layout">
    <!-- 侧边栏 -->
    <aside class="qy-sidebar" role="navigation" aria-label="侧边导航">
      <div class="qy-sidebar__logo">
        <img src="logo.svg" alt="青阳云">
      </div>
      <nav class="qy-sidebar__nav">
        <div class="qy-sidebar__group">
          <div class="qy-sidebar__title">核心人事</div>
          <a href="#" class="qy-sidebar__item is-active" aria-current="page">
            <span class="qy-sidebar__icon">👥</span>
            <span>花名册</span>
          </a>
          <a href="#" class="qy-sidebar__item">
            <span class="qy-sidebar__icon">📄</span>
            <span>合同管理</span>
          </a>
        </div>
      </nav>
    </aside>

    <!-- 主内容区 -->
    <main class="qy-main" id="main-content">
      <!-- 顶部导航 -->
      <header class="qy-header" role="banner">
        <nav class="qy-header__nav" role="tablist" aria-label="顶部导航">
          <button class="qy-header__tab is-active" role="tab" aria-selected="true">核心人事</button>
          <button class="qy-header__tab" role="tab" aria-selected="false">智能薪酬</button>
          <button class="qy-header__tab" role="tab" aria-selected="false">假勤管理</button>
        </nav>
        <div class="qy-header__user">
          <button class="qy-btn qy-btn--text">管理员</button>
        </div>
      </header>

      <!-- 页面内容 -->
      <div class="qy-page">
        <!-- 页面标题 -->
        <div class="qy-page__header">
          <h1 class="qy-page__title">页面标题</h1>
          <button class="qy-btn qy-btn--primary">添加</button>
        </div>

        <!-- KPI统计（可选） -->
        <div class="qy-kpi-section">
          <button class="qy-kpi-card is-active" aria-pressed="true">
            <span class="qy-kpi-card__value">275</span>
            <span class="qy-kpi-card__label">全部</span>
          </button>
          <button class="qy-kpi-card" aria-pressed="false">
            <span class="qy-kpi-card__value">12</span>
            <span class="qy-kpi-card__label">已到期</span>
          </button>
        </div>

        <!-- Warning Banner（可选） -->
        <div class="qy-alert qy-alert--warning qy-alert--banner" role="alert">
          <span class="qy-alert__content">256人未参保</span>
          <a href="#" class="qy-alert__action">查看详情</a>
        </div>

        <!-- 筛选工具栏 -->
        <div class="qy-toolbar">
          <div class="qy-toolbar__left">
            <select class="qy-select" style="width: 140px;" aria-label="结算主体">
              <option>按结算主体</option>
            </select>
            <select class="qy-select" style="width: 180px;" aria-label="公司">
              <option>湖南立人科技有限公司</option>
            </select>
            <input type="text" class="qy-input" style="width: 240px;" placeholder="姓名/工号/身份证">
            <button class="qy-btn qy-btn--primary">搜索</button>
            <button class="qy-btn qy-btn--secondary">高级搜索</button>
          </div>
        </div>

        <!-- 批量操作栏（动态显示） -->
        <div class="qy-bulk-bar" role="toolbar" aria-label="批量操作">
          <span class="qy-bulk-bar__count">已选 5 项</span>
          <button class="qy-btn qy-btn--text">批量操作1</button>
          <button class="qy-btn qy-btn--text">批量操作2</button>
        </div>

        <!-- 数据表格 -->
        <div class="qy-table-container" role="region" aria-label="数据表格" tabindex="0">
          <table class="qy-table">
            <thead>
              <tr>
                <th class="qy-table__checkbox"><input type="checkbox" aria-label="全选"></th>
                <th>姓名</th>
                <th>证件号码</th>
                <th>所属客户</th>
                <th>状态</th>
                <th class="qy-table__actions">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="qy-table__checkbox"><input type="checkbox" aria-label="选择行"></td>
                <td>张三</td>
                <td>430***********1234</td>
                <td>湖南立人科技有限公司</td>
                <td><span class="qy-tag qy-tag--success">在职</span></td>
                <td class="qy-table__actions">
                  <button class="qy-btn-action qy-btn-action--text">编辑</button>
                  <button class="qy-btn-action qy-btn-action--text">详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 分页 -->
        <nav class="qy-pagination" aria-label="分页">
          <span class="qy-pagination__total">共 275 条</span>
          <div class="qy-pagination__pages">
            <button class="qy-pagination__btn" disabled>‹</button>
            <button class="qy-pagination__btn qy-pagination__btn--active" aria-current="page">1</button>
            <button class="qy-pagination__btn">2</button>
            <button class="qy-pagination__btn">3</button>
            <span class="qy-pagination__ellipsis">...</span>
            <button class="qy-pagination__btn">28</button>
            <button class="qy-pagination__btn">›</button>
          </div>
          <div class="qy-pagination__options">
            <select class="qy-select" style="width: 90px;" aria-label="每页条数">
              <option>10条/页</option>
              <option selected>20条/页</option>
              <option>50条/页</option>
            </select>
            <span class="qy-pagination__jump">
              跳至 <input type="text" class="qy-input" style="width: 48px;"> 页
            </span>
          </div>
        </nav>
      </div>
    </main>
  </div>
</body>
</html>
```

---

## CSS布局样式

```css
/* ========== 布局 ========== */
.qy-layout {
  display: flex;
  min-height: 100vh;
}

/* 侧边栏 */
.qy-sidebar {
  width: var(--qy-sidebar-width);
  background: var(--qy-bg-primary);
  border-right: 1px solid var(--qy-border-light);
  flex-shrink: 0;
}

.qy-sidebar__logo {
  display: flex;
  align-items: center;
  height: var(--qy-header-height);
  padding: 0 var(--qy-space-4);
  border-bottom: 1px solid var(--qy-border-light);
}

.qy-sidebar__nav {
  padding: var(--qy-space-4);
}

.qy-sidebar__group {
  margin-bottom: var(--qy-space-6);
}

.qy-sidebar__title {
  padding: 0 var(--qy-space-3);
  margin-bottom: var(--qy-space-2);
  font-size: var(--qy-font-size-xs);
  font-weight: var(--qy-font-weight-semibold);
  color: var(--qy-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.qy-sidebar__item {
  display: flex;
  align-items: center;
  gap: var(--qy-space-3);
  padding: var(--qy-space-2) var(--qy-space-3);
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-secondary);
  text-decoration: none;
  border-radius: var(--qy-radius-md);
  transition: all var(--qy-transition-fast);
}

.qy-sidebar__item:hover {
  background: var(--qy-bg-secondary);
  color: var(--qy-text-primary);
}

.qy-sidebar__item.is-active {
  background: var(--qy-primary-50);
  color: var(--qy-primary-600);
  font-weight: var(--qy-font-weight-semibold);
  border-left: 3px solid var(--qy-primary-500);
  margin-left: -3px;
}

.qy-sidebar__icon {
  width: 16px;
  height: 16px;
}

/* 主内容区 */
.qy-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* 顶部导航 */
.qy-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: var(--qy-header-height);
  padding: 0 var(--qy-space-6);
  background: var(--qy-bg-primary);
  border-bottom: 1px solid var(--qy-border-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.qy-header__nav {
  display: flex;
  gap: var(--qy-space-6);
}

.qy-header__tab {
  position: relative;
  height: var(--qy-header-height);
  padding: 0 var(--qy-space-1);
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-secondary);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color var(--qy-transition-fast);
}

.qy-header__tab:hover {
  color: var(--qy-text-primary);
}

.qy-header__tab.is-active {
  color: var(--qy-primary-600);
  font-weight: var(--qy-font-weight-semibold);
}

.qy-header__tab.is-active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--qy-primary-500);
}

/* 页面内容 */
.qy-page {
  flex: 1;
  padding: var(--qy-space-6);
  overflow-y: auto;
}

.qy-page__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--qy-space-6);
}

.qy-page__title {
  font-size: var(--qy-font-size-2xl);
  font-weight: var(--qy-font-weight-bold);
  color: var(--qy-text-primary);
}

/* KPI区域 */
.qy-kpi-section {
  display: flex;
  gap: var(--qy-space-4);
  margin-bottom: var(--qy-space-6);
  flex-wrap: wrap;
}

/* 工具栏 */
.qy-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--qy-space-4);
  margin-bottom: var(--qy-space-4);
}

.qy-toolbar__left,
.qy-toolbar__right {
  display: flex;
  align-items: center;
  gap: var(--qy-space-3);
  flex-wrap: wrap;
}

/* 批量操作栏 */
.qy-bulk-bar {
  display: flex;
  align-items: center;
  gap: var(--qy-space-4);
  padding: var(--qy-space-3) var(--qy-space-4);
  background: var(--qy-bg-secondary);
  border-radius: var(--qy-radius-md);
  margin-bottom: var(--qy-space-3);
}

.qy-bulk-bar__count {
  font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-primary);
}
```

---

## 设计检查清单

在交付每个页面/组件前，请确认以下检查项：

### 视觉质量
- [ ] 没有使用emoji作为图标
- [ ] 所有图标来自同一图标库，风格一致
- [ ] 按下状态不会引起布局偏移
- [ ] 使用语义化颜色token，没有硬编码色值

### 交互
- [ ] 所有可点击元素有清晰的按下反馈
- [ ] 触摸目标 ≥ 44×44px
- [ ] 微交互时长在 150-300ms 之间
- [ ] 禁用状态视觉清晰且不可交互
- [ ] 焦点顺序与视觉顺序一致

### 可访问性
- [ ] 正文对比度 ≥ 4.5:1
- [ ] 所有交互元素有可见焦点环
- [ ] 所有图片有alt文本
- [ ] 表单字段有关联标签
- [ ] 颜色不是唯一的指示方式
- [ ] 支持减少动画偏好

### B2B SaaS 特定
- [ ] 信息密度适中，适合长时间使用
- [ ] 高频操作路径短
- [ ] 数据表格支持排序、筛选、分页
- [ ] 批量操作清晰可发现
- [ ] 空状态提供明确引导

---

## 附录

### 命名规范

```
前缀: qy- (qingyang)

组件: .qy-{组件名}
  例如: .qy-btn, .qy-input, .qy-card

修饰符: .qy-{组件}--{修饰符}
  例如: .qy-btn--primary, .qy-btn--lg

子元素: .qy-{组件}__{子元素}
  例如: .qy-card__header, .qy-card__body

状态: .is-{状态}
  例如: .is-active, .is-disabled, .is-selected
```

### 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### 性能预算

- 首屏加载 < 2s
- 可交互时间 (TTI) < 3.5s
- 累积布局偏移 (CLS) < 0.1
- 首次输入延迟 (FID) < 100ms

---

*本文档是青阳云HRO系统的官方设计系统，所有原型设计必须遵循此规范。*
