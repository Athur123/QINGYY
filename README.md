# 青阳云 HRO 原型仓库

这是青阳云 HRO 的静态原型、设计系统与产品文档仓库。它用于沉淀业务原型、规格说明、PRD、计划、操作手册和协作规则，不是生产应用代码仓库。

## 快速入口

- 项目知识库入口：[docs/HOME.md](docs/HOME.md)
- 代码与结构说明：[docs/CODE_WIKI.md](docs/CODE_WIKI.md)
- 原型浏览入口：[prototype/index.html](prototype/index.html)
- 原型页面索引：[docs/reference/prototype-pages.md](docs/reference/prototype-pages.md)
- 项目知识说明：[docs/reference/project-knowledge.md](docs/reference/project-knowledge.md)
- 设计系统手册：[docs/reference/qingyang-hro-design-system.md](docs/reference/qingyang-hro-design-system.md)

## 主要目录

| 目录 | 用途 |
| --- | --- |
| `prototype/` | 按业务模块组织的静态 HTML 原型 |
| `styles/` | 青阳云 HRO 设计系统 CSS / SCSS |
| `docs/` | Obsidian 知识库、规格、PRD、计划、操作手册和参考资料 |
| `docs/superpowers/specs/` | 当前有效的模块规格说明 |
| `docs/superpowers/prd/` | 面向研发和测试的 PRD |
| `docs/superpowers/plans/` | 实施计划、交接计划和任务拆解 |
| `docs/manuals/` | 面向最终用户的操作手册 |
| `scripts/` | 文档检查、原型检查和辅助脚本 |
| `.agents/skills/` | Codex 项目技能 |
| `.claude/skills/` | Claude Code 项目技能 |

## 本地预览

从项目根目录启动静态服务：

```bash
python3 -m http.server 8080
```

然后访问：

```text
http://localhost:8080/prototype/index.html
http://localhost:8080/prototype/<module>/<page>.html
```

注意：原型通常位于 `prototype/<module>/` 下，样式路径依赖从项目根目录提供静态服务，不建议直接用浏览器打开本地 HTML 文件。

## 当前参考模块：对账复核

对账复核是当前最完整、最适合作为新模块参考的样板模块。

- 汇总页原型：[prototype/reconciliation/summary.html](prototype/reconciliation/summary.html)
- 明细页原型：[prototype/reconciliation/unified.html](prototype/reconciliation/unified.html)
- 主规格：[docs/superpowers/specs/reconciliation/type-month-matching.md](docs/superpowers/specs/reconciliation/type-month-matching.md)
- PRD：[docs/superpowers/prd/reconciliation/reconciliation.md](docs/superpowers/prd/reconciliation/reconciliation.md)
- 完整计划：[docs/superpowers/plans/reconciliation/v1-complete-plan.md](docs/superpowers/plans/reconciliation/v1-complete-plan.md)
- 研发测试交接计划：[docs/superpowers/plans/reconciliation/development-test-handoff.md](docs/superpowers/plans/reconciliation/development-test-handoff.md)
- 最终用户操作手册：[docs/manuals/reconciliation/user-manual.md](docs/manuals/reconciliation/user-manual.md)

## 常用校验

仓库提供统一检查脚本：

```bash
./scripts/check_all.sh
```

如只检查 Markdown frontmatter，可运行：

```bash
python3 scripts/check_docs_frontmatter.py docs
```

## 协作入口

- Codex 工作入口：[AGENTS.md](AGENTS.md)
- Claude Code 工作入口：[CLAUDE.md](CLAUDE.md)
- 本仓库同时支持 Codex 与 Claude Code。共享规则应保持两份入口文件一致，工具私有配置分别放在 `.codex/` 和 `.claude/` 下。

## 文档约定

- `docs/` 已作为 Obsidian vault 使用，新增或更新 specs、PRD、plan、manual、HOME 类文档时应保留 frontmatter。
- 文档默认使用中文，专业术语可保留英文。
- 这是原型仓库，不应新增数据库设计目录或生产后端实现目录。
