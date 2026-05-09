# 青阳云 HRO

**青阳云 (Qingyang Cloud)** 人力资源外包 (HRO) 管理系统的原型与设计系统仓库。

纯 HTML/CSS/JS 前端原型，无框架依赖，无需构建。用于快速验证业务流程和交互设计。

## 快速开始

```bash
git clone https://github.com/Athur123/QINGYY.git
cd QINGYY
python3 -m http.server 8080
```

浏览器打开 `http://localhost:8080/prototype/<模块>/<页面>.html`，例如：

- 对账复核汇总：`http://localhost:8080/prototype/reconciliation/summary.html`
- 对账复核明细：`http://localhost:8080/prototype/reconciliation/unified.html?ruleName=社保规则A&month=2026-04`
- 社保计算器：`http://localhost:8080/prototype/calculator/index.html`
- 员工详情：`http://localhost:8080/prototype/employee/detail.html`

> 必须从项目根目录启动服务，CSS 使用相对路径 `../../styles/`。

## 项目结构

```
├── prototype/                     # HTML 原型（41 页，7 个业务模块）
│   ├── reconciliation/            # 对账复核
│   ├── calculator/                # 社保方案计算
│   ├── employee/                  # 员工管理
│   ├── settlement/                # 结算方案
│   ├── insurance-config/          # 参保规则配置
│   ├── approval/                  # 审批管理
│   └── system/                    # 系统日志
├── styles/                        # 设计系统 CSS（变量/基础/组件/表单）
├── docs/superpowers/
│   ├── specs/                     # 设计文档（按模块分目录）
│   └── plans/                     # 实现计划（按模块分目录）
├── qingyang-hro-design-system.md  # 设计规范手册 v2.1
├── CLAUDE.md                      # Claude Code 项目指引
├── scripts/                       # 工具脚本
└── screenshots/                   # 测试截图（gitignored）
```

## 业务模块

| 模块 | 目录 | 说明 |
|------|------|------|
| 对账复核 | `reconciliation/` | 系统侧与社保局台账逐笔核对，支持导入、匹配、归档批次、强制核对 |
| 社保计算 | `calculator/` | 社保方案计算器、政策配置、公式识别、地区规则 |
| 员工管理 | `employee/` | 员工详情、异动采集、费用明细、档案版本 |
| 结算方案 | `settlement/` | 结算方案管理、费用分摊、预付款申请 |
| 参保配置 | `insurance-config/` | 规则向导、字段采集配置、全局字段管理 |
| 审批管理 | `approval/` | 审批模板管理 |
| 系统日志 | `system/` | 系统日志查看器 |

## 设计系统

命名规范：`qy-` 前缀 + BEM 风格（`.qy-btn--primary`、`.qy-card__header`）

| 资源 | 路径 |
|------|------|
| 设计规范手册 | `qingyang-hro-design-system.md` |
| CSS 变量 | `styles/qingyang-variables.css` |
| 基础样式 | `styles/qingyang-base.css` |
| 组件库 | `styles/qingyang-components.css` |
| 表单控件 | `styles/qingyang-forms.css` |
| 聚合版 | `styles/qingyang-design-system.css` |

主要设计令牌：

| Token | 值 | 用途 |
|-------|-----|------|
| `--qy-primary-500` | `#2563EB` | 主色 |
| `--qy-bg-secondary` | `#F8FAFC` | 页面背景 |
| `--qy-text-primary` | `#1E293B` | 正文 |
| `--qy-font-size-base` | `14px` | 正文字号 |
| `--qy-sidebar-width` | `220px` | 侧边栏宽度 |

## 技术栈

- **前端原型**：纯 HTML + CSS + 内联 JavaScript
- **设计系统**：CSS Custom Properties + BEM 命名
- **字体**：Plus Jakarta Sans（回退 Inter）
- **Excel 处理**：xlsx CDN 库
- **生产目标**：Vue 3 + TypeScript + Vite（Composition API）

## AI 辅助开发

本项目支持 Claude Code 和 Codex 双 AI 代理。入口文件：

- `CLAUDE.md` — Claude Code 项目指引
- `AGENTS.md` — Codex 项目指引

开发流程：brainstorming → spec → plan → implement，产出文档按模块归入 `docs/superpowers/`。

## License

Private — 内部项目
