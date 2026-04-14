# 青阳云样式系统

> Qingyang Cloud Design System - CSS/SCSS

## 📁 文件说明

| 文件 | 类型 | 说明 |
|------|------|------|
| `qingyang-variables.css` | CSS | CSS 变量文件，包含完整的设计令牌 |
| `qingyang-variables.scss` | SCSS | SCSS 变量文件，包含函数和混合宏 |
| `qingyang-base.css` | CSS | 基础样式文件，包含 Reset + 工具类 |
| `qingyang-components.css` | CSS | 完整组件库（25+ 组件） |
| `qingyang-forms.css` | CSS | 表单组件库（15+ 表单控件） |
| `example.html` | HTML | 使用示例 |

## 🚀 快速开始

### 1. 仅使用 CSS 变量

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <link rel="stylesheet" href="styles/qingyang-variables.css">
    <link rel="stylesheet" href="styles/qingyang-base.css">
</head>
<body>
    <button class="qy-btn qy-btn--primary">主要按钮</button>
</body>
</html>
```

### 2. 使用 SCSS（推荐）

```scss
// 引入变量文件
@import 'styles/qingyang-variables';

// 使用变量和混合宏
.my-component {
  background: $primary-500;
  padding: space(4);
  border-radius: radius('md');
  
  @include respond-to('desktop') {
    padding: space(6);
  }
  
  @include card-base;
}
```

## 🎨 设计令牌

### 颜色

```css
/* 主色 */
var(--qy-primary-500)    /* #2563EB - 主按钮 */
var(--qy-primary-600)    /* #1D4ED8 - 悬停 */
var(--qy-primary-50)     /* #EFF6FF - 背景 */

/* 语义色 */
var(--qy-success-500)    /* #22C55E */
var(--qy-warning-500)    /* #F97316 */
var(--qy-error-500)      /* #EF4444 */

/* 中性色 */
var(--qy-text-primary)   /* #1E293B */
var(--qy-text-secondary) /* #64748B */
var(--qy-text-muted)     /* #94A3B8 */
```

### 间距

```css
var(--qy-space-1)  /* 4px  */
var(--qy-space-2)  /* 8px  */
var(--qy-space-3)  /* 12px */
var(--qy-space-4)  /* 16px */
var(--qy-space-5)  /* 20px */
var(--qy-space-6)  /* 24px */
```

### 圆角

```css
var(--qy-radius-sm)  /* 4px  */
var(--qy-radius-md)  /* 8px  */
var(--qy-radius-lg)  /* 12px */
var(--qy-radius-xl)  /* 16px */
```

### 阴影

```css
var(--qy-shadow-sm)   /* 小阴影 */
var(--qy-shadow-card) /* 卡片阴影 */
var(--qy-shadow-md)   /* 中等阴影 */
var(--qy-shadow-lg)   /* 大阴影 */
```

## 🧩 组件类名

### 按钮

```html
<!-- 变体 -->
<button class="qy-btn qy-btn--primary">主要</button>
<button class="qy-btn qy-btn--secondary">次要</button>
<button class="qy-btn qy-btn--text">文字</button>
<button class="qy-btn qy-btn--danger">危险</button>

<!-- 尺寸 -->
<button class="qy-btn qy-btn--primary qy-btn--sm">小</button>
<button class="qy-btn qy-btn--primary">中（默认）</button>
<button class="qy-btn qy-btn--primary qy-btn--lg">大</button>
```

### 输入框

```html
<input class="qy-input" placeholder="默认">
<input class="qy-input qy-input--error" placeholder="错误状态">
```

### 卡片

```html
<div class="qy-card">
  <div class="qy-card__header">标题</div>
  <div class="qy-card__body">内容</div>
  <div class="qy-card__footer">底部</div>
</div>
```

### 标签

```html
<span class="qy-tag qy-tag--default">默认</span>
<span class="qy-tag qy-tag--primary">主要</span>
<span class="qy-tag qy-tag--success">成功</span>
<span class="qy-tag qy-tag--warning">警告</span>
<span class="qy-tag qy-tag--error">错误</span>
<span class="qy-badge">9</span>
```

---

## 🧩 完整组件库（25+ 组件）

### 表格 / Table

```html
<div class="qy-table-wrapper">
  <table class="qy-table">
    <thead>
      <tr>
        <th>姓名</th>
        <th>部门</th>
        <th>状态</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>张三</td>
        <td>技术部</td>
        <td><span class="qy-tag qy-tag--success">在职</span></td>
      </tr>
    </tbody>
  </table>
</div>
```

**表格变体：**
- `qy-table--small` - 小尺寸
- `qy-table--large` - 大尺寸
- `qy-table--bordered` - 边框
- `qy-table--striped` - 斑马纹

### 分页 / Pagination

```html
<div class="qy-pagination">
  <span class="qy-pagination__total">共 100 条</span>
  <button class="qy-pagination__prev">←</button>
  <div class="qy-pagination__list">
    <span class="qy-pagination__item">1</span>
    <span class="qy-pagination__item is-active">2</span>
    <span class="qy-pagination__item">3</span>
  </div>
  <button class="qy-pagination__next">→</button>
</div>
```

### 面包屑 / Breadcrumb

```html
<nav class="qy-breadcrumb">
  <span class="qy-breadcrumb__item"><a href="#">首页</a></span>
  <span class="qy-breadcrumb__separator">/</span>
  <span class="qy-breadcrumb__item"><a href="#">员工管理</a></span>
  <span class="qy-breadcrumb__separator">/</span>
  <span class="qy-breadcrumb__item is-active">员工列表</span>
</nav>
```

### 下拉菜单 / Dropdown

```html
<div class="qy-dropdown is-open">
  <button class="qy-dropdown__trigger qy-btn qy-btn--secondary">
    操作 ▼
  </button>
  <div class="qy-dropdown__menu">
    <div class="qy-dropdown__item">编辑</div>
    <div class="qy-dropdown__item">删除</div>
    <div class="qy-dropdown__divider"></div>
    <div class="qy-dropdown__item is-disabled">禁用项</div>
  </div>
</div>
```

### 模态框 / Modal

```html
<div class="qy-modal is-open">
  <div class="qy-modal__overlay"></div>
  <div class="qy-modal__container">
    <div class="qy-modal__header">
      <span class="qy-modal__title">对话框标题</span>
      <span class="qy-modal__close">×</span>
    </div>
    <div class="qy-modal__body">内容区域</div>
    <div class="qy-modal__footer">
      <button class="qy-btn qy-btn--secondary">取消</button>
      <button class="qy-btn qy-btn--primary">确定</button>
    </div>
  </div>
</div>
```

**尺寸：** `qy-modal__container--small/large/xlarge/full`

### 抽屉 / Drawer

```html
<div class="qy-drawer qy-drawer--right is-open">
  <div class="qy-drawer__overlay"></div>
  <div class="qy-drawer__container">
    <div class="qy-drawer__header">
      <span class="qy-drawer__title">抽屉标题</span>
      <span class="qy-drawer__close">×</span>
    </div>
    <div class="qy-drawer__body">
      <div class="qy-drawer__section">
        <div class="qy-drawer__section-title">分段标题</div>
        <!-- 表单内容 -->
      </div>
    </div>
    <div class="qy-drawer__footer">
      <button class="qy-btn qy-btn--secondary">取 消</button>
      <button class="qy-btn qy-btn--primary">确 认</button>
    </div>
  </div>
</div>
```

**位置：** `qy-drawer--left/right/top/bottom`
**宽度：** 右侧/左侧抽屉默认宽度 520px

### 消息提示 / Message

```html
<div class="qy-message-container">
  <div class="qy-message">
    <span class="qy-message__icon qy-message__icon--success">✓</span>
    <span class="qy-message__content">操作成功</span>
    <span class="qy-message__close">×</span>
  </div>
</div>
```

**类型：** `qy-message__icon--success/warning/error/info`

### 加载状态 / Loading

```html
<!-- 加载动画 -->
<div class="qy-loading">
  <div class="qy-loading__spinner"></div>
  <span class="qy-loading__text">加载中...</span>
</div>

<!-- 骨架屏 -->
<div class="qy-skeleton">
  <div class="qy-skeleton__item qy-skeleton__item--title"></div>
  <div class="qy-skeleton__item qy-skeleton__item--text"></div>
  <div class="qy-skeleton__item qy-skeleton__item--text"></div>
</div>
```

### 空状态 / Empty

```html
<div class="qy-empty">
  <div class="qy-empty__icon">📭</div>
  <div class="qy-empty__title">暂无数据</div>
  <div class="qy-empty__description">当前列表为空，请添加数据</div>
  <div class="qy-empty__action">
    <button class="qy-btn qy-btn--primary">立即添加</button>
  </div>
</div>
```

### 步骤条 / Steps

```html
<div class="qy-steps qy-steps--horizontal">
  <div class="qy-step is-finish">
    <div class="qy-step__head">
      <div class="qy-step__icon">1</div>
      <div class="qy-step__line"></div>
    </div>
    <div class="qy-step__main">
      <div class="qy-step__title">填写信息</div>
    </div>
  </div>
  <div class="qy-step is-process">
    <div class="qy-step__head">
      <div class="qy-step__icon">2</div>
    </div>
    <div class="qy-step__main">
      <div class="qy-step__title">确认提交</div>
    </div>
  </div>
</div>
```

**方向：** `qy-steps--horizontal/vertical`
**状态：** `is-finish/is-process/is-error`

### 树形控件 / Tree

```html
<div class="qy-tree">
  <div class="qy-tree__node is-expanded">
    <div class="qy-tree__node-content">
      <span class="qy-tree__node-expand">▶</span>
      <span class="qy-tree__node-label">总公司</span>
    </div>
    <div class="qy-tree__children">
      <div class="qy-tree__node is-leaf">
        <div class="qy-tree__node-content">
          <span class="qy-tree__node-expand"></span>
          <span class="qy-tree__node-label">技术部</span>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 时间轴 / Timeline

```html
<div class="qy-timeline">
  <div class="qy-timeline__item">
    <div class="qy-timeline__dot qy-timeline__dot--success"></div>
    <div class="qy-timeline__content">
      <div class="qy-timeline__title">入职</div>
      <div class="qy-timeline__description">张三加入公司</div>
      <div class="qy-timeline__time">2024-01-15</div>
    </div>
  </div>
</div>
```

**点类型：** `qy-timeline__dot--success/warning/error`

### 统计卡片 / Stat Card

```html
<div class="qy-stat-card">
  <div class="qy-stat-card__header">
    <span class="qy-stat-card__title">在职员工</span>
    <div class="qy-stat-card__icon qy-stat-card__icon--primary">👥</div>
  </div>
  <div class="qy-stat-card__value">256</div>
  <div class="qy-stat-card__footer">
    <span class="qy-stat-card__trend qy-stat-card__trend--up">↑ 12%</span>
    <span class="qy-stat-card__label">较上月</span>
  </div>
</div>
```

### 开关 / Switch

```html
<label class="qy-switch">
  <input type="checkbox" class="qy-switch__input" checked>
  <span class="qy-switch__slider"></span>
</label>

<!-- 小尺寸 -->
<label class="qy-switch qy-switch--small">
  <input type="checkbox" class="qy-switch__input">
  <span class="qy-switch__slider"></span>
</label>
```

### 单选/复选框 / Radio & Checkbox

```html
<label class="qy-radio">
  <input type="radio" class="qy-radio__input" name="option">
  <span class="qy-radio__icon"></span>
  <span class="qy-radio__label">选项一</span>
</label>

<label class="qy-checkbox">
  <input type="checkbox" class="qy-checkbox__input" checked>
  <span class="qy-checkbox__icon"></span>
  <span class="qy-checkbox__label">勾选框</span>
</label>
```

### 工具提示 / Tooltip

```html
<span class="qy-tooltip">
  悬停查看
  <span class="qy-tooltip__content qy-tooltip__content--top">提示内容</span>
</span>
```

**位置：** `qy-tooltip__content--top/bottom/left/right`

### 头像 / Avatar

```html
<div class="qy-avatar qy-avatar--medium">张</div>

<!-- 带图片 -->
<div class="qy-avatar qy-avatar--large">
  <img src="avatar.jpg" alt="头像">
</div>

<!-- 头像组 -->
<div class="qy-avatar-group">
  <div class="qy-avatar qy-avatar--small">A</div>
  <div class="qy-avatar qy-avatar--small">B</div>
  <div class="qy-avatar qy-avatar--small">C</div>
</div>
```

**尺寸：** `qy-avatar--small/medium/large/xlarge`

### 进度条 / Progress

```html
<!-- 线性进度条 -->
<div class="qy-progress">
  <div class="qy-progress__bar" style="width: 60%"></div>
</div>

<!-- 带文字 -->
<div class="qy-flex qy-items-center">
  <div class="qy-progress qy-progress--success">
    <div class="qy-progress__bar" style="width: 80%"></div>
  </div>
  <span class="qy-progress__text">80%</span>
</div>

<!-- 圆形进度条 -->
<div class="qy-progress-circle">
  <svg class="qy-progress-circle__svg" width="80" height="80">
    <circle class="qy-progress-circle__track" cx="40" cy="40" r="36"></circle>
    <circle class="qy-progress-circle__path" cx="40" cy="40" r="36"
            stroke-dasharray="226" stroke-dashoffset="90"></circle>
  </svg>
  <span class="qy-progress-circle__text">60%</span>
</div>
```

**类型：** `qy-progress--success/warning/error`

### 标签页 / Tabs

```html
<div class="qy-tabs">
  <div class="qy-tabs__nav">
    <div class="qy-tabs__item is-active">基本信息</div>
    <div class="qy-tabs__item">工作经历</div>
    <div class="qy-tabs__item">教育背景</div>
  </div>
  <div class="qy-tabs__content">
    <div class="qy-tabs__pane is-active">内容一</div>
    <div class="qy-tabs__pane">内容二</div>
  </div>
</div>

<!-- 卡片式 -->
<div class="qy-tabs qy-tabs--card">...</div>
```

### 结果页 / Result

```html
<div class="qy-result">
  <div class="qy-result__icon qy-result__icon--success">✓</div>
  <div class="qy-result__title">提交成功</div>
  <div class="qy-result__subtitle">您的申请已提交，我们会在3个工作日内处理</div>
  <div class="qy-result__extra">
    <button class="qy-btn qy-btn--primary">返回首页</button>
    <button class="qy-btn qy-btn--secondary">查看详情</button>
  </div>
</div>
```

**类型：** `qy-result__icon--success/error/warning/info/404`

### 导航菜单 / Menu

```html
<div class="qy-menu">
  <div class="qy-menu__item is-active">
    <span class="qy-menu__icon">🏠</span>
    <span>工作台</span>
  </div>
  <div class="qy-menu__item">
    <span class="qy-menu__icon">👥</span>
    <span>员工管理</span>
  </div>
  <div class="qy-menu__divider"></div>
  <div class="qy-menu__item is-disabled">
    <span class="qy-menu__icon">⚙️</span>
    <span>系统设置</span>
  </div>
</div>
```

### 描述列表 / Descriptions

```html
<div class="qy-descriptions">
  <div class="qy-descriptions__title">员工信息</div>
  <div class="qy-descriptions__list">
    <div class="qy-descriptions__item">
      <span class="qy-descriptions__label">姓名</span>
      <span class="qy-descriptions__value">张三</span>
    </div>
    <div class="qy-descriptions__item">
      <span class="qy-descriptions__label">部门</span>
      <span class="qy-descriptions__value">技术部</span>
    </div>
  </div>
</div>
```

### 回到顶部 / BackTop

```html
<div class="qy-backtop is-visible">
  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
    <path fill-rule="evenodd" d="M3.293 9.707a1 1 0 010-1.414l6-6a1 1 0 011.414 0l6 6a1 1 0 01-1.414 1.414L11 5.414V17a1 1 0 11-2 0V5.414L4.707 9.707a1 1 0 01-1.414 0z" clip-rule="evenodd"/>
  </svg>
</div>
```

## 🛠️ 工具类

### 间距

```html
<div class="qy-m-4">margin: 16px</div>
<div class="qy-mt-2">margin-top: 8px</div>
<div class="qy-p-4">padding: 16px</div>
<div class="qy-px-3">padding-left/right: 12px</div>
```

### Flex 布局

```html
<div class="qy-flex">Flex 容器</div>
<div class="qy-flex-center">水平垂直居中</div>
<div class="qy-flex-between">两端对齐</div>
```

### 文字

```html
<p class="qy-text-primary">主要文字</p>
<p class="qy-text-secondary">次要文字</p>
<p class="qy-text-muted">弱化文字</p>
<p class="qy-truncate">单行截断...</p>
```

### 显示/隐藏

```html
<div class="qy-hidden-mobile">移动端隐藏</div>
<div class="qy-show-mobile">移动端显示</div>
```

## 🌙 深色模式

通过 `data-theme="dark"` 或 `.qy-theme-dark` 类启用：

```html
<html data-theme="dark">
  <!-- 深色模式内容 -->
</html>
```

或在特定元素上：

```html
<div class="qy-theme-dark">
  <!-- 深色模式内容 -->
</div>
```

## ♿ 可访问性

- 所有组件支持键盘导航
- 焦点状态清晰可见
- 支持 `prefers-reduced-motion` 减少动效
- 支持 `prefers-contrast: high` 高对比度模式

## 📱 响应式断点

| 名称 | 宽度 | SCSS |
|------|------|------|
| Mobile | < 768px | `@include respond-to-max('mobile')` |
| Tablet | ≥ 768px | `@include respond-to('tablet')` |
| Desktop | ≥ 1024px | `@include respond-to('desktop')` |
| Wide | ≥ 1440px | `@include respond-to('wide')` |

## 📝 SCSS 混合宏

### 响应式

```scss
.my-class {
  font-size: 14px;
  
  @include respond-to('desktop') {
    font-size: 16px;
  }
}
```

### 文本截断

```scss
.title {
  @include text-truncate;        // 单行
}

.description {
  @include text-truncate-lines(3); // 多行
}
```

### 自定义滚动条

```scss
.scrollable {
  @include custom-scrollbar(8px, transparent, #ccc, #999);
}
```

### 玻璃拟态

```scss
.glass-card {
  @include glass-effect(0.8, 10px);
}
```

## 🔧 自定义配置

### 修改变量

在引入样式文件前定义变量：

```scss
// 自定义主色
$primary-500: #3B82F6;

@import 'styles/qingyang-variables';
```

### 添加新变量

```scss
@import 'styles/qingyang-variables';

// 新增业务变量
$brand-color: #FF6B00;
$sidebar-width-expanded: 280px;
```

---

## 📝 表单组件库

表单组件需要额外引入 `qingyang-forms.css`：

```html
<link rel="stylesheet" href="styles/qingyang-forms.css">
```

### 文本域 / Textarea

```html
<textarea class="qy-textarea" placeholder="请输入内容"></textarea>

<!-- 带字数限制 -->
<div class="qy-textarea-wrapper">
    <textarea class="qy-textarea" maxlength="200"></textarea>
    <span class="qy-textarea__count">0/200</span>
</div>
```

### 下拉选择 / Select

```html
<div class="qy-select">
    <div class="qy-select__trigger">
        <span class="qy-select__placeholder">请选择</span>
        <span class="qy-select__arrow">▼</span>
    </div>
    <div class="qy-select__dropdown">
        <div class="qy-select__option is-selected">选项一</div>
        <div class="qy-select__option">选项二</div>
        <div class="qy-select__option">选项三</div>
    </div>
</div>
```

**变体：**
- `qy-select--small/large` - 尺寸
- `qy-select--multiple` - 多选
- `qy-select--searchable` - 可搜索

### 日期选择 / DatePicker

```html
<div class="qy-datepicker">
    <div class="qy-datepicker__input">
        <span>2024-01-15</span>
        <span class="qy-datepicker__icon">📅</span>
    </div>
</div>

<!-- 范围选择 -->
<div class="qy-datepicker qy-datepicker--range">
    <div class="qy-datepicker__input">
        <span>2024-01-01 至 2024-01-31</span>
    </div>
</div>
```

### 文件上传 / Upload

```html
<!-- 点击上传 -->
<div class="qy-upload">
    <input type="file" class="qy-upload__input" id="file">
    <label for="file" class="qy-btn qy-btn--primary">选择文件</label>
</div>

<!-- 拖拽上传 -->
<div class="qy-upload__drag">
    <div class="qy-upload__drag-icon">📁</div>
    <div class="qy-upload__drag-text">点击或拖拽文件到此区域上传</div>
    <div class="qy-upload__drag-hint">支持单个或批量上传</div>
</div>
```

### 数字输入 / InputNumber

```html
<div class="qy-input-number">
    <span class="qy-input-number__decrease">-</span>
    <input type="number" class="qy-input-number__input" value="1">
    <span class="qy-input-number__increase">+</span>
</div>

<!-- 尺寸变体 -->
<div class="qy-input-number qy-input-number--small">...</div>
<div class="qy-input-number qy-input-number--large">...</div>
```

### 搜索框 / Search

```html
<div class="qy-input-search">
    <span class="qy-input-search__icon">🔍</span>
    <input type="text" class="qy-input" placeholder="请输入搜索内容">
    <span class="qy-input-search__clear">✕</span>
</div>
```

### 滑块 / Slider

```html
<div class="qy-slider">
    <div class="qy-slider__runway">
        <div class="qy-slider__bar" style="width: 50%"></div>
        <div class="qy-slider__button" style="left: 50%"></div>
    </div>
</div>

<!-- 带输入框 -->
<div class="qy-slider">
    <div class="qy-slider__runway">...</div>
    <input type="number" class="qy-input qy-slider__input" value="50">
</div>
```

### 评分 / Rate

```html
<div class="qy-rate">
    <span class="qy-rate__item is-active">★</span>
    <span class="qy-rate__item is-active">★</span>
    <span class="qy-rate__item is-active">★</span>
    <span class="qy-rate__item">★</span>
    <span class="qy-rate__item">★</span>
    <span class="qy-rate__text">3分</span>
</div>
```

### 开关 / Switch

```html
<label class="qy-switch">
    <input type="checkbox" class="qy-switch__input" checked>
    <span class="qy-switch__slider"></span>
</label>

<!-- 小尺寸 -->
<label class="qy-switch qy-switch--small">
    <input type="checkbox" class="qy-switch__input">
    <span class="qy-switch__slider"></span>
</label>
```

### 单选框 / Radio

```html
<label class="qy-radio">
    <input type="radio" class="qy-radio__input" name="radio" checked>
    <span class="qy-radio__icon"></span>
    <span class="qy-radio__label">选项一</span>
</label>

<label class="qy-radio">
    <input type="radio" class="qy-radio__input" name="radio">
    <span class="qy-radio__icon"></span>
    <span class="qy-radio__label">选项二</span>
</label>
```

### 复选框 / Checkbox

```html
<label class="qy-checkbox">
    <input type="checkbox" class="qy-checkbox__input" checked>
    <span class="qy-checkbox__icon"></span>
    <span class="qy-checkbox__label">勾选框</span>
</label>
```

### 表单布局 / Form

```html
<!-- 垂直布局（默认） -->
<div class="qy-form">
    <div class="qy-form-item">
        <label class="qy-form-item__label is-required">用户名</label>
        <div class="qy-form-item__content">
            <input class="qy-input" placeholder="请输入用户名">
            <div class="qy-form-item__error">用户名不能为空</div>
        </div>
    </div>
</div>

<!-- 水平布局 -->
<div class="qy-form qy-form--horizontal">
    <div class="qy-form-item">
        <label class="qy-form-item__label">用户名</label>
        <div class="qy-form-item__content">
            <input class="qy-input">
        </div>
    </div>
</div>

<!-- 行内布局 -->
<div class="qy-form qy-form--inline">
    <div class="qy-form-item">
        <label class="qy-form-item__label">用户名</label>
        <input class="qy-input">
    </div>
    <div class="qy-form-item">
        <label class="qy-form-item__label">邮箱</label>
        <input class="qy-input">
    </div>
    <button class="qy-btn qy-btn--primary">查询</button>
</div>
```

### 输入框组 / Input Group

```html
<div class="qy-input-group">
    <span class="qy-input-group__addon qy-input-group__addon--prepend">https://</span>
    <input class="qy-input" placeholder="请输入网址">
    <span class="qy-input-group__addon qy-input-group__addon--append">.com</span>
</div>

<!-- 带按钮 -->
<div class="qy-input-group">
    <input class="qy-input" placeholder="请输入内容">
    <button class="qy-btn qy-btn--primary">搜索</button>
</div>
```

### 自动完成 / Autocomplete

```html
<div class="qy-autocomplete">
    <input class="qy-input" placeholder="请输入">
    <div class="qy-autocomplete__suggestions">
        <div class="qy-autocomplete__item">
            <span class="qy-autocomplete__item-highlight">Key</span>word
        </div>
        <div class="qy-autocomplete__item">Keychain</div>
        <div class="qy-autocomplete__item">Keyboard</div>
    </div>
</div>
```

### 穿梭框 / Transfer

```html
<div class="qy-transfer">
    <div class="qy-transfer__panel">
        <div class="qy-transfer__header">
            <span class="qy-transfer__title">源列表</span>
            <span class="qy-transfer__count">3/10</span>
        </div>
        <div class="qy-transfer__list">
            <div class="qy-transfer__item">选项一</div>
            <div class="qy-transfer__item">选项二</div>
        </div>
    </div>
    <div class="qy-transfer__buttons">
        <button class="qy-transfer__button">→</button>
        <button class="qy-transfer__button">←</button>
    </div>
    <div class="qy-transfer__panel">
        <div class="qy-transfer__header">
            <span class="qy-transfer__title">目标列表</span>
        </div>
        <div class="qy-transfer__list">
            <div class="qy-transfer__item is-selected">选项三</div>
        </div>
    </div>
</div>
```

### 级联选择 / Cascader

```html
<div class="qy-cascader">
    <div class="qy-cascader__trigger">
        <span>请选择</span>
        <span>▼</span>
    </div>
    <div class="qy-cascader__panel">
        <div class="qy-cascader__menu">
            <div class="qy-cascader__item is-selected">
                湖南省 <span class="qy-cascader__item-arrow">▶</span>
            </div>
        </div>
        <div class="qy-cascader__menu">
            <div class="qy-cascader__item">长沙市</div>
            <div class="qy-cascader__item">株洲市</div>
        </div>
    </div>
</div>
```

### 颜色选择器 / ColorPicker

```html
<div class="qy-color-picker">
    <div class="qy-color-picker__trigger">
        <span class="qy-color-picker__color" style="background: #2563EB"></span>
        <span class="qy-color-picker__value">#2563EB</span>
    </div>
</div>
```

## 📚 更多资源

- [设计规范文档](../qingyang-ui-ux-guidelines.md)
- [Inter 字体](https://fonts.google.com/specimen/Inter)
- [Lucide 图标](https://lucide.dev/)