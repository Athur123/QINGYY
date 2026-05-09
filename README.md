# 青阳云 HRO 原型仓库

这是一个面向青阳云 HRO 场景的原型与设计资产仓库，不是生产应用代码仓库。

## 仓库包含什么

- `prototype/`：按业务模块拆分的静态 HTML 原型
- `styles/`：设计系统 CSS / SCSS
- `docs/superpowers/specs/`：按模块拆分的设计规格
- `docs/superpowers/plans/`：按模块拆分的实施计划
- `scripts/`：仓库级辅助脚本
- `.agents/skills/`：Codex 项目技能
- `.claude/skills/`：Claude 项目技能

## 当前模块结构

- `approval/`
- `calculator/`
- `employee/`
- `insurance-config/`
- `reconciliation/`
- `settlement/`
- `system/`

## 建议阅读顺序

1. `CLAUDE.md` 或 `AGENTS.md`
2. `docs/CODE_WIKI.md`
3. `styles/README.md`
4. 目标模块的 `prototype/<module>/`
5. 对应 `docs/superpowers/specs/<module>/`
6. 对应 `docs/superpowers/plans/<module>/`

## 当前主线

当前最完整、最适合作为参考样板的模块是 `reconciliation/`：

- `prototype/reconciliation/summary.html`
- `prototype/reconciliation/unified.html`
- `docs/superpowers/specs/reconciliation/reconciliation-design.md`
- `docs/superpowers/plans/reconciliation/archive-batch.md`

## 本地预览

从项目根目录启动：

```bash
python3 -m http.server 8080
```

然后访问：

```text
http://localhost:8080/prototype/<module>/<page>.html
```
