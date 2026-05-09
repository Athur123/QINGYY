---
name: 青阳云HRO项目概况
description: 青阳云HRO人力资源管理系统项目信息，包含规范文档和CSS库路径
type: project
---

- **规范文档**: `qingyang-hro-design-system.md` (v2.0)
- **CSS库**: `styles/qingyang-design-system.css`
- **命名规范**: `qy-` 前缀，BEM 规范（`.qy-btn--primary`, `.qy-card__header`）
- **色彩**: 主色 `#2563EB`，背景 `#F8FAFC`，文字 `#1E293B`
- **字体**: 14px 正文，Plus Jakarta Sans（回退 Inter）
- **变量前缀**: 所有 CSS 变量使用 `--qy-`
- **布局方案**: flex 布局，`.qy-main { flex: 1; margin-left: 0 }`（非 margin-left 偏移）

## 文件组织规范

所有产出按 7 个业务模块分目录：

| 模块 | 目录 |
|------|------|
| 对账复核 | `reconciliation/` |
| 社保计算 | `calculator/` |
| 员工管理 | `employee/` |
| 结算方案 | `settlement/` |
| 参保配置 | `insurance-config/` |
| 审批管理 | `approval/` |
| 系统日志 | `system/` |

**约定**：原型→`prototype/<模块>/`，CSS 引用 `../../styles/`；spec→`docs/superpowers/specs/<模块>/`；plan→`docs/superpowers/plans/<模块>/`。文件名用业务含义短名称，不加日期前缀。

## 社保对账复核

- **两层结构**: 汇总列表（`reconciliation/summary.html`）+ 明细核对（`reconciliation/unified.html`）
- **核对状态机**: UNMATCHED → MATCHED / PENDING / DIFF，MATCHED 可归档（`archived=true`），归档后可付款（PAID，spec 已定义）
- **归档批次**: 同一账单月份可多次归档，每次生成新批次（`archiveBatches[]`），记录归属到批次（`archiveBatchId`）
- **强制核对**: DIFF/UNMATCHED 可直接标记为 MATCHED（仅系统侧可用，台账侧不允许）
- **核心 spec**: `docs/superpowers/specs/reconciliation/type-month-matching.md`

## 文档历史
- v3.0 (2026-05-09): 目录按模块重组、归档批次、PAID 状态、flex 布局方案
- v2.1 (2026-04-30): 新增社保对账复核模块知识
- v2.0 (2026-04-28): 合并 guidelines + design-system 为单一文档