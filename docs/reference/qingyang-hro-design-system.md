---
title: 青阳云 HRO 设计系统
module: design-system
type: reference
status: active
owner: athur
updated: 2026-05-16
source_of_truth: true
---

# 青阳云HRO设计系统 v2.1

> **类型**: B2B SaaS / 企业级人力资源管理系统
> **风格**: Professional / Clean / Efficient
> **版本**: v2.1（布局方案修正 + 模块目录结构）
> **日期**: 2026-05-09
>
> **更新说明**: v2.0 合并了原 `qingyang-ui-ux-guidelines.md` 和 `qingyang-hro-design-system.md`，统一 `--qy-` 前缀，字号 14px，字体 Plus Jakarta Sans。v2.1 将布局方案从 margin-left 偏移修正为 flex 布局，原型按 7 业务模块分目录，CSS 引用路径调整为 `../../styles/`。

---

## 目录

1. [设计原则](#1-设计原则)
2. [色彩系统](#2-色彩系统)
3. [字体系统](#3-字体系统)
4. [间距系统](#4-间距系统)
5. [圆角系统](#5-圆角系统)
6. [阴影系统](#6-阴影系统)
7. [动效规范](#7-动效规范)
8. [图标规范](#8-图标规范)
9. [布局规范](#9-布局规范)
10. [可访问性](#10-可访问性)
11. [组件库](#11-组件库)
12. [表单规范](#12-表单规范)
13. [数据可视化](#13-数据可视化)
14. [登录页面](#14-登录页面)
15. [页面模板](#15-页面模板)
16. [最佳实践](#16-最佳实践)
17. [设计检查清单](#17-设计检查清单)
18. [附录](#18-附录)

---

## 1. 设计原则

### 1.1 设计理念
- **专业可信**：Enterprise SaaS 风格，传递专业、可靠的企业级服务形象
- **简洁高效**：信息密度适中，减少视觉噪音，提升操作效率
- **一致性**：统一的设计语言，降低用户学习成本
- **可访问性**：符合 WCAG 2.1 AA 标准，确保所有用户可用

### 1.2 设计关键词
专业 · 清晰 · 高效 · 可信 · 现代

---

## 2. 色彩系统

### 2.1 主色调

| 角色 | Token | 色值 | 用途 |
|------|-------|------|------|
| Primary-50 | `--qy-primary-50` | `#EFF6FF` | 选中背景、hover 背景 |
| Primary-100 | `--qy-primary-100` | `#DBEAFE` | 轻量背景、焦点环 |
| Primary-200 | `--qy-primary-200` | `#BFDBFE` | 边框、装饰 |
| Primary-300 | `--qy-primary-300` | `#93C5FD` | — |
| Primary-400 | `--qy-primary-400` | `#60A5FA` | 次要强调、焦点边框 |
| Primary-500 | `--qy-primary-500` | `#2563EB` | 主按钮、链接、强调色 |
| Primary-600 | `--qy-primary-600` | `#1D4ED8` | 悬停、激活状态 |
| Primary-700 | `--qy-primary-700` | `#1E40AF` | 按钮按下状态 |

### 2.2 语义色

| 角色 | Token | 色值 | 用途 |
|------|-------|------|------|
| Success-50 | `--qy-success-50` | `#F0FDF4` | 成功背景 |
| Success-500 | `--qy-success-500` | `#22C55E` | 成功状态、正向趋势 |
| Success-600 | `--qy-success-600` | `#16A34A` | 成功悬停 |
| Warning-50 | `--qy-warning-50` | `#FFF7ED` | 警告背景 |
| Warning-500 | `--qy-warning-500` | `#F97316` | 警告、提醒、橙色标签 |
| Warning-600 | `--qy-warning-600` | `#EA580C` | 推荐用于警告文字 |
| Error-50 | `--qy-error-50` | `#FEF2F2` | 错误背景 |
| Error-500 | `--qy-error-500` | `#EF4444` | 错误、删除 |
| Error-600 | `--qy-error-600` | `#DC2626` | 错误悬停 |

### 2.3 中性色

| 角色 | Token | 色值 | 对比度 | 用途 |
|------|-------|------|--------|------|
| BG-Primary | `--qy-bg-primary` | `#FFFFFF` | — | 卡片、弹窗背景 |
| BG-Secondary | `--qy-bg-secondary` | `#F8FAFC` | — | 页面背景 |
| BG-Tertiary | `--qy-bg-tertiary` | `#F1F5F9` | — | 输入框背景、禁用 |
| Text-Primary | `--qy-text-primary` | `#1E293B` | 11.5:1 | 标题、正文 |
| Text-Secondary | `--qy-text-secondary` | `#64748B` | 5.7:1 | 说明、标签 |
| Text-Muted | `--qy-text-muted` | `#94A3B8` | 3.3:1 | 占位符（仅用于占位符）|
| Text-Disabled | `--qy-text-disabled` | `#CBD5E1` | — | 禁用文字 |
| Border-Light | `--qy-border-light` | `#E2E8F0` | — | 浅色边框 |
| Border-Medium | `--qy-border-medium` | `#CBD5E1` | — | 输入框边框 |
| Border-Focus | `--qy-border-focus` | `#60A5FA` | — | 输入框 hover 边框 |

### 2.4 CSS 变量

```css
:root {
  /* 主色 */
  --qy-primary-50:  #EFF6FF;
  --qy-primary-100: #DBEAFE;
  --qy-primary-200: #BFDBFE;
  --qy-primary-300: #93C5FD;
  --qy-primary-400: #60A5FA;
  --qy-primary-500: #2563EB;
  --qy-primary-600: #1D4ED8;
  --qy-primary-700: #1E40AF;

  /* 语义色 */
  --qy-success-50:  #F0FDF4;  --qy-success-500: #22C55E;  --qy-success-600: #16A34A;
  --qy-warning-50:  #FFF7ED;  --qy-warning-500: #F97316;  --qy-warning-600: #EA580C;
  --qy-error-50:    #FEF2F2;  --qy-error-500:   #EF4444;  --qy-error-600:   #DC2626;

  /* 中性色 */
  --qy-bg-primary:   #ffffff;
  --qy-bg-secondary: #F8FAFC;
  --qy-bg-tertiary:  #F1F5F9;
  --qy-text-primary:   #1E293B;
  --qy-text-secondary: #64748B;
  --qy-text-muted:     #94A3B8;
  --qy-text-disabled:  #CBD5E1;
  --qy-border-light:   #E2E8F0;
  --qy-border-medium:  #CBD5E1;
  --qy-border-focus:   #60A5FA;
}
```

---

## 3. 字体系统

### 3.1 字体选择

**主字体**：`Plus Jakarta Sans, Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

- Plus Jakarta Sans 为首选，Inter 为回退
- 现代无衬线字体，专为屏幕阅读优化
- 支持多种字重（300-700）
- 优秀的数字显示效果

### 3.2 字号规范

| 级别 | Token | 大小 | 行高 | 字重 | 用途 |
|------|-------|------|------|------|------|
| XS | `--qy-font-size-xs` | 11px | 1.4 | 500 | 标签、徽章、时间戳 |
| SM | `--qy-font-size-sm` | 12px | 1.5 | 400 | 次要文本、帮助文字、错误提示 |
| Base | `--qy-font-size-base` | 14px | 1.6 | 400 | 正文文本 |
| MD | `--qy-font-size-md` | 14px | 1.5 | 500 | 表单标签 |
| LG | `--qy-font-size-lg` | 16px | 1.4 | 600 | 卡片标题 |
| XL | `--qy-font-size-xl` | 20px | 1.3 | 700 | 区块标题 |
| 2XL | `--qy-font-size-2xl` | 24px | 1.3 | 700 | 页面大标题、登录标题 |

### 3.3 字重变量

```css
--qy-font-weight-normal:     400;
--qy-font-weight-medium:     500;
--qy-font-weight-semibold:   600;
--qy-font-weight-bold:       700;
```

### 3.4 行高变量

```css
--qy-line-height-tight:   1.3;   /* 标题 */
--qy-line-height-normal:  1.5;   /* 正文 */
--qy-line-height-relaxed: 1.6;   /* 正文宽松 */
```

### 3.5 特殊文字

| 用途 | 大小 | 字重 | 颜色 |
|------|------|------|------|
| KPI 大数字 | 40px | 700 | text-primary |
| KPI 中数字 | 28px | 700 | text-primary |
| 表格数值 | 12px | 600 | tabular-nums |
| 导航链接 | 13px | 500 | text-secondary |
| 导航链接激活 | 13px | 600 | primary-600 |
| 导航分组标题 | 11px | 600 | text-muted, uppercase |

---

## 4. 间距系统

### 4.1 基础间距（4px 网格）

| Token | 值 | 用途 |
|-------|-----|------|
| `--qy-space-1` | 4px | 图标与文字间距 |
| `--qy-space-2` | 8px | 小间距、紧凑布局 |
| `--qy-space-3` | 12px | 按钮内边距（垂直）、表格单元格 |
| `--qy-space-4` | 16px | 标准间距、卡片内边距、表单间距 |
| `--qy-space-5` | 20px | 大间距、容器内边距 |
| `--qy-space-6` | 24px | 页面内容区边距、区块间距 |
| `--qy-space-8` | 32px | 大区块间距 |
| `--qy-space-10` | 40px | 页面级间距 |
| `--qy-space-12` | 48px | 空状态内边距 |

### 4.2 布局间距

```
页面边距：20px（左右），24px（上下）
侧边栏宽度：220px（CSS 变量 --qy-sidebar-width）
顶部导航高度：52px（CSS 变量 --qy-header-height）
卡片内边距：16px - 20px
表单元素间距：16px
布局方案：flex 横向排列，.qy-main { flex: 1; margin-left: 0 }，不使用 margin-left 偏移
```

---

## 5. 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| `--qy-radius-sm` | 4px | 小按钮、输入框、标签 |
| `--qy-radius-md` | 8px | 按钮、卡片、下拉菜单 |
| `--qy-radius-lg` | 12px | 大卡片、面板、表格容器 |
| `--qy-radius-xl` | 16px | 弹窗、模态框 |
| `--qy-radius-full` | 9999px | 圆形元素（头像、徽章、操作按钮）|

---

## 6. 阴影系统

```css
--qy-shadow-sm:   0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02);
--qy-shadow-md:   0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
--qy-shadow-card: 0 2px 8px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.03);
--qy-shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);
```

| Token | 用途 |
|-------|------|
| shadow-sm | 下拉菜单、小卡片 |
| shadow-card | 标准卡片 |
| shadow-md | 悬停状态、浮动元素 |
| shadow-lg | 弹窗、模态框、抽屉 |

---

## 7. 动效规范

### 7.1 过渡时间

```css
--qy-transition-fast:   150ms ease;
--qy-transition-normal: 200ms ease;
--qy-transition-slow:   300ms ease;
```

### 7.2 常用动效

| 场景 | 时长 | 缓动函数 |
|------|------|----------|
| 按钮悬停 | 150ms | ease |
| 卡片悬停 | 200ms | ease |
| 下拉展开 | 200ms | ease-out |
| 模态框出现 | 300ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Toast 出现/消失 | 300ms | ease-out |
| 页面切换 | 200ms | ease-in-out |

### 7.3 动效原则
- 微交互使用 150-200ms
- 页面级过渡使用 200-300ms
- 使用 `transform` 和 `opacity`（避免触发重排）
- 支持 `prefers-reduced-motion` 媒体查询

---

## 8. 图标规范

### 8.1 图标系统
- **图标库**：Lucide / Heroicons
- **风格**：线性描边，圆角端点
- **默认尺寸**：16px (小) / 20px (中) / 24px (大)
- **描边宽度**：1.5px - 2px

### 8.2 使用规则
- 导航图标：16px，与文字颜色一致
- 按钮图标：14px-16px，与文字颜色一致
- 空状态图标：48px-64px，text-muted 颜色
- **不允许使用 Emoji 作为功能图标**

---

## 9. 布局规范

### 9.1 页面结构

```
┌─────────────────────────────────────┐
│  Sidebar (220px)  │  Top Header      │
│                   │  (52px, sticky)  │
│  Logo             ├──────────────────┤
│  Navigation       │                  │
│                   │  Page Content    │
│  Group Title      │  (padding: 24px  │
│  ├─ Nav Item      │   28px)          │
│  ├─ Nav Item      │                  │
│  └─ Nav Item      │  [Content]       │
│                   │                  │
│  Group Title      │                  │
│  ├─ Nav Item      │                  │
│  └─ Nav Item      │                  │
│                   │                  │
│  User Profile     │                  │
└───────────────────┴──────────────────┘
```

### 9.2 响应式断点

| 断点 | 宽度 | 布局调整 |
|------|------|----------|
| Mobile | < 768px | 侧边栏收起为抽屉，单列布局 |
| Tablet | 768px - 1024px | 侧边栏可折叠，双列布局 |
| Desktop | 1024px - 1440px | 固定侧边栏，多列布局 |
| Large | > 1440px | 最大宽度 1440px，居中 |

### 9.3 内容区域
- **默认最大宽度**：无限制（适应屏幕）
- **推荐内容宽度**：1200px - 1440px
- **阅读区域宽度**：不超过 75ch（约 600px）

---

## 10. 可访问性

### 10.1 对比度要求
- 正文文本：≥ 4.5:1（AA 级）
- 大文本（18px+ 或 14px+ bold）：≥ 3:1
- 交互元素：≥ 3:1

### 10.2 焦点状态
- 所有可交互元素必须有可见焦点指示器
- 焦点环：`0 0 0 3px var(--qy-primary-100)`，2px 偏移
- 键盘导航顺序与视觉顺序一致

### 10.3 触摸目标
- 最小触摸区域：44×44px
- 相邻触摸目标间距：≥ 8px

### 10.4 动画
- 支持 `prefers-reduced-motion`
- 关键动画时长 < 5 秒
- 无闪烁内容（< 3Hz）

---

## 11. 组件库

### 11.0 Canonical CSS 入口

**推荐入口（新页面优先使用拆分版）：**

```html
<link rel="stylesheet" href="../../styles/qingyang-variables.css">
<link rel="stylesheet" href="../../styles/qingyang-base.css">
<link rel="stylesheet" href="../../styles/qingyang-components.css">
<link rel="stylesheet" href="../../styles/qingyang-forms.css">
```

**聚合入口（适合一次性引入或旧页面过渡）：**

```html
<link rel="stylesheet" href="../../styles/qingyang-design-system.css">
```

两种入口不应在同一页面混用。`qingyang-variables.css` 是 token 的 canonical 来源；`qingyang-design-system.css` 是聚合快照，用于保持兼容。新页面不得在页面内重新定义 `--qy-*` token，也不得覆盖 `.qy-btn`、`.qy-table`、`.qy-layout` 等系统级组件类；页面私有样式应使用业务命名空间，例如 `.reconciliation-*`、`.employee-*`。

### 基础重置与样式

```css
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

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

/* Skip Link */
.qy-skip-link {
  position: absolute; top: -100%; left: 50%; transform: translateX(-50%);
  padding: var(--qy-space-2) var(--qy-space-4); background: var(--qy-primary-500);
  color: white; border-radius: var(--qy-radius-md); z-index: 9999;
  transition: top var(--qy-transition-fast);
}
.qy-skip-link:focus { top: var(--qy-space-4); }

/* Focus States */
*:focus-visible { outline: none; box-shadow: var(--qy-focus-ring); }

/* Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important; transition-duration: 0.01ms !important; }
}
```

---

### 11.1 按钮 Button

```html
<button class="qy-btn qy-btn--primary">主要操作</button>
<button class="qy-btn qy-btn--primary" disabled>禁用状态</button>
<button class="qy-btn qy-btn--secondary">次要操作</button>
<button class="qy-btn qy-btn--text">文字按钮</button>
<button class="qy-btn qy-btn--danger">危险操作</button>
<button class="qy-btn qy-btn--primary qy-btn--lg">大按钮</button>
```

```css
/* 基础按钮 */
.qy-btn {
  display: inline-flex; align-items: center; justify-content: center;
  gap: var(--qy-space-2); padding: 0 var(--qy-space-4);
  font-family: inherit; font-size: var(--qy-font-size-base);
  font-weight: var(--qy-font-weight-medium); line-height: 1;
  border: 1px solid transparent; border-radius: var(--qy-radius-md);
  cursor: pointer; transition: all var(--qy-transition-fast); white-space: nowrap;
}

/* 尺寸 */
.qy-btn--sm { height: 28px; font-size: var(--qy-font-size-sm); }
.qy-btn--md { height: 32px; }
.qy-btn--lg { height: 40px; padding: 0 var(--qy-space-5); }

/* 主按钮 */
.qy-btn--primary {
  height: 32px; background: var(--qy-primary-500); color: white;
}
.qy-btn--primary:hover:not(:disabled) { background: var(--qy-primary-600); }
.qy-btn--primary:active:not(:disabled) { background: var(--qy-primary-700); }
.qy-btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }

/* 次按钮 */
.qy-btn--secondary {
  height: 32px; background: white; border-color: var(--qy-border-medium); color: var(--qy-text-secondary);
}
.qy-btn--secondary:hover:not(:disabled) { background: var(--qy-bg-secondary); border-color: var(--qy-border-light); }

/* 文字按钮 */
.qy-btn--text {
  height: 32px; background: transparent; color: var(--qy-primary-500);
}
.qy-btn--text:hover:not(:disabled) { background: var(--qy-primary-50); }

/* 危险按钮 */
.qy-btn--danger {
  height: 32px; background: var(--qy-error-500); color: white;
}
.qy-btn--danger:hover:not(:disabled) { background: var(--qy-error-600); }
```

#### 行内操作按钮 Row Action

```html
<button class="qy-btn-action qy-btn-action--primary">参保</button>
<button class="qy-btn-action qy-btn-action--warning">减员</button>
<button class="qy-btn-action qy-btn-action--text">详情</button>
```

```css
.qy-btn-action {
  display: inline-flex; align-items: center; height: 24px;
  padding: 0 var(--qy-space-3); font-size: var(--qy-font-size-sm);
  font-weight: var(--qy-font-weight-medium); border: 1px solid;
  border-radius: var(--qy-radius-full); cursor: pointer;
  transition: all var(--qy-transition-fast);
}
.qy-btn-action--primary {
  background: var(--qy-primary-50); border-color: var(--qy-primary-200); color: var(--qy-primary-600);
}
.qy-btn-action--warning {
  background: var(--qy-warning-50); border-color: var(--qy-warning-200); color: var(--qy-warning-600);
}
.qy-btn-action--text {
  background: transparent; border-color: transparent; color: var(--qy-primary-500);
}
.qy-btn-action:hover { filter: brightness(0.95); }
```

#### 全宽按钮（登录/提交表单底部）
- 高度：44px | 字号：16px | 宽度：100%

---

### 11.2 输入框 Input

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
.qy-form-group { display: flex; flex-direction: column; gap: var(--qy-space-2); }

.qy-label {
  font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium); color: var(--qy-text-primary);
}
.qy-required { color: var(--qy-error-500); margin-left: var(--qy-space-1); }

.qy-input {
  height: 32px; padding: 0 var(--qy-space-3); font-family: inherit;
  font-size: var(--qy-font-size-base); color: var(--qy-text-primary);
  background: var(--qy-bg-secondary); border: 1px solid var(--qy-border-medium);
  border-radius: var(--qy-radius-md); transition: all var(--qy-transition-fast);
}
.qy-input:hover:not(:disabled) { border-color: var(--qy-border-focus); }
.qy-input:focus { outline: none; border-color: var(--qy-primary-400); box-shadow: var(--qy-focus-ring); }
.qy-input::placeholder { color: var(--qy-text-muted); }
.qy-input:disabled { background: var(--qy-bg-tertiary); color: var(--qy-text-disabled); cursor: not-allowed; }
.qy-input--error { border-color: var(--qy-error-500); }
.qy-input--error:focus { box-shadow: 0 0 0 3px var(--qy-error-50); }

.qy-help-text { font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary); }
.qy-error-text { font-size: var(--qy-font-size-sm); color: var(--qy-error-500); }

/* 大尺寸 */
.qy-input--lg { height: 40px; padding: 0 var(--qy-space-4); }
```

#### 密码输入框
- **眼睛图标位置**：右侧内嵌，距右边 12px
- **图标大小**：16px
- **图标颜色**：`--qy-text-muted` 默认，`--qy-primary-500` 悬停/激活
- **切换逻辑**：点击切换 type="password" / type="text"
- **背景**：白色或 `--qy-bg-primary`

#### 登录专用输入框
- **高度**：40px | **字号**：14px | **圆角**：8px
- **边框**：`--qy-border-medium` | **占位符**：`--qy-text-muted`
- **间距**：输入框之间 16px-20px

#### 验证状态

| 状态 | 样式 |
|------|------|
| 默认 | `--qy-border-medium` |
| 焦点 | `--qy-border-focus`，焦点环阴影 |
| 错误 | `--qy-error-500` 边框，error-50 背景 |
| 成功 | `--qy-success-500`（可选）|
| 禁用 | `--qy-bg-tertiary`，`--qy-text-muted` |

#### 错误提示
- 位置：输入框下方
- 字体：12px，`--qy-error-500`
- 图标：16px alert 图标 + 8px 间距
- 间距：距输入框 4px

---

### 11.3 下拉选择 Select

```html
<div class="qy-select-wrapper">
  <select class="qy-select">
    <option value="">请选择</option>
    <option value="1">选项1</option>
  </select>
</div>
```

```css
.qy-select-wrapper { position: relative; }
.qy-select-wrapper::after {
  content: ''; position: absolute; right: var(--qy-space-3); top: 50%; transform: translateY(-50%);
  width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent;
  border-top: 4px solid var(--qy-text-secondary); pointer-events: none;
}
.qy-select {
  appearance: none; width: 100%; height: 32px; padding: 0 var(--qy-space-8) 0 var(--qy-space-3);
  font-family: inherit; font-size: var(--qy-font-size-base); color: var(--qy-text-primary);
  background: var(--qy-bg-secondary); border: 1px solid var(--qy-border-medium);
  border-radius: var(--qy-radius-md); cursor: pointer; transition: all var(--qy-transition-fast);
}
.qy-select:focus { outline: none; border-color: var(--qy-primary-400); box-shadow: var(--qy-focus-ring); }
```

#### Combobox（下拉输入框组合）
用于筛选工具栏，如"按结算主体"、"湖南立人科技有限公司"

```html
<div class="qy-combobox" aria-label="结算主体">
  <span class="qy-combobox__text">按结算主体</span>
  <span class="qy-combobox__arrow"><svg viewBox="0 0 12 12" fill="currentColor"><path d="M3 4.5L6 7.5L9 4.5"/></svg></span>
</div>
```

```css
.qy-combobox {
  display: inline-flex; align-items: center; height: 32px; padding: 0 var(--qy-space-3);
  background: var(--qy-bg-secondary); border: 1px solid var(--qy-border-medium);
  border-radius: var(--qy-radius-md); cursor: pointer; transition: all var(--qy-transition-fast);
}
.qy-combobox:hover { border-color: var(--qy-border-focus); }
.qy-combobox:focus-within { outline: none; border-color: var(--qy-primary-400); box-shadow: var(--qy-focus-ring); }
.qy-combobox__text { font-size: var(--qy-font-size-sm); color: var(--qy-text-primary); white-space: nowrap; }
.qy-combobox__arrow { display: flex; align-items: center; margin-left: var(--qy-space-2); color: var(--qy-text-secondary); }
.qy-combobox__arrow svg { width: 12px; height: 12px; }
```

---

### 11.4 复选框 Checkbox

```
尺寸：16px × 16px | 圆角：4px | 边框：1px solid --qy-border-medium

选中状态：背景 --qy-primary-500，边框 --qy-primary-500，图标白色对勾 ✓
悬停状态：未选中 → border-primary-400；已选中 → primary-600
禁用状态：背景 --qy-bg-tertiary，边框 --qy-border-light
```

#### 带文字的复选框
```
布局：flex 横向排列 | 间距：8px | 文字：14px，--qy-text-secondary | 垂直对齐：居中
```

---

### 11.5 卡片 Card

```html
<div class="qy-card">
  <div class="qy-card__header">
    <h3 class="qy-card__title">卡片标题</h3>
    <span class="qy-card__extra">额外信息</span>
  </div>
  <div class="qy-card__body">卡片内容区域</div>
  <div class="qy-card__footer">
    <button class="qy-btn qy-btn--secondary">取消</button>
    <button class="qy-btn qy-btn--primary">确认</button>
  </div>
</div>
```

```css
.qy-card {
  background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-lg); box-shadow: var(--qy-shadow-card);
}
.qy-card__header {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--qy-space-4) var(--qy-space-5); border-bottom: 1px solid var(--qy-border-light);
}
.qy-card__title { font-size: var(--qy-font-size-lg); font-weight: var(--qy-font-weight-semibold); color: var(--qy-text-primary); }
.qy-card__extra { font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary); }
.qy-card__body { padding: var(--qy-space-5); }
.qy-card__footer {
  display: flex; justify-content: flex-end; gap: var(--qy-space-3);
  padding: var(--qy-space-4) var(--qy-space-5); border-top: 1px solid var(--qy-border-light);
}
```

#### KPI 卡片

```html
<button class="qy-kpi-card" aria-pressed="false">
  <span class="qy-kpi-card__value">275</span>
  <span class="qy-kpi-card__label">全部</span>
</button>
```

```css
.qy-kpi-card {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-width: 120px; padding: var(--qy-space-4); background: white;
  border: 1px solid var(--qy-border-light); border-radius: var(--qy-radius-md);
  cursor: pointer; transition: all var(--qy-transition-fast);
}
.qy-kpi-card:hover { background: var(--qy-bg-secondary); }
.qy-kpi-card[aria-pressed="true"] { background: var(--qy-primary-50); border-color: var(--qy-primary-200); }
.qy-kpi-card__value {
  font-size: 24px; font-weight: var(--qy-font-weight-bold); color: var(--qy-text-primary);
  font-variant-numeric: tabular-nums;
}
.qy-kpi-card[aria-pressed="true"] .qy-kpi-card__value { color: var(--qy-primary-600); }
.qy-kpi-card__label { font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary); margin-top: var(--qy-space-1); }
```

#### Hero 卡片（带左侧强调条）
- 最小高度：120px
- 左侧强调条：4px 宽，圆角
- 内边距：18px 20px
- 布局：左侧强调条 + 内容区

#### Stats Cards（统计数据条）
如参保状态统计

```html
<div class="qy-stats-bar">
  <div class="qy-stats-bar__item is-active">
    <span class="qy-stats-bar__count">0</span>
    <span class="qy-stats-bar__label">已参保</span>
  </div>
  <div class="qy-stats-bar__divider"></div>
  <button class="qy-btn qy-btn--secondary">离职员工</button>
</div>
```

```css
.qy-stats-bar { display: flex; align-items: center; gap: var(--qy-space-4); padding: var(--qy-space-4) 0; margin-bottom: var(--qy-space-4); flex-wrap: wrap; }
.qy-stats-bar__item {
  display: flex; align-items: center; gap: var(--qy-space-3); padding: var(--qy-space-3) var(--qy-space-4);
  background: var(--qy-bg-primary); border: 1px solid var(--qy-border-light);
  border-radius: var(--qy-radius-md); cursor: pointer; transition: all var(--qy-transition-fast);
}
.qy-stats-bar__item:hover { background: var(--qy-bg-secondary); }
.qy-stats-bar__item.is-active { background: var(--qy-primary-50); border-color: var(--qy-primary-200); }
.qy-stats-bar__count { font-size: var(--qy-font-size-lg); font-weight: var(--qy-font-weight-bold); font-variant-numeric: tabular-nums; color: var(--qy-text-primary); }
.qy-stats-bar__item.is-active .qy-stats-bar__count { color: var(--qy-primary-600); }
.qy-stats-bar__label { font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary); }
.qy-stats-bar__divider { width: 1px; height: 20px; background: var(--qy-border-light); margin: 0 var(--qy-space-2); }
```

---

### 11.6 标签 Tag

```html
<span class="qy-tag qy-tag--default">默认</span>
<span class="qy-tag qy-tag--primary">主要</span>
<span class="qy-tag qy-tag--success">成功</span>
<span class="qy-tag qy-tag--warning">警告</span>
<span class="qy-tag qy-tag--error">错误</span>
<span class="qy-tag qy-tag--success qy-tag--dot">带圆点</span>
```

```css
.qy-tag {
  display: inline-flex; align-items: center; height: 22px; padding: 0 var(--qy-space-3);
  font-size: var(--qy-font-size-xs); font-weight: var(--qy-font-weight-medium);
  border-radius: var(--qy-radius-full); white-space: nowrap;
}
.qy-tag--default { background: var(--qy-bg-secondary); color: var(--qy-text-secondary); }
.qy-tag--primary { background: var(--qy-primary-50); color: var(--qy-primary-600); }
.qy-tag--success { background: var(--qy-success-50); color: var(--qy-success-600); }
.qy-tag--warning { background: var(--qy-warning-50); color: var(--qy-warning-600); }
.qy-tag--error   { background: var(--qy-error-50);   color: var(--qy-error-600); }

/* 带圆点 */
.qy-tag--dot::before { content: ''; width: 6px; height: 6px; border-radius: 50%; margin-right: 6px; }
.qy-tag--success.qy-tag--dot::before { background: var(--qy-success-500); }
.qy-tag--warning.qy-tag--dot::before { background: var(--qy-warning-500); }
.qy-tag--error.qy-tag--dot::before   { background: var(--qy-error-500); }
```

---

### 11.7 提示 Alert

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
  display: flex; align-items: center; gap: var(--qy-space-3); padding: var(--qy-space-3) var(--qy-space-4);
  border-radius: var(--qy-radius-md); border-left: 3px solid;
}
.qy-alert--info    { background: var(--qy-primary-50); border-left-color: var(--qy-primary-500); }
.qy-alert--success { background: var(--qy-success-50); border-left-color: var(--qy-success-500); }
.qy-alert--warning { background: var(--qy-warning-50); border-left-color: var(--qy-warning-500); }
.qy-alert--error   { background: var(--qy-error-50);   border-left-color: var(--qy-error-500); }

/* Banner 变体（无边框） */
.qy-alert--banner { border-left: none; border: 1px solid; border-radius: var(--qy-radius-md); }
.qy-alert--banner.qy-alert--warning { background: var(--qy-warning-50); border-color: #FED7AA; }

.qy-alert__content { flex: 1; font-size: var(--qy-font-size-sm); }
.qy-alert__action  { font-size: var(--qy-font-size-sm); color: var(--qy-primary-500); text-decoration: none; }
.qy-alert__action:hover { text-decoration: underline; }
.qy-alert__close {
  display: flex; align-items: center; justify-content: center; width: 20px; height: 20px;
  font-size: 16px; color: var(--qy-text-secondary); background: transparent; border: none;
  cursor: pointer; border-radius: var(--qy-radius-sm);
}
.qy-alert__close:hover { background: rgba(0,0,0,0.05); }
```

#### Inline Warning Banner（内联警告横幅）
用于列表页顶部的重要提醒，如"XX人未参保"

```html
<div class="qy-warning-banner">
  <div class="qy-warning-banner__content">
    <span class="qy-warning-banner__icon">⚠️</span>
    <span class="qy-warning-banner__text">
      <span class="qy-warning-banner__names">李先生，谭...等</span>
      <span class="qy-warning-banner__count">260</span>人在职未参保
    </span>
  </div>
  <button class="qy-warning-banner__action">立即处理</button>
</div>
```

```css
.qy-warning-banner {
  display: flex; align-items: center; justify-content: space-between;
  padding: var(--qy-space-3) var(--qy-space-4); background: var(--qy-warning-50);
  border: 1px solid #FED7AA; border-radius: var(--qy-radius-md); margin-bottom: var(--qy-space-4);
}
.qy-warning-banner__content { display: flex; align-items: center; gap: var(--qy-space-3); }
.qy-warning-banner__icon { display: flex; align-items: center; justify-content: center; width: 20px; height: 20px; color: var(--qy-warning-500); }
.qy-warning-banner__text { font-size: var(--qy-font-size-sm); color: var(--qy-text-primary); }
.qy-warning-banner__names { color: var(--qy-primary-500); font-weight: var(--qy-font-weight-medium); }
.qy-warning-banner__count { font-weight: var(--qy-font-weight-semibold); }
.qy-warning-banner__action {
  font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium); color: var(--qy-primary-500);
  background: none; border: none; cursor: pointer; padding: var(--qy-space-1) var(--qy-space-2);
  border-radius: var(--qy-radius-sm); transition: background var(--qy-transition-fast);
}
.qy-warning-banner__action:hover { background: var(--qy-primary-50); }
```

---

### 11.8 表格 Table

```html
<div class="qy-table-container" role="region" aria-label="数据表格" tabindex="0">
  <table class="qy-table">
    <thead>
      <tr>
        <th class="qy-table__checkbox"><input type="checkbox" aria-label="全选"></th>
        <th>姓名</th><th>部门</th><th>状态</th>
        <th class="qy-table__actions">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="qy-table__checkbox"><input type="checkbox" aria-label="选择张三"></td>
        <td>张三</td><td>技术部</td>
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
.qy-table-container { overflow-x: auto; border: 1px solid var(--qy-border-light); border-radius: var(--qy-radius-lg); }
.qy-table { width: 100%; border-collapse: collapse; font-size: var(--qy-font-size-sm); }
.qy-table thead { background: var(--qy-bg-secondary); }
.qy-table th {
  padding: var(--qy-space-3) var(--qy-space-4); font-weight: var(--qy-font-weight-semibold);
  font-size: var(--qy-font-size-xs); text-transform: uppercase; letter-spacing: 0.5px;
  color: var(--qy-text-secondary); text-align: left; white-space: nowrap;
}
.qy-table td { padding: var(--qy-space-3) var(--qy-space-4); border-bottom: 1px solid var(--qy-border-light); }
.qy-table tbody tr { transition: background var(--qy-transition-fast); }
.qy-table tbody tr:hover { background: var(--qy-bg-secondary); }
.qy-table tbody tr:last-child td { border-bottom: none; }
.qy-table__checkbox { width: 44px; text-align: center; }
.qy-table__actions  { width: 120px; white-space: nowrap; }
.qy-table__actions > * + * { margin-left: var(--qy-space-2); }
.qy-table tbody tr.is-selected { background: var(--qy-primary-50); }
/* 斑马纹（可选） */
.qy-table--striped tbody tr:nth-child(even) { background: #FAFBFC; }
.qy-table--striped tbody tr:nth-child(even):hover { background: var(--qy-bg-secondary); }
/* 行高 */
.qy-table--compact td    { padding: var(--qy-space-2) var(--qy-space-4); }
.qy-table--comfortable td { padding: var(--qy-space-4); }
/* 空值显示 */
.qy-table td:empty::after, .qy-table td:has(> .qy-placeholder) { content: '--'; color: var(--qy-text-muted); }

/* 单元格内联信息 */
.qy-cell-info { display: flex; flex-direction: column; gap: 2px; }
.qy-cell-info__primary   { font-size: var(--qy-font-size-sm); color: var(--qy-text-primary); }
.qy-cell-info__secondary { font-size: var(--qy-font-size-xs); color: var(--qy-text-secondary); }
```

#### 表格工具栏（表格上方筛选、操作栏）
```css
.qy-table-toolbar {
  display: flex; align-items: center; justify-content: space-between; gap: var(--qy-space-4);
  margin-bottom: var(--qy-space-4); flex-wrap: wrap;
}
.qy-table-toolbar__left, .qy-table-toolbar__right { display: flex; align-items: center; gap: var(--qy-space-3); flex-wrap: wrap; }
```

---

### 11.9 分页 Pagination

```html
<nav class="qy-pagination" aria-label="分页">
  <span class="qy-pagination__total">共 260 条数据</span>
  <div class="qy-pagination__pages">
    <button class="qy-pagination__btn" disabled aria-label="上一页">‹</button>
    <button class="qy-pagination__btn qy-pagination__btn--active" aria-current="page">1</button>
    <button class="qy-pagination__btn">2</button>
    <span class="qy-pagination__ellipsis">•••</span>
    <button class="qy-pagination__btn">26</button>
    <button class="qy-pagination__btn" aria-label="下一页">›</button>
  </div>
  <div class="qy-pagination__options">
    <div class="qy-combobox">
      <span class="qy-combobox__text">10 条/页</span>
      <span class="qy-combobox__arrow">▼</span>
    </div>
    <span class="qy-pagination__jump">跳至 <input type="text" class="qy-input qy-input--sm" style="width: 48px;"> 页</span>
  </div>
</nav>
```

```css
.qy-pagination { display: flex; align-items: center; justify-content: space-between; padding: var(--qy-space-4) 0; font-size: var(--qy-font-size-sm); }
.qy-pagination__total { color: var(--qy-text-secondary); }
.qy-pagination__pages { display: flex; align-items: center; gap: var(--qy-space-1); }
.qy-pagination__btn {
  display: flex; align-items: center; justify-content: center; min-width: 32px; height: 32px;
  padding: 0 var(--qy-space-2); font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary);
  background: transparent; border: none; border-radius: var(--qy-radius-sm);
  cursor: pointer; transition: all var(--qy-transition-fast);
}
.qy-pagination__btn:hover:not(:disabled) { background: var(--qy-bg-secondary); color: var(--qy-text-primary); }
.qy-pagination__btn--active { background: var(--qy-primary-500) !important; color: white !important; }
.qy-pagination__btn:disabled { opacity: 0.4; cursor: not-allowed; }
.qy-pagination__ellipsis { color: var(--qy-text-muted); padding: 0 var(--qy-space-1); letter-spacing: 2px; }
.qy-pagination__options { display: flex; align-items: center; gap: var(--qy-space-4); }
.qy-pagination__jump { display: flex; align-items: center; gap: var(--qy-space-2); color: var(--qy-text-secondary); }
```

---

### 11.10 分段控制器 Segmented Control

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
.qy-segmented { display: inline-flex; padding: 2px; background: var(--qy-bg-secondary); border-radius: var(--qy-radius-md); }
.qy-segmented__item {
  display: flex; align-items: center; gap: var(--qy-space-2); height: 32px; padding: 0 var(--qy-space-4);
  font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium); color: var(--qy-text-secondary);
  background: transparent; border: none; border-radius: var(--qy-radius-sm);
  cursor: pointer; transition: all var(--qy-transition-fast); white-space: nowrap;
}
.qy-segmented__item:hover:not(.is-active) { color: var(--qy-text-primary); }
.qy-segmented__item.is-active { background: white; color: var(--qy-text-primary); box-shadow: var(--qy-shadow-sm); }
.qy-segmented__badge {
  display: inline-flex; align-items: center; height: 16px; padding: 0 6px;
  font-size: 11px; font-weight: var(--qy-font-weight-semibold);
  background: var(--qy-bg-tertiary); border-radius: var(--qy-radius-full);
}
.qy-segmented__item.is-active .qy-segmented__badge { background: var(--qy-primary-100); color: var(--qy-primary-600); }
```

---

### 11.11 保险类型选项卡 Insurance Tabs

```html
<div class="qy-insurance-tabs" role="tablist" aria-label="保险类型">
  <button class="qy-insurance-tabs__item is-active" role="tab" aria-selected="true">社保</button>
  <button class="qy-insurance-tabs__item" role="tab" aria-selected="false">公积金</button>
  <button class="qy-insurance-tabs__item" role="tab" aria-selected="false">商保</button>
</div>
```

```css
.qy-insurance-tabs { display: flex; gap: var(--qy-space-6); padding-bottom: var(--qy-space-4); border-bottom: 1px solid var(--qy-border-light); margin-bottom: var(--qy-space-4); }
.qy-insurance-tabs__item {
  position: relative; padding: var(--qy-space-2) 0; font-size: var(--qy-font-size-base);
  font-weight: var(--qy-font-weight-medium); color: var(--qy-text-secondary);
  background: transparent; border: none; cursor: pointer; transition: color var(--qy-transition-fast);
}
.qy-insurance-tabs__item:hover { color: var(--qy-text-primary); }
.qy-insurance-tabs__item.is-active { color: var(--qy-primary-600); font-weight: var(--qy-font-weight-semibold); }
.qy-insurance-tabs__item.is-active::after {
  content: ''; position: absolute; bottom: -var(--qy-space-4); left: 0; right: 0;
  height: 2px; background: var(--qy-primary-500); border-radius: 1px;
}
```

---

### 11.12 空状态 Empty State

```html
<div class="qy-empty">
  <div class="qy-empty__icon"><!-- SVG 图标 --></div>
  <h3 class="qy-empty__title">暂无数据</h3>
  <p class="qy-empty__description">当前列表为空，请点击下方按钮添加</p>
  <button class="qy-btn qy-btn--primary">添加数据</button>
</div>
```

```css
.qy-empty { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: var(--qy-space-12) var(--qy-space-6); text-align: center; }
.qy-empty__icon { width: 64px; height: 64px; margin-bottom: var(--qy-space-4); color: var(--qy-text-muted); }
.qy-empty__icon svg { width: 100%; height: 100%; }
.qy-empty__title { font-size: var(--qy-font-size-md); font-weight: var(--qy-font-weight-semibold); color: var(--qy-text-primary); margin-bottom: var(--qy-space-2); }
.qy-empty__description { font-size: var(--qy-font-size-sm); color: var(--qy-text-secondary); margin-bottom: var(--qy-space-5); max-width: 400px; }
```

---

### 11.13 抽屉 Drawer

从页面侧边滑出的面板，用于展示详情、表单或辅助操作。

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

**位置变体**：`qy-drawer--left` `qy-drawer--right` `qy-drawer--top` `qy-drawer--bottom`

**CSS 变量**：
```css
--qy-drawer-width: 520px;           /* 右侧/左侧抽屉宽度 */
--qy-drawer-height: 300px;          /* 顶部/底部抽屉高度 */
--qy-drawer-max-width: 90vw;        /* 最大宽度 */
--qy-drawer-overlay: rgba(0,0,0,0.5); /* 遮罩颜色 */
```

**规格**：
- 抽屉宽度：520px（右侧/左侧）
- 抽屉高度：300px（顶部/底部）
- 遮罩层：rgba(0,0,0,0.5)
- 标题字号：16px，字重 600
- 分段标题字号：14px，字重 600
- 底部按钮栏内边距：16px 20px
- 表单分组间距：16px

**实际应用**：
- `employeeManage/employee/index` 花名册添加人员抽屉
- `employeeManage/employee/detail` 员工详情抽屉

---

### 11.14 导航 Navigation

#### 侧边栏 + 主内容布局

侧边栏与主内容区采用 flex 横向排列，`.qy-main` 通过 `flex: 1` 自动占据剩余空间，无需 margin-left 偏移。

```css
.qy-layout { display: flex; height: 100vh; overflow: hidden; }
.qy-sidebar {
  width: var(--qy-sidebar-width); background: var(--qy-bg-primary);
  border-right: 1px solid var(--qy-border-light); flex-shrink: 0;
}
.qy-main { flex: 1; margin-left: 0; min-width: 0; overflow: hidden; }
.qy-sidebar__logo {
  display: flex; align-items: center; height: var(--qy-header-height);
  padding: 0 var(--qy-space-4); border-bottom: 1px solid var(--qy-border-light);
}
.qy-sidebar__nav { padding: var(--qy-space-4); }
.qy-sidebar__group { margin-bottom: var(--qy-space-6); }
.qy-sidebar__title {
  padding: 0 var(--qy-space-3); margin-bottom: var(--qy-space-2);
  font-size: var(--qy-font-size-xs); font-weight: var(--qy-font-weight-semibold);
  color: var(--qy-text-muted); text-transform: uppercase; letter-spacing: 0.5px;
}
.qy-sidebar__item {
  display: flex; align-items: center; gap: var(--qy-space-3); padding: var(--qy-space-2) var(--qy-space-3);
  font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-secondary); text-decoration: none; border-radius: var(--qy-radius-md);
  transition: all var(--qy-transition-fast);
}
.qy-sidebar__item:hover { background: var(--qy-bg-secondary); color: var(--qy-text-primary); }
.qy-sidebar__item.is-active {
  background: var(--qy-primary-50); color: var(--qy-primary-600);
  font-weight: var(--qy-font-weight-semibold);
  border-left: 3px solid var(--qy-primary-500); margin-left: -3px;
}
.qy-sidebar__icon { width: 16px; height: 16px; }
```

**规格**：
- 内边距：9px 12px | 圆角：8px | 字体：13px，weight 500
- 图标：16px，右侧间距 10px
- 激活状态：背景 primary-50，文字 primary-600，weight 600，左侧 3px 强调条

#### 顶部导航

```css
.qy-header {
  display: flex; align-items: center; justify-content: space-between;
  height: var(--qy-header-height); padding: 0 var(--qy-space-6);
  background: var(--qy-bg-primary); border-bottom: 1px solid var(--qy-border-light);
  position: sticky; top: 0; z-index: 100;
}
.qy-header__nav { display: flex; gap: var(--qy-space-6); }
.qy-header__tab {
  position: relative; height: var(--qy-header-height); padding: 0 var(--qy-space-1);
  font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium);
  color: var(--qy-text-secondary); background: transparent; border: none;
  cursor: pointer; transition: color var(--qy-transition-fast);
}
.qy-header__tab:hover { color: var(--qy-text-primary); }
.qy-header__tab.is-active { color: var(--qy-primary-600); font-weight: var(--qy-font-weight-semibold); }
.qy-header__tab.is-active::after {
  content: ''; position: absolute; bottom: 0; left: 0; right: 0;
  height: 2px; background: var(--qy-primary-500);
}
```

**规格**：高度 52px | 内边距 0 28px | 位置 sticky, top: 0

---

### 11.15 模态框/弹窗 Modal

```
遮罩：rgba(0,0,0,0.5)
背景：var(--qy-bg-primary)
圆角：var(--qy-radius-xl) (16px)
阴影：var(--qy-shadow-lg)
最大宽度：480px (小) / 640px (中) / 800px (大)

头部：
  内边距：16px 20px | 边框底部：var(--qy-border-light)
  标题：16px，weight 600

内容：
  内边距：20px | 最大高度：70vh | 可滚动

底部：
  内边距：12px 20px | 边框顶部：var(--qy-border-light)
  按钮右对齐
```

---

### 11.16 批量操作栏

```html
<div class="qy-bulk-bar" role="toolbar" aria-label="批量操作">
  <span class="qy-bulk-bar__count">已选 5 项</span>
  <button class="qy-btn qy-btn--text">批量操作1</button>
  <button class="qy-btn qy-btn--text">批量操作2</button>
</div>
```

```css
.qy-bulk-bar {
  display: flex; align-items: center; gap: var(--qy-space-4); padding: var(--qy-space-3) var(--qy-space-4);
  background: var(--qy-bg-secondary); border-radius: var(--qy-radius-md); margin-bottom: var(--qy-space-3);
}
.qy-bulk-bar__count { font-size: var(--qy-font-size-sm); font-weight: var(--qy-font-weight-medium); color: var(--qy-text-primary); }
```

---

## 12. 表单规范

### 12.1 基础垂直布局（推荐用于简单表单）

```
标签 + 输入框（垂直布局）
内边距：8px 0
标签：12px，weight 500，text-secondary
输入框间距：16px
```

### 12.2 网格布局（用于复杂表单/配置页面）

当表单包含多个字段且需要紧凑展示时，使用 CSS Grid：

```css
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--qy-space-4);
}
.form-field--full { grid-column: 1 / -1; }
```

**响应式断点规则：**

| 断点 | 每行字段数 | 说明 |
|------|-----------|------|
| < 768px (Mobile) | 1 列 | 单列堆叠 |
| 768px - 1024px (Tablet) | 2 列 | 双列布局 |
| 1024px - 1440px (Desktop) | 3 列 | 三列布局 |
| > 1440px (Large) | 4 列 | 四列布局 |

**字段跨度规则：**
- 重要字段（如方案名称、方案编码）可设置为 `form-field--full` 占据整行
- 相关字段组可使用 2 列跨越
- 下拉选择、日期选择等可根据重要性设置跨列

```
┌─────────────┬─────────────┬─────────────┐
│ 方案名称*   │ 方案编码*   │ 所属客户*   │  ← 3列
├─────────────┴─────────────┼─────────────┤
│ 适用范围（跨2列）         │ 状态        │  ← 2+1列
├───────────────────────────┴─────────────┤
│ 备注（跨3列）                          │  ← 全宽
└─────────────────────────────────────────┘
```

---

## 13. 数据可视化

### 13.1 图表颜色

```
主色序列：#2563EB → #60A5FA → #93C5FD → #BFDBFE
辅助色：#22C55E（正向）/ #EF4444（负向）/ #F97316（警告）
```

### 13.2 图表规范
- 使用圆角线条（stroke-linecap: round）
- 数据点使用清晰标记
- 提供图例说明
- 坐标轴标签使用 text-muted 的颜色
- 网格线使用虚线，颜色 border-light

---

## 14. 登录页面

### 14.1 页面布局

```
┌─────────────────────────────────────────────────────┐
│  左侧品牌区 (50%)          │  右侧登录表单区 (50%)   │
│  ┌────────────────────┐   │  ┌──────────────────┐  │
│  │ Logo               │   │  │ 欢迎来到青阳云   │  │
│  │                    │   │  │ HR SaaS          │  │
│  │ 一站式人力资源     │   │  │ 很高兴再次见到你 │  │
│  │ 管理平台           │   │  │                  │  │
│  │                    │   │  │ [企业账号输入框] │  │
│  │                    │   │  │ [个人账号输入框] │  │
│  │                    │   │  │ [密码输入框  👁] │  │
│  │                    │   │  │                  │  │
│  │                    │   │  │ [✓] 记住密码     │  │
│  │                    │   │  │                  │  │
│  │                    │   │  │ [   登 录   ]    │  │
│  │                    │   │  │                  │  │
│  └────────────────────┘   │  └──────────────────┘  │
│  Copyright © 2015-2026     │                        │
└─────────────────────────────────────────────────────┘
```

### 14.2 登录表单规范

```css
.login-title { font-size: 24px; font-weight: 700; color: var(--qy-text-primary); line-height: 1.3; }
.login-subtitle { font-size: 14px; color: var(--qy-text-muted); margin-top: 8px; }

.login-input {
  height: 40px; padding: 0 12px; border: 1px solid var(--qy-border-medium);
  border-radius: 8px; font-size: 14px; background: var(--qy-bg-primary);
}
.login-input:focus { border-color: var(--qy-primary-400); box-shadow: 0 0 0 3px var(--qy-primary-100); }
.login-input::placeholder { color: var(--qy-text-muted); }

.login-btn {
  width: 100%; height: 44px; background: var(--qy-primary-500); color: white;
  font-size: 16px; font-weight: 500; border-radius: 8px; border: none;
}
.login-btn:hover { background: var(--qy-primary-600); }
```

### 14.3 品牌区
- **Logo**：居中显示，宽度自适应
- **标语**："一站式人力资源管理平台"（字号 20-24px，颜色：白色或浅色，字重 400-500）
- **背景**：可使用品牌渐变色或抽象图案

### 14.4 页脚
- 版权信息：`Copyright © 2015-2026`
- 备案链接：下划线样式，`--qy-text-muted` 颜色，字体 12px，位置：左下角

---

## 15. 页面模板

### 15.1 标准列表页模板

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
  <a href="#main-content" class="qy-skip-link">跳转到主要内容</a>

  <div class="qy-layout">
    <aside class="qy-sidebar" role="navigation" aria-label="侧边导航">
      <div class="qy-sidebar__logo"><img src="logo.svg" alt="青阳云"></div>
      <nav class="qy-sidebar__nav">
        <div class="qy-sidebar__group">
          <div class="qy-sidebar__title">核心人事</div>
          <a href="#" class="qy-sidebar__item is-active" aria-current="page">
            <span class="qy-sidebar__icon">👥</span><span>花名册</span>
          </a>
          <a href="#" class="qy-sidebar__item">
            <span class="qy-sidebar__icon">📄</span><span>合同管理</span>
          </a>
        </div>
      </nav>
    </aside>

    <main class="qy-main" id="main-content">
      <header class="qy-header" role="banner">
        <nav class="qy-header__nav" role="tablist" aria-label="顶部导航">
          <button class="qy-header__tab is-active" role="tab" aria-selected="true">核心人事</button>
          <button class="qy-header__tab" role="tab">智能薪酬</button>
          <button class="qy-header__tab" role="tab">假勤管理</button>
        </nav>
        <div class="qy-header__user">
          <button class="qy-btn qy-btn--text">管理员</button>
        </div>
      </header>

      <div class="qy-page">
        <div class="qy-page__header">
          <h1 class="qy-page__title">页面标题</h1>
          <button class="qy-btn qy-btn--primary">添加</button>
        </div>

        <!-- KPI统计 -->
        <div class="qy-kpi-section">
          <button class="qy-kpi-card is-active" aria-pressed="true">
            <span class="qy-kpi-card__value">275</span><span class="qy-kpi-card__label">全部</span>
          </button>
          <button class="qy-kpi-card" aria-pressed="false">
            <span class="qy-kpi-card__value">12</span><span class="qy-kpi-card__label">已到期</span>
          </button>
        </div>

        <!-- 保险类型选项卡 -->
        <div class="qy-insurance-tabs" role="tablist">
          <button class="qy-insurance-tabs__item is-active">社保</button>
          <button class="qy-insurance-tabs__item">公积金</button>
          <button class="qy-insurance-tabs__item">商保</button>
        </div>

        <!-- Stats Bar -->
        <div class="qy-stats-bar">
          <div class="qy-stats-bar__item is-active">
            <span class="qy-stats-bar__count">0</span><span class="qy-stats-bar__label">已参保</span>
          </div>
          <div class="qy-stats-bar__item">
            <span class="qy-stats-bar__count">260</span><span class="qy-stats-bar__label">未参保</span>
          </div>
          <div class="qy-stats-bar__divider"></div>
          <button class="qy-btn qy-btn--secondary">离职员工</button>
        </div>

        <!-- Warning Banner -->
        <div class="qy-warning-banner">
          <div class="qy-warning-banner__content">
            <span class="qy-warning-banner__icon">⚠️</span>
            <span class="qy-warning-banner__text">
              <span class="qy-warning-banner__names">李先生，谭...等</span>
              <span class="qy-warning-banner__count">260</span>人在职未参保
            </span>
          </div>
          <button class="qy-warning-banner__action">立即处理</button>
        </div>

        <!-- 筛选工具栏 -->
        <div class="qy-table-toolbar">
          <div class="qy-table-toolbar__left">
            <div class="qy-combobox"><span class="qy-combobox__text">按结算主体</span><span class="qy-combobox__arrow">▼</span></div>
            <div class="qy-combobox"><span class="qy-combobox__text">湖南立人科技有限公司</span><span class="qy-combobox__arrow">▼</span></div>
            <input type="text" class="qy-input" style="width: 200px;" placeholder="姓名/手机号/证件号">
            <button class="qy-btn qy-btn--primary">搜索</button>
            <button class="qy-btn qy-btn--secondary">高级搜索</button>
          </div>
          <div class="qy-table-toolbar__right">
            <button class="qy-btn qy-btn--primary">批量导入</button>
            <button class="qy-btn qy-btn--secondary">•••</button>
          </div>
        </div>

        <!-- 批量操作栏 -->
        <div class="qy-bulk-bar" role="toolbar" aria-label="批量操作">
          <span class="qy-bulk-bar__count">已选 5 项</span>
          <button class="qy-btn qy-btn--text">批量操作1</button>
        </div>

        <!-- 数据表格 -->
        <div class="qy-table-container" role="region" aria-label="数据表格" tabindex="0">
          <table class="qy-table">
            <thead>
              <tr>
                <th class="qy-table__checkbox"><input type="checkbox" aria-label="全选"></th>
                <th>姓名</th><th>证件号码</th><th>所属客户</th><th>状态</th>
                <th class="qy-table__actions">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td class="qy-table__checkbox"><input type="checkbox" aria-label="选择行"></td>
                <td>张三</td><td>430***********1234</td>
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
          <span class="qy-pagination__total">共 260 条数据</span>
          <div class="qy-pagination__pages">
            <button class="qy-pagination__btn" disabled>‹</button>
            <button class="qy-pagination__btn qy-pagination__btn--active" aria-current="page">1</button>
            <button class="qy-pagination__btn">2</button>
            <button class="qy-pagination__btn">3</button>
            <span class="qy-pagination__ellipsis">•••</span>
            <button class="qy-pagination__btn">26</button>
            <button class="qy-pagination__btn">›</button>
          </div>
          <div class="qy-pagination__options">
            <div class="qy-combobox"><span class="qy-combobox__text">10 条/页</span><span class="qy-combobox__arrow">▼</span></div>
            <span class="qy-pagination__jump">跳至 <input type="text" class="qy-input qy-input--sm" style="width: 48px;"> 页</span>
          </div>
        </nav>
      </div>
    </main>
  </div>
</body>
</html>
```

### 15.2 CSS 布局

```css
/* 布局 — flex 方案，qy-main 不使用 margin-left 偏移 */
.qy-layout { display: flex; height: 100vh; overflow: hidden; }
.qy-sidebar { width: var(--qy-sidebar-width); flex-shrink: 0; border-right: 1px solid var(--qy-border-light); }
.qy-main { flex: 1; margin-left: 0; min-width: 0; display: flex; flex-direction: column; overflow: hidden; }
.qy-page { flex: 1; padding: 20px; overflow-y: auto; }
.qy-page__header { display: flex; align-items: center; justify-content: space-between; margin-bottom: var(--qy-space-6); }
.qy-page__title { font-size: var(--qy-font-size-2xl); font-weight: var(--qy-font-weight-bold); color: var(--qy-text-primary); }
.qy-kpi-section { display: flex; gap: var(--qy-space-4); margin-bottom: var(--qy-space-6); flex-wrap: wrap; }
.qy-btn--with-icon { display: inline-flex; align-items: center; gap: var(--qy-space-2); }
```

> **注意**: 原型文件位于 `prototype/<module>/` 目录下，CSS 引用路径为 `../../styles/`。始终从项目根目录启动 HTTP 服务。

### 15.3 HTML/CSS 文件模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面标题 - 青阳云</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root { /* 引用上述 CSS 变量 */ }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: var(--qy-font-family);
            background: var(--qy-bg-secondary);
            color: var(--qy-text-primary);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
        }
    </style>
</head>
<body>
    <!-- 页面内容 -->
</body>
</html>
```

---

## 16. 最佳实践

### 16.1 应该做的
- 使用语义化 HTML 标签
- 保持一致的间距和排版
- 为图标添加 `aria-label`
- 使用 loading 状态指示异步操作
- 提供清晰的错误反馈
- 使用骨架屏加载复杂内容

### 16.2 不应该做的
- 使用 Emoji 作为功能图标
- 依赖颜色作为唯一的信息传递方式
- 使用纯占位符作为标签
- 禁用浏览器的默认缩放
- 使用模糊的阴影或过度的装饰
- 混合多种设计风格

---

## 17. 设计检查清单

### 视觉质量
- [ ] 没有使用 emoji 作为图标（系统图标使用 SVG/图标字体）
- [ ] 所有图标来自同一图标库，风格一致
- [ ] 按下状态不会引起布局偏移
- [ ] 使用语义化颜色 token，没有硬编码色值

### 交互
- [ ] 所有可点击元素有清晰的按下反馈
- [ ] 触摸目标 ≥ 44×44px
- [ ] 微交互时长在 150-300ms 之间
- [ ] 禁用状态视觉清晰且不可交互
- [ ] 焦点顺序与视觉顺序一致

### 可访问性
- [ ] 正文对比度 ≥ 4.5:1
- [ ] 所有交互元素有可见焦点环
- [ ] 所有图片有 alt 文本
- [ ] 表单字段有关联标签
- [ ] 颜色不是唯一的指示方式
- [ ] 支持减少动画偏好

### B2B SaaS 特定
- [ ] 信息密度适中，适合长时间使用
- [ ] 高频操作路径短
- [ ] 数据表格支持排序、筛选、分页
- [ ] 批量操作清晰可发现
- [ ] 空状态提供明确引导

### 保险福利模块特定
- [ ] 使用 `qy-insurance-tabs` 展示保险类型切换
- [ ] 使用 `qy-stats-bar` 展示参保状态统计
- [ ] 使用 `qy-warning-banner` 展示待处理提醒
- [ ] 使用 `qy-combobox` 替代原生 select 用于筛选器
- [ ] 使用 `qy-table-toolbar` 布局筛选和操作按钮

---

## 18. 附录

### 18.1 命名规范

```
前缀: qy- (qingyang)

组件: .qy-{组件名}          例: .qy-btn, .qy-input, .qy-card
修饰符: .qy-{组件}--{修饰符} 例: .qy-btn--primary, .qy-btn--lg
子元素: .qy-{组件}__{子元素} 例: .qy-card__header, .qy-card__body
状态:   .is-{状态}           例: .is-active, .is-disabled, .is-selected
```

### 18.2 浏览器支持
- Chrome 90+ | Firefox 88+ | Safari 14+ | Edge 90+

### 18.3 性能预算
- 首屏加载 < 2s
- 可交互时间 (TTI) < 3.5s
- 累积布局偏移 (CLS) < 0.1
- 首次输入延迟 (FID) < 100ms

### 18.4 参考链接
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans)
- [Inter 字体](https://fonts.google.com/specimen/Inter)
- [Lucide 图标](https://lucide.dev/)
- [WCAG 2.1 指南](https://www.w3.org/WAI/WCAG21/quickref/)

### 18.5 更新日志
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-02 | 初始版本（guidelines）|
| v1.1 | 2026-04-03 | 新增登录页面设计规范 |
| v1.2 | 2026-04-10 | design-system 新增抽屉组件、更新默认宽度 |
| v2.0 | 2026-04-28 | 合并 guidelines + design-system，统一 `--qy-` 前缀，字号升级至 14px，字体改为 Plus Jakarta Sans |
| v2.1 | 2026-05-09 | 布局方案从 margin-left 改为 flex，原型按 7 业务模块分目录，CSS 引用路径调整为 `../../styles/`，页面边距调整为 20px |

---

*本文档是青阳云HRO系统的官方设计系统，所有原型设计必须遵循此规范。*
