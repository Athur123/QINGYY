---
title: 青阳云 HRO 知识库首页
module: system
type: home
status: active
owner: athur
updated: 2026-05-16
source_of_truth: true
---

# 青阳云 HRO 知识库首页

> Obsidian Vault 入口。新人按 `CODE_WIKI.md` → 模块 README → 具体 spec/plan 顺序阅读。

## 模块导航

| 模块 | PRD | Specs | Plans |
|---|---|---|---|
| 对账复核 | [prd](superpowers/prd/reconciliation) | [specs](superpowers/specs/reconciliation) | [plans](superpowers/plans/reconciliation) |
| 结算方案 | — | [specs](superpowers/specs/settlement) | [plans](superpowers/plans/settlement) |
| 员工管理 | — | [specs](superpowers/specs/employee) | [plans](superpowers/plans/employee) |
| 险种配置 | — | [specs](superpowers/specs/insurance-config) | [plans](superpowers/plans/insurance-config) |
| 社保计算器 | — | [specs](superpowers/specs/calculator) | [plans](superpowers/plans/calculator) |
| 审批模板 | — | [specs](superpowers/specs/approval) | [plans](superpowers/plans/approval) |
| 系统/通用 | — | [specs](superpowers/specs/system) | [plans](superpowers/plans/system) |

## 操作手册

- [对账复核操作手册](manuals/reconciliation/user-manual.md)

## 参考资料
- [代码地图](CODE_WIKI.md)
- [Spec 变更指南](spec-change-guide.md)
- [设计 Token 参考](reference/design-tokens.md)
- [原型页面索引](reference/prototype-pages.md)
- [对账复核模块参考](reference/reconciliation-module.md)
- [社保政策数据库](reference/social-insurance-policy)
- [项目知识参考](reference/project-knowledge.md)

## 文档维护规则

- 新增或更新 `docs/HOME.md`、`docs/superpowers/specs/`、`docs/superpowers/plans/`、`docs/superpowers/prd/`、`docs/manuals/`、`docs/reference/` 下的 Markdown 文档时，必须按 Obsidian Markdown 规则维护 frontmatter。
- 更新正文、标题、状态、真源关系或链接时，同步更新 `updated`。
- 内部知识库链接优先使用相对 Markdown 链接或 Obsidian wikilink，不使用 `file:///` 本机绝对链接。
- 修改完成后运行校验：`python3 scripts/check_docs_frontmatter.py <changed-files>`。
- 提交前可运行：`python3 scripts/check_all.sh` 或 `python3 scripts/check_docs_frontmatter.py --staged`。

---

## Dataview 自动索引

> 需安装 Obsidian Dataview 插件才能渲染。给 spec/plan/PRD/HOME 的 frontmatter 添加 `title / module / type / status / owner / updated / source_of_truth` 字段后，下面的查询会自动生效。

### 进行中的 spec

```dataview
TABLE module, status, updated
FROM "superpowers/specs"
WHERE type = "spec" AND status != "done"
SORT updated DESC
```

### 最近更新的文档（30 天）

```dataview
TABLE module, type, status, updated
FROM "superpowers" OR "manuals" OR "reference"
WHERE updated >= date(today) - dur(30 days)
SORT updated DESC
LIMIT 20
```

### 按模块分组的 plan 完成度

```dataview
TABLE length(rows) AS 计划数, length(filter(rows.status, (s) => s = "done")) AS 已完成
FROM "superpowers/plans"
GROUP BY module
```

---

## Frontmatter 模板

新建 spec/plan 时建议使用：

```yaml
---
title: 对账复核主规格        # 必填：文档标题
module: reconciliation       # 必填：所属模块
type: spec                   # home | spec | plan | prd | guide | reference | note | decision | readme | adr | index
status: draft                # draft | active | deprecated | archived | done
owner: athur                 # 负责人
updated: 2026-05-16          # 最近修改日期，YYYY-MM-DD
source_of_truth: false       # 是否当前模块/主题真源
---
```
