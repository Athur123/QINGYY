# CLAUDE.md

本文件是 Claude Code 在本仓库工作的入口说明。请优先遵循这里的项目事实、协作偏好和目录约定。

## 安全注意事项

1. 本仓库没有 `package.json`，不要假设存在 npm 构建或测试命令。
2. `.claude/settings.local.json` 和 `.codex/config.toml` 可能包含真实凭据，禁止提交。
3. 只提交安全模板：`.claude/settings.local.example.json`、`.codex/config.example.toml`。
4. `.claude/worktrees/` 和 `.worktrees/` 是本地 worktree 快照，不属于主源码。
5. 提交前检查是否误改无关文件，尤其注意用户已有未提交改动。
6. 修改 `CLAUDE.md` 或 `AGENTS.md` 时，必须同步另一份文件中的共享项目事实，并检查两份文件是否仍然一致。

## 双 Agent 支持

本仓库同时支持 **Claude Code** 与 **Codex**。

- `CLAUDE.md` 是 Claude Code 入口；`AGENTS.md` 是 Codex 入口，共享项目事实应保持一致。
- Claude Code 配置：`.claude/`；技能：`.claude/skills/`；本机记忆：`.claude/memory/`。
- Codex 配置：`.codex/`；技能：`.agents/skills/`。
- 安全模板：`.claude/settings.local.example.json`、`.codex/config.example.toml`。

## 用户偏好

- 默认使用中文与用户沟通；即使用户使用英文提问，也优先用中文回答。
- 编写项目文档时默认使用中文，包括 specs、plans、PRD、README、交接说明、评审说明等。
- 专业术语、文件名、命令、代码标识、API 字段、框架名和产品名可以保留英文。
- 如果用户明确要求英文或双语输出，以用户当次要求为准。
- 执行代码改动前先读项目上下文，避免凭空重构；只修改与任务直接相关的文件。
- 工作区可能存在用户未提交改动，不要回退、覆盖或整理与当前任务无关的变更。

## 项目概览

本项目是 **青阳云（Qingyang Cloud）HRO** 原型与设计系统仓库，面向人力资源外包、派遣、结算、对账等业务场景。静态原型仓库，无 `package.json`，无前端构建流程。

主要内容：`prototype/`（HTML 原型）、`styles/`（设计系统 CSS/SCSS）、`docs/`（文档）、`.claude/skills/`（Claude 技能）、`scripts/`（工具脚本）。

## 关键目录

| 目录 | 用途 |
| --- | --- |
| `prototype/` | 静态 HTML 原型，按 7 个业务模块组织；从项目根目录启动服务预览 |
| `styles/` | 设计系统 CSS/SCSS |
| `docs/` | Code Wiki、PRD、specs、plans、manuals、reference；同时作为 Obsidian Vault 根目录 |
| `docs/reference/` | 设计 Token、原型页面索引、模块参考、共享项目知识等速查文档 |
| `docs/superpowers/specs/` | 设计规格，按模块存放 |
| `docs/superpowers/plans/` | 实施计划，按模块存放 |
| `scripts/` | 工具脚本和校验脚本 |
| `.claude/skills/` | Claude Code 技能 |
| `.claude/memory/` | Claude Code 本机记忆文件，不作为项目知识真源 |
| `.agents/skills/` | Codex 项目技能 |

## 设计系统

- 完整组件手册：`docs/reference/qingyang-hro-design-system.md`（v2.1）
- 组件说明：`styles/README.md`
- 设计 Token 速查：`docs/reference/design-tokens.md`
- 共享项目知识：`docs/reference/project-knowledge.md`

组件类名使用 `qy-` 前缀，接近 BEM 结构（`qy-btn`、`qy-card`、`qy-input`、`qy-table`、`qy-tag`）。

## 原型页面

预览：从项目根目录运行 `python3 -m http.server 8080`，访问 `http://localhost:8080/prototype/<module>/<page>.html`。

完整页面列表见 `docs/reference/prototype-pages.md`。

## Claude Code 技能

技能位于 `.claude/skills/`，用于自动化操作线上青阳云 HRO 系统。

| 技能 | 用途 | 常见触发 |
|------|------|----------|
| `qingyang-login` | 登录青阳云 | `登录青阳云`、`打开HRO`、`进入系统` |
| `qingyang-switch-hro` | 切换到 HRO 客户组织维度 | `切换到HRO`、`进入客户组织` |

凭据来源：`.claude/settings.local.json`（不提交，模板见 `.claude/settings.local.example.json`）。

## 开发与验证流程

较大需求采用 `brainstorming → spec → plan → implement` 节奏：

1. `brainstorming`：明确业务目标、约束、边界和验收标准。
2. `spec`：写入 `docs/superpowers/specs/<module>/<name>.md`。
3. `plan`：写入 `docs/superpowers/plans/<module>/<name>.md`。
4. `implement`：修改原型/样式/文档，浏览器验证。

### 校验命令

```bash
# 标准全量校验
./scripts/check_all.sh

# 设计系统校验
python3 scripts/check_design_system.py

# 对账复核逻辑校验（涉及确认/归档/匹配时）
python3 scripts/check_reconciliation_confirm_unification.py

# 文档 frontmatter 校验
python3 scripts/check_docs_frontmatter.py --strict
```

## 文档约定

- 新功能文档放入 `docs/superpowers/specs/<module>/`、`plans/<module>/`、`prd/<module>/`。
- 共享项目知识放入 `docs/reference/`；个人或工具私有记忆不放入项目文档。
- `docs/HOME.md` 是 Obsidian 知识库入口。
- `docs/` 下受管文档必须有 Obsidian frontmatter（`title`、`module`、`type`、`status`、`owner`、`updated`、`source_of_truth`），按 `obsidian-markdown` skill 规则维护。
- `type` 只使用：`home`、`spec`、`plan`、`prd`、`guide`、`reference`、`note`、`decision`、`readme`、`adr`、`index`。
- `status` 只使用：`draft`、`active`、`deprecated`、`archived`、`done`。
- 内部链接优先使用相对 Markdown 链接或 Obsidian wikilink，不新增 `file:///` 绝对链接。
- 原型使用原生 HTML、CSS 和内联 `<script>`，不引入框架或构建链。
- 可复用脚本放入 `scripts/`，一次性补丁脚本不放仓库根目录。
- `.claude/memory/` 是本机 agent 记忆，不作为项目真源；需要让 Codex/Claude 都自动读取的知识应迁入 `docs/`。

## 系统架构要点

青阳云 HRO 存在两个业务维度：**EHR**（核心人事，登录默认进入）和 **HRO**（外包/派遣客户组织，通过头像菜单切换）。

HRO 重点能力：上下游管理、结算方案、参保规则、费用计算、对账复核、审批与系统日志。

对账复核模块详情见 `docs/reference/reconciliation-module.md`。
