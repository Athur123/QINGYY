# 青阳云 UI/UE 设计规范

> 版本：v1.0  
> 更新日期：2026-04-02  
> 适用范围：青阳云 HRO 人力资源管理系统

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

| 角色 | 色值 | 用途 |
|------|------|------|
| Primary-500 | `#2563EB` | 主按钮、链接、强调色 |
| Primary-600 | `#1D4ED8` | 悬停状态、激活状态 |
| Primary-400 | `#60A5FA` | 次要强调、图标高亮 |
| Primary-200 | `#BFDBFE` | 边框、背景装饰 |
| Primary-100 | `#DBEAFE` | 轻量背景 |
| Primary-50 | `#EFF6FF` | 选中背景、hover背景 |

### 2.2 语义色

| 角色 | 色值 | 用途 |
|------|------|------|
| Success-500 | `#22C55E` | 成功状态、正向趋势 |
| Success-600 | `#16A34A` | 成功悬停 |
| Success-50 | `#F0FDF4` | 成功背景 |
| Warning-500 | `#F97316` | 警告、提醒、橙色标签 |
| Warning-600 | `#EA580C` | 警告悬停 |
| Warning-50 | `#FFF7ED` | 警告背景 |
| Error-500 | `#EF4444` | 错误、负向趋势、删除 |
| Error-600 | `#DC2626` | 错误悬停 |
| Error-50 | `#FEF2F2` | 错误背景 |

### 2.3 中性色

| 角色 | 色值 | 用途 |
|------|------|------|
| Text-Primary | `#1E293B` | 主要文本（标题、正文）|
| Text-Secondary | `#64748B` | 次要文本（说明、标签）|
| Text-Muted | `#94A3B8` | 弱化文本（占位符、禁用）|
| BG-Primary | `#FFFFFF` | 主背景（卡片、弹窗）|
| BG-Secondary | `#F8FAFC` | 次级背景（页面背景）|
| BG-Tertiary | `#F1F5F9` | 三级背景（输入框背景）|
| Border-Light | `#E2E8F0` | 浅色边框 |
| Border-Medium | `#CBD5E1` | 中等边框（输入框）|

### 2.4 使用规范

```css
:root {
  /* 主色 */
  --primary-50:  #EFF6FF;
  --primary-100: #DBEAFE;
  --primary-200: #BFDBFE;
  --primary-400: #60A5FA;
  --primary-500: #2563EB;
  --primary-600: #1D4ED8;

  /* 语义色 */
  --success-50:  #F0FDF4;
  --success-500: #22C55E;
  --success-600: #16A34A;

  --warning-50:  #FFF7ED;
  --warning-500: #F97316;
  --warning-600: #EA580C;

  --error-50:    #FEF2F2;
  --error-500:   #EF4444;
  --error-600:   #DC2626;

  /* 中性色 */
  --bg-primary:   #ffffff;
  --bg-secondary: #F8FAFC;
  --bg-tertiary:  #F1F5F9;

  --text-primary:   #1E293B;
  --text-secondary: #64748B;
  --text-muted:     #94A3B8;

  --border-light:  #E2E8F0;
  --border-medium: #CBD5E1;
}
```

---

## 3. 字体系统

### 3.1 字体选择

**主字体**：`Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

- 现代无衬线字体，专为屏幕阅读优化
- 支持多种字重（300-700）
- 优秀的数字显示效果

### 3.2 字号规范

| 级别 | 大小 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 24px | 1.3 | 700 | 页面大标题 |
| H2 | 20px | 1.3 | 700 | 区块标题 |
| H3 | 16px | 1.4 | 600 | 卡片标题 |
| H4 | 14px | 1.4 | 600 | 小标题 |
| Body | 13px | 1.5 | 400 | 正文文本 |
| Body-Small | 12px | 1.5 | 400 | 次要文本 |
| Caption | 11px | 1.4 | 500 | 标签、辅助文本 |
| Tiny | 10px | 1.4 | 600 | 徽章、时间戳 |

### 3.3 特殊文本

| 用途 | 大小 | 字重 | 颜色 |
|------|------|------|------|
| KPI 大数字 | 40px | 700 | text-primary |
| KPI 中数字 | 28px | 700 | text-primary |
| 导航链接 | 13px | 500 | text-secondary |
| 导航链接激活 | 13px | 600 | primary-600 |

---

## 4. 间距系统

### 4.1 基础间距（4px 网格）

| Token | 值 | 用途 |
|-------|-----|------|
| space-1 | 4px | 图标与文字间距 |
| space-2 | 8px | 小间距、紧凑布局 |
| space-3 | 12px | 按钮内边距（垂直）|
| space-4 | 16px | 标准间距、卡片内边距 |
| space-5 | 20px | 大间距、容器内边距 |
| space-6 | 24px | 页面内容区边距 |
| space-8 | 32px | 区块间距 |

### 4.2 布局间距

```
页面边距：24px 28px
侧边栏宽度：220px
顶部导航高度：52px
卡片内边距：16px - 20px
表单元素间距：16px
```

---

## 5. 圆角系统

| Token | 值 | 用途 |
|-------|-----|------|
| radius-sm | 4px | 小按钮、输入框、标签 |
| radius-md | 8px | 按钮、卡片、下拉菜单 |
| radius-lg | 12px | 大卡片、面板 |
| radius-xl | 16px | 弹窗、模态框 |
| radius-full | 9999px | 圆形元素（头像、徽章）|

---

## 6. 阴影系统

```css
--shadow-sm:   0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.02);
--shadow-md:   0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03);
--shadow-card: 0 2px 8px rgba(0,0,0,0.05), 0 1px 3px rgba(0,0,0,0.03);
--shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -2px rgba(0,0,0,0.04);
```

| Token | 用途 |
|-------|------|
| shadow-sm | 下拉菜单、小卡片 |
| shadow-card | 标准卡片 |
| shadow-md | 悬停状态、浮动元素 |
| shadow-lg | 弹窗、模态框、抽屉 |

---

## 7. 组件规范

### 7.1 按钮

#### 主按钮（Primary）
```
高度：32px / 40px / 44px（大）
内边距：0 16px
背景：primary-500
文字：白色，13px-16px，weight 500
圆角：radius-md (8px)
悬停：primary-600
禁用：opacity 0.5，cursor not-allowed
过渡：200ms ease
```

**全宽按钮**
- 用于登录、提交等表单底部
- 高度：44px
- 字号：16px
- 宽度：100%

#### 次按钮（Secondary）
```
背景：white
边框：1px solid border-medium
文字：text-secondary
悬停：bg-secondary
```

#### 文字按钮（Text）
```
背景：transparent
文字：primary-500
悬停：primary-50 背景
```

#### 危险按钮（Danger）
```
背景：error-500
悬停：error-600
```

### 7.2 输入框

```
高度：32px / 40px
内边距：0 12px
背景：bg-secondary
边框：1px solid border-medium
圆角：radius-md (8px)
字体：13px

焦点状态：
- 边框：primary-400
- 阴影：0 0 0 3px primary-100

禁用状态：
- 背景：bg-tertiary
- 文字：text-muted
```

#### 密码输入框
- **眼睛图标位置**：右侧内嵌，距右边12px
- **图标大小**：16px
- **图标颜色**：`--text-muted` 默认，`--primary-500` 悬停/激活
- **切换逻辑**：点击切换 type="password" / type="text"
- **背景**：白色或 `--bg-primary`

#### 登录专用输入框
- **高度**：40px
- **字号**：14px
- **圆角**：8px
- **边框**：`--border-medium`
- **占位符颜色**：`--text-muted`
- **间距**：输入框之间 16px-20px

### 7.3 卡片

#### 标准卡片
```
背景：bg-primary
边框：1px solid border-light
圆角：radius-lg (12px)
内边距：16px - 20px
阴影：shadow-card
悬停：shadow-md，translateY(-1px)
过渡：200ms ease
```

#### KPI 卡片（Hero）
```
最小高度：120px
左侧强调条：4px 宽，圆角
内边距：18px 20px
布局：左侧强调条 + 内容区
```

### 7.4 复选框

```
尺寸：16px x 16px
圆角：radius-sm (4px)
边框：1px solid border-medium

选中状态：
- 背景：primary-500
- 边框：primary-500
- 图标：白色对勾 ✓

悬停状态：
- 未选中：border-primary-400
- 已选中：primary-600

禁用状态：
- 背景：bg-tertiary
- 边框：border-light
```

#### 带文字的复选框
```
布局：flex 横向排列
间距：图标与文字之间 8px
文字：14px，--text-secondary
垂直对齐：居中
```

### 7.5 导航

#### 侧边栏导航
```
宽度：220px
背景：bg-primary
边框右侧：1px solid border-light

导航项：
- 内边距：9px 12px
- 圆角：radius-md
- 字体：13px，weight 500
- 图标：16px，右侧间距 10px

激活状态：
- 背景：primary-50
- 文字：primary-600，weight 600
- 左侧 3px 强调条
```

#### 顶部导航
```
高度：52px
背景：bg-primary
边框底部：1px solid border-light
内边距：0 28px
位置：sticky，top: 0
```

### 7.6 表格

```
表头背景：bg-secondary
表头字体：12px，weight 600，text-secondary，uppercase
单元格内边距：12px 16px
行分隔：1px solid border-light
行悬停：bg-secondary
选中行：primary-50

空状态：
- 居中显示
- 图标 + 描述文字
- 可选操作按钮
```

### 7.7 标签/徽章

```
高度：20px - 24px
内边距：2px 8px / 4px 12px
圆角：radius-full
字体：11px - 12px，weight 500

类型：
- 默认：bg-secondary，text-secondary，border-light
- 主色：primary-50，primary-600
- 成功：success-50，success-600
- 警告：warning-50，warning-600
- 错误：error-50，error-600
```

### 7.8 提示/alert

```
内边距：12px 16px
圆角：radius-md
边框左侧：3px solid
图标：16px，右侧间距 8px

类型：
- 信息：primary-50 背景，primary-500 边框
- 成功：success-50 背景，success-500 边框
- 警告：warning-50 背景，warning-500 边框
- 错误：error-50 背景，error-500 边框
```

### 7.9 模态框/抽屉

```
遮罩：rgba(0,0,0,0.5)
背景：bg-primary
圆角：radius-xl (16px)
阴影：shadow-lg
最大宽度：480px (小) / 640px (中) / 800px (大)

头部：
- 内边距：16px 20px
- 边框底部：border-light
- 标题：16px，weight 600

内容：
- 内边距：20px
- 最大高度：70vh
- 可滚动

底部：
- 内边距：12px 20px
- 边框顶部：border-light
- 按钮右对齐
```

---

## 8. 动效规范

### 8.1 过渡时间

```css
--transition-fast:   150ms ease;
--transition-normal: 200ms ease;
--transition-slow:   300ms ease;
```

### 8.2 常用动效

| 场景 | 时长 | 缓动函数 |
|------|------|----------|
| 按钮悬停 | 150ms | ease |
| 卡片悬停 | 200ms | ease |
| 下拉展开 | 200ms | ease-out |
| 模态框出现 | 300ms | cubic-bezier(0.16, 1, 0.3, 1) |
| Toast 出现/消失 | 300ms | ease-out |
| 页面切换 | 200ms | ease-in-out |

### 8.3 动效原则
- 微交互使用 150-200ms
- 页面级过渡使用 200-300ms
- 使用 transform 和 opacity（避免触发重排）
- 支持 prefers-reduced-motion 媒体查询

---

## 9. 图标规范

### 9.1 图标系统
- **图标库**：Lucide / Heroicons
- **风格**：线性描边，圆角端点
- **默认尺寸**：16px (小) / 20px (中) / 24px (大)
- **描边宽度**：1.5px - 2px

### 9.2 使用规则
- 导航图标：16px，与文字颜色一致
- 按钮图标：14px-16px，与文字颜色一致
- 空状态图标：48px-64px，text-muted 颜色
- 不允许使用 Emoji 作为功能图标

---

## 10. 布局规范

### 10.1 页面结构

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

### 10.2 响应式断点

| 断点 | 宽度 | 布局调整 |
|------|------|----------|
| Mobile | < 768px | 侧边栏收起为抽屉，单列布局 |
| Tablet | 768px - 1024px | 侧边栏可折叠，双列布局 |
| Desktop | 1024px - 1440px | 固定侧边栏，多列布局 |
| Large | > 1440px | 最大宽度 1440px，居中 |

### 10.3 内容区域

- **默认最大宽度**：无限制（适应屏幕）
- **推荐内容宽度**：1200px - 1440px
- **阅读区域宽度**：不超过 75ch（约 600px）

---

## 11. 表单规范

### 11.1 表单布局

```
标签 + 输入框（垂直布局，推荐）
内边距：8px 0
标签：12px，weight 500，text-secondary
输入框间距：16px
```

### 11.2 验证状态

| 状态 | 样式 |
|------|------|
| 默认 | border-medium |
| 焦点 | border-primary-400，阴影 |
| 错误 | border-error-500，error-50 背景 |
| 成功 | border-success-500（可选）|
| 禁用 | bg-tertiary，text-muted |

### 11.3 错误提示
```
位置：输入框下方
字体：12px，error-500
图标：16px alert 图标 + 8px 间距
间距：距输入框 4px
```

---

## 12. 数据可视化

### 12.1 图表颜色

```
主色序列：#2563EB → #60A5FA → #93C5FD → #BFDBFE
辅助色：#22C55E（正向）/ #EF4444（负向）/ #F97316（警告）
```

### 12.2 图表规范
- 使用圆角线条（stroke-linecap: round）
- 数据点使用清晰标记
- 提供图例说明
- 坐标轴标签使用 text-muted 颜色
- 网格线使用虚线，颜色 border-light

---

## 13. 可访问性规范

### 13.1 对比度要求
- 正文文本：≥ 4.5:1（AA 级）
- 大文本（18px+ 或 14px+ bold）：≥ 3:1
- 交互元素：≥ 3:1

### 13.2 焦点状态
- 所有可交互元素必须有可见焦点指示器
- 焦点环：2px solid primary-500，2px 偏移
- 键盘导航顺序与视觉顺序一致

### 13.3 触摸目标
- 最小触摸区域：44×44px
- 相邻触摸目标间距：≥ 8px

### 13.4 动画
- 支持 prefers-reduced-motion
- 关键动画时长 < 5 秒
- 无闪烁内容（< 3Hz）

---

## 14. 最佳实践

### 14.1 应该做的 ✅
- 使用语义化 HTML 标签
- 保持一致的间距和排版
- 为图标添加 aria-label
- 使用 loading 状态指示异步操作
- 提供清晰的错误反馈
- 使用骨架屏加载复杂内容

### 14.2 不应该做的 ❌
- 使用 Emoji 作为功能图标
- 依赖颜色作为唯一的信息传递方式
- 使用纯占位符作为标签
- 禁用浏览器的默认缩放
- 使用模糊的阴影或过度的装饰
- 混合多种设计风格

---

## 15. 登录页面设计规范

基于青阳云HR SaaS登录页实际设计，制定以下规范：

### 15.1 页面布局

```
┌─────────────────────────────────────────────────────┐
│  左侧品牌区 (50%)          │  右侧登录表单区 (50%)   │
│                            │                        │
│  ┌────────────────────┐   │  ┌──────────────────┐  │
│  │ Logo               │   │  │ 欢迎来到青阳云   │  │
│  │                    │   │  │ HR SaaS          │  │
│  │ 一站式人力资源     │   │  │                  │  │
│  │ 管理平台           │   │  │ 很高兴再次见到你 │  │
│  │                    │   │  │                  │  │
│  │                    │   │  │ [企业账号输入框] │  │
│  │                    │   │  │ [个人账号输入框] │  │
│  │                    │   │  │ [密码输入框  👁] │  │
│  │                    │   │  │                  │  │
│  │                    │   │  │ [✓] 记住密码     │  │
│  │                    │   │  │                  │  │
│  │                    │   │  │ [   登 录   ]    │  │
│  │                    │   │  │                  │  │
│  └────────────────────┘   │  └──────────────────┘  │
│                            │                        │
│  Copyright © 2015-2026     │                        │
│  备案信息链接              │                        │
└─────────────────────────────────────────────────────┘
```

### 15.2 登录表单规范

#### 标题样式
```css
.login-title {
    font-size: 24px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.3;
}

.login-subtitle {
    font-size: 14px;
    color: var(--text-muted);
    margin-top: 8px;
}
```

#### 输入框规范
```css
.login-input {
    height: 40px;
    padding: 0 12px;
    border: 1px solid var(--border-medium);
    border-radius: 8px;
    font-size: 14px;
    background: var(--bg-primary);
    
    &:focus {
        border-color: var(--primary-400);
        box-shadow: 0 0 0 3px var(--primary-100);
    }
    
    &::placeholder {
        color: var(--text-muted);
    }
}
```

#### 密码框眼睛图标
- 位置：输入框右侧内嵌
- 图标：眼睛睁开/闭上的状态切换
- 点击：切换密码可见性
- 颜色：`--text-muted` 默认，`--primary-500` 悬停

#### 登录按钮
```css
.login-btn {
    width: 100%;
    height: 44px;
    background: var(--primary-500);
    color: white;
    font-size: 16px;
    font-weight: 500;
    border-radius: 8px;
    border: none;
    
    &:hover {
        background: var(--primary-600);
    }
}
```

#### 记住密码
- 复选框：`--primary-500` 选中状态
- 文字：`--text-secondary`，14px
- 位置：密码框下方左侧

### 15.3 品牌区规范

- **Logo**：居中显示，宽度自适应
- **标语**："一站式人力资源管理平台"
  - 字号：20-24px
  - 颜色：白色或浅色
  - 字重：400-500
- **背景**：可使用品牌渐变色或抽象图案

### 15.4 页脚规范

- 版权信息：`Copyright © 2015-2026`
- 备案链接：下划线样式，`--text-muted` 颜色
- 字体：12px
- 位置：左下角

## 16. 文件模板

### 16.1 HTML/CSS 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>页面标题 - 青阳云</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            /* 引用上述 CSS 变量 */
        }
        
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-secondary);
            color: var(--text-primary);
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

## 附录

### A. 参考链接
- [Inter 字体](https://fonts.google.com/specimen/Inter)
- [Lucide 图标](https://lucide.dev/)
- [WCAG 2.1 指南](https://www.w3.org/WAI/WCAG21/quickref/)

### B. 更新日志
| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-04-02 | 初始版本 |
| v1.1 | 2026-04-03 | 新增登录页面设计规范（第15节）|

---

*本文档由 UI/UX Pro Max 技能辅助生成*