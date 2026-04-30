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

## 社保对账复核
- **核心矛盾**：系统有费用类型无应缴月份（补缴/调基补差），台账有应缴月份无费用类型。双方共同拥有：身份证、险种、金额。
- **匹配算法**：按 `身份证|险种|应缴月份` 分组 → 按金额精确配对 → 1:1自动匹配，多笔同金额标记待确认
- **核对状态**：UNMATCHED → MATCHED / PENDING / DIFF → ARCHIVED
- **UI模式**：Tab 切换（系统侧/台账侧），各自独立筛选+统计，已核对记录双向展示带跨引用
- **特殊规则**：补缴/调基补差台账无匹配 → 未匹配（非差异，可后续月份继续匹配）；汇缴台账无匹配 → 差异
- **险种映射**：支持别名标准化（如"基本养老保险"→"养老"），含大额医疗
- **原型文件**：`prototype/qingyang-reconciliation-unified.html`
- **设计文档**：`docs/superpowers/specs/2026-04-29-reconciliation-type-month-matching-design.md`

## 文档历史
- v2.1 (2026-04-30): 新增社保对账复核模块知识
- v2.0 (2026-04-28): 合并 guidelines + design-system 为单一文档，统一 `--qy-` 前缀
- 原 `qingyang-ui-ux-guidelines.md` 已删除