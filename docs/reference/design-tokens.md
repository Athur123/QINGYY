---
title: 设计 Token 参考
module: design-system
type: reference
status: active
owner: athur
updated: 2026-05-16
source_of_truth: styles/qingyang-variables.css
---

# 设计 Token

## 核心颜色

| Token | 值 |
|-------|----|
| `--qy-primary-500` | `#2563EB` |
| `--qy-bg-secondary` | `#F8FAFC` |
| `--qy-text-primary` | `#1E293B` |
| `--qy-text-secondary` | `#64748B` |
| `--qy-border-light` | `#E2E8F0` |

## 字体

- 字体族：Plus Jakarta Sans、Inter、system-ui、sans-serif
- 默认正文：14px

## CSS 入口

| 入口类型 | 文件 |
|----------|------|
| 拆分入口 | `qingyang-variables.css`、`qingyang-base.css`、`qingyang-components.css`、`qingyang-forms.css` |
| 聚合入口 | `qingyang-design-system.css` |
| SCSS | `qingyang-variables.scss` |

同一 HTML 页面不要混用拆分入口和聚合入口。

### 样式归属规则

1. 设计变量 → `qingyang-variables.css`
2. 基础样式和工具类 → `qingyang-base.css`
3. 通用组件 → `qingyang-components.css`
4. 表单控件 → `qingyang-forms.css`
5. 聚合入口需与拆分入口语义一致

## 组件命名

类名使用 `qy-` 前缀，接近 BEM 结构：

| 类名 | 说明 | 常见变体/元素 |
|------|------|--------------|
| `qy-btn` | 按钮 | `--primary`、`--secondary`、`--text`、`--danger` |
| `qy-card` | 卡片 | `__header`、`__body`、`__footer` |
| `qy-input` | 输入框 | — |
| `qy-table` | 数据表格 | — |
| `qy-tag` | 标签/状态标识 | — |
