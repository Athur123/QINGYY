# AGENTS.md

本文件是 Codex 在本仓库工作的入口说明。请优先遵循这里的项目事实、协作偏好和目录约定。

## 双 Agent 支持

本仓库从项目根目录同时支持 **Codex** 与 **Claude Code**。

- `AGENTS.md` 是 Codex 入口文件。
- `CLAUDE.md` 是 Claude Code 入口文件。
- 两份文件中的共享项目事实应保持一致。
- Codex 本地配置放在 `.codex/`。
- Claude Code 本地配置放在 `.claude/`。
- Codex 项目技能放在 `.agents/skills/`。
- Claude Code 技能放在 `.claude/skills/`。
- 安全配置模板放在 `.codex/config.example.toml` 和 `.claude/settings.local.example.json`。

## 用户偏好

- 默认使用中文与用户沟通；即使用户使用英文提问，也优先用中文回答。
- 编写项目文档时默认使用中文，包括 specs、plans、PRD、README、交接说明、评审说明等。
- 专业术语、文件名、命令、代码标识、API 字段、框架名和产品名可以保留英文。
- 如果用户明确要求英文或双语输出，以用户当次要求为准。
- 执行代码改动前先读项目上下文，避免凭空重构；只修改与任务直接相关的文件。
- 工作区可能存在用户未提交改动，不要回退、覆盖或整理与当前任务无关的变更。

## 项目概览

本项目是 **青阳云（Qingyang Cloud）HRO** 原型与设计系统仓库，面向人力资源外包、派遣、结算、对账等业务场景。

这是一个静态原型仓库，没有 `package.json`，也没有前端构建流程。主要内容包括：

1. `prototype/`：按业务模块组织的 HTML 原型页面。
2. `styles/`：青阳云设计系统 CSS/SCSS。
3. `docs/`：Code Wiki、PRD、specs、plans、SQL 草案等文档。
4. `.agents/skills/`：Codex 使用的青阳云自动化技能。
5. `.claude/`：Claude Code 相关技能、记忆和本地配置。
6. `scripts/`：Markdown 转 PDF、记忆维护、校验脚本、Git hook 等工具。

## 关键目录

| 目录 | 用途 |
| --- | --- |
| `prototype/` | 静态 HTML 原型页面，按 7 个业务模块组织；从项目根目录启动服务预览 |
| `styles/` | 设计系统 CSS/SCSS 文件 |
| `docs/` | Code Wiki、PRD、specs、plans、SQL 草案 |
| `docs/superpowers/specs/` | 设计规格文档，按模块存放 |
| `docs/superpowers/plans/` | 实施计划文档，按模块存放 |
| `docs/superpowers/sql/` | 数据库迁移或 SQL 草案 |
| `scripts/` | 工具脚本和校验脚本 |
| `README.md` | 面向新协作者的快速入口 |
| `.agents/skills/` | Codex 项目技能 |
| `.codex/` | Codex 本地配置，可能包含敏感信息，不要提交真实配置 |
| `.claude/skills/` | Claude Code 技能，保留用于跨工具兼容 |
| `.claude/memory/` | Claude Code 记忆文件 |

## 设计系统

设计系统主要由以下文档和样式文件维护：

- `qingyang-hro-design-system.md`：完整组件手册，当前为 v2.1。
- `styles/README.md`：组件与使用说明文档。

### 核心设计 Token

- 主色：`--qy-primary-500` = `#2563EB`
- 页面背景：`--qy-bg-secondary` = `#F8FAFC`
- 主文本：`--qy-text-primary` = `#1E293B`
- 次级文本：`--qy-text-secondary` = `#64748B`
- 浅边框：`--qy-border-light` = `#E2E8F0`
- 字体：Plus Jakarta Sans、Inter、system-ui、sans-serif
- 默认正文：14px

### CSS 入口规则

`styles/` 下的样式文件分为拆分入口和聚合入口：

- 拆分入口：`qingyang-variables.css`、`qingyang-base.css`、`qingyang-components.css`、`qingyang-forms.css`
- 聚合入口：`qingyang-design-system.css`
- SCSS 版本：`qingyang-variables.scss`

同一个 HTML 页面不要同时混用拆分入口和聚合入口。新增或维护样式时遵循以下归属：

1. 设计变量写入 `qingyang-variables.css`。
2. 基础样式和工具类写入 `qingyang-base.css`。
3. 通用组件写入 `qingyang-components.css`。
4. 表单控件写入 `qingyang-forms.css`。
5. 如果维护聚合入口，确保它与拆分入口语义一致。

### 组件命名

组件类名使用 `qy-` 前缀，并采用接近 BEM 的结构。

- `qy-btn`：按钮，常见变体包括 `--primary`、`--secondary`、`--text`、`--danger`。
- `qy-card`：卡片，常见元素包括 `__header`、`__body`、`__footer`。
- `qy-input`：输入框。
- `qy-table`：数据表格。
- `qy-tag`：标签或状态标识。

## 原型页面

原型页面位于 `prototype/`，按业务模块拆分。预览时必须从项目根目录启动静态服务，确保 `../../styles/` 这类 CSS 路径能够正确解析。

```bash
python3 -m http.server 8080
```

访问示例：

```text
http://localhost:8080/prototype/reconciliation/summary.html
```

| 模块 | 目录 | 主要页面 |
| --- | --- | --- |
| 对账复核 | `prototype/reconciliation/` | `summary.html`、`unified.html` |
| 社保计算 | `prototype/calculator/` | `index.html`、`policy.html`、`region-rules.html`、`sub-account.html`、`formula-recognition.html` |
| 员工管理 | `prototype/employee/` | `detail.html`、`change-field.html`、`cost-detail.html`、`archive-version.html` |
| 结算方案 | `prototype/settlement/` | `plan.html`、`detail.html`、`cost-attribution.html`、`cost-allocation.html` |
| 参保配置 | `prototype/insurance-config/` | `stepper.html`、`field-collection.html`、`global-field.html` |
| 审批管理 | `prototype/approval/` | `template-management.html` |
| 系统 | `prototype/system/` | `log-viewer.html`、`sys-log.html` |

旧版本原型可以保留在相同模块目录中，但新页面命名应短、稳定、有业务含义，不使用日期前缀。

## Codex 技能

Codex 项目技能位于 `.agents/skills/`，用于自动化操作线上青阳云 HRO 系统。Claude Code 对应技能保留在 `.claude/skills/`，用于跨工具兼容。

### 可用技能

**`qingyang-login`**

- 用途：登录青阳云。
- 地址：`https://qingyangyun.com.cn/#/login`
- 凭据来源：`.codex/config.toml` 中的本地环境变量。
- 常见触发：`登录青阳云`、`打开HRO`、`进入系统`、`帮我登录`。

**`qingyang-switch-hro`**

- 用途：从 EHR 维度切换到 HRO 客户组织维度。
- 入口：用户头像下拉菜单中的 `切换客户组织`。
- 常见触发：`切换到HRO`、`进入客户组织`、`HRO维度`、`上下游管理`。

### Codex 本地环境变量

真实值只放在 `.codex/config.toml`，不要提交。安全模板见 `.codex/config.example.toml`。

```toml
[shell_environment_policy]
inherit = "core"

[shell_environment_policy.set]
QINGYANG_LOGIN_URL = "https://qingyangyun.com.cn/#/login"
QINGYANG_TENANT = "zjhcrl"
QINGYANG_USERNAME = "admin"
QINGYANG_PASSWORD = "<redacted>"
```

## 开发与验证流程

### 本地预览

从项目根目录启动服务：

```bash
python3 -m http.server 8080
```

然后访问：

```text
http://localhost:8080/prototype/<module>/<page>.html
```

原型页面通常位于 `prototype/<module>/` 二级目录，CSS 引用多为 `../../styles/`，因此不要从子目录启动静态服务。

### 浏览器验证

涉及视觉、交互或布局变化时，使用 Playwright 或 Codex Browser 打开本地页面验证。

典型流程：

```text
1. 在项目根目录运行 python3 -m http.server 8080
2. 打开 http://localhost:8080/prototype/reconciliation/summary.html
3. 检查页面是否加载样式、布局是否异常
4. 对关键按钮、筛选、抽屉、弹窗等交互做基本验证
5. 如需截图，保存到 screenshots/，不要放在项目根目录
```

测试产物目录包括 `.playwright-mcp/` 和 `screenshots/`，均为本地临时产物，通常不需要提交。

### 设计系统校验

修改设计系统或原型样式引用后，优先运行：

```bash
python3 scripts/check_design_system.py
```

如果改动涉及对账复核的确认、归档或匹配逻辑，再运行：

```bash
python3 scripts/check_reconciliation_confirm_unification.py
```

## 文档与实现约定

- 新功能文档优先放入对应模块目录：`docs/superpowers/specs/<module>/`、`docs/superpowers/plans/<module>/`、`docs/superpowers/prd/<module>/`。
- `docs/` 同时作为 Obsidian Vault 根目录，`docs/HOME.md` 是知识库入口。
- 新增或更新 `docs/HOME.md`、`docs/superpowers/specs/`、`docs/superpowers/plans/`、`docs/superpowers/prd/` 下的 Markdown 文件时，必须按 `obsidian-markdown` skill 规则检查和维护 Obsidian frontmatter。
- 上述文档的 frontmatter 至少包含：`title`、`module`、`type`、`status`、`owner`、`updated`、`source_of_truth`。
- `type` 只使用：`home`、`spec`、`plan`、`prd`、`guide`、`reference`、`note`、`decision`、`readme`、`adr`、`index`。
- `status` 只使用：`draft`、`active`、`deprecated`、`archived`、`done`。
- `updated` 使用 `YYYY-MM-DD`，并在正文、标题、状态、真源关系或链接发生实质更新时同步更新。
- 文档内部链接优先使用相对 Markdown 链接或 Obsidian wikilink；不要新增 `file:///` 本机绝对链接。
- 修改上述文档后运行 `python3 scripts/check_docs_frontmatter.py <changed-files>`；提交前可运行 `python3 scripts/check_docs_frontmatter.py --staged`。
- 如需启用本地 Git 提交拦截，运行 `scripts/install-git-hooks.sh`，它会安装 pre-commit 文档校验和现有 post-commit memory 更新 hook。
- 原型新增页面放入 `prototype/<module>/`。
- 一次性本地补丁脚本不要放在仓库根目录；可复用脚本放入 `scripts/`。
- 项目原型使用原生 HTML、CSS 和内联 `<script>`，不要无故引入框架或构建链。
- 原型中的后端/API 多为 mock；真实后端设计主要沉淀在 `docs/superpowers/`。
- 生产方向偏好为 Vue 3 + TypeScript + Vite + Composition API，但本仓库当前不承载生产构建。

## 系统架构要点

青阳云 HRO 系统存在两个业务维度：

- EHR：核心人事维度，登录后通常默认进入。
- HRO：外包/派遣客户组织维度，需要通过头像菜单切换。

HRO 重点能力包括上下游管理、结算方案、参保规则、费用计算、对账复核、审批与系统日志。

### 对账复核模块

对账复核是当前原型中较复杂的模块：

- 汇总页：`prototype/reconciliation/summary.html`
- 明细页：`prototype/reconciliation/unified.html`
- 常见跳转：通过 URL 参数传递 `ruleName`、`month` 或 `groupId`
- 核心数据：系统费用记录、台账记录、匹配结果、归档批次
- 关键交互：页签切换、状态筛选、类型筛选、单条/批量操作、确认弹窗、右侧抽屉、归档批次筛选

修改该模块时要重点关注汇总页与明细页之间的数据语义、状态流转和筛选逻辑一致性。

## 重要注意事项

1. 本仓库没有 `package.json`，不要假设存在 npm 构建或测试命令。
2. `.codex/config.toml` 和 `.claude/settings.local.json` 可能包含真实凭据，禁止提交。
3. 只提交安全模板：`.codex/config.example.toml`、`.claude/settings.local.example.json`。
4. `.claude/worktrees/` 和 `.worktrees/` 是本地 worktree 快照，不属于主源码。
5. 测试截图放入 `screenshots/`；不要把截图或临时 PNG 放在项目根目录。
6. 提交前检查是否误改无关文件，尤其注意用户已有未提交改动。
7. 修改 `AGENTS.md` 或 `CLAUDE.md` 时，尽量同步另一份文件中的共享项目事实。
