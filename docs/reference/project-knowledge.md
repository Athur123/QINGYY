---
title: 项目知识参考
module: system
type: reference
status: active
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 项目知识参考

本文件沉淀需要 Codex 与 Claude Code 共同读取的长期项目知识。个人偏好、工具运行缓存和 agent 私有记忆不放在这里。

## 用户偏好

- 默认使用中文与用户沟通；即使用户使用英文提问，也优先用中文回答。
- 编写项目文档时默认使用中文，包括 specs、plans、PRD、README、交接说明、评审说明等。
- 专业术语、文件名、命令、代码标识、API 字段、框架名和产品名可以保留英文。

## 技术栈偏好

- 生产方向偏好：Vue 3 + TypeScript + Vite + Composition API（`<script setup>`）。
- 当前仓库现状：静态原型仓库，无 `package.json`，无构建流程，使用原生 HTML、CSS 和内联 script。
- 不要在当前仓库中引入 Vue 或任何前端框架，除非用户明确要求进行生产化改造。

## 设计系统约定

- 设计系统入口：`styles/qingyang-design-system.css`。
- 组件类名前缀：`qy-`，接近 BEM 结构，例如 `qy-btn--primary`、`qy-card__header`。
- 主色：`#2563EB`。
- 背景：`#F8FAFC`。
- 主要文字：`#1E293B`。
- 默认正文：14px。
- 字体：Plus Jakarta Sans，回退 Inter 和 system-ui。

## 文件组织规范

所有产出按 7 个业务模块分目录：

| 模块 | 目录 |
|---|---|
| 对账复核 | `reconciliation/` |
| 社保计算 | `calculator/` |
| 员工管理 | `employee/` |
| 结算方案 | `settlement/` |
| 参保配置 | `insurance-config/` |
| 审批管理 | `approval/` |
| 系统/通用 | `system/` |

约定：

- 原型放入 `prototype/<module>/`。
- spec 放入 `docs/superpowers/specs/<module>/`。
- plan 放入 `docs/superpowers/plans/<module>/`。
- PRD 放入 `docs/superpowers/prd/<module>/`。
- 操作手册放入 `docs/manuals/<module>/`。
- 文件名使用短、稳定、有业务含义的英文名，不使用日期前缀。

## 设计检查清单

开发页面或组件时，至少确认：

- 不使用 emoji 作为正式图标，优先使用 SVG 或图标库图形。
- 交互元素有可见焦点环。
- 触摸目标建议不小于 44×44px。
- 动效应考虑 `prefers-reduced-motion`。
- Warning 橙色应搭配图标或文字，不只依赖颜色表达。
- 使用语义化颜色 token，避免新增硬编码色值。
- 禁用状态视觉清晰且不可交互。

## 对账复核模块要点

- 页面结构：汇总页 `prototype/reconciliation/summary.html`，明细页 `prototype/reconciliation/unified.html`。
- 当前主规格：`docs/superpowers/specs/reconciliation/type-month-matching.md`。
- 当前 PRD：`docs/superpowers/prd/reconciliation/reconciliation.md`。
- 账单月份是页面上下文，不用于减少汇总页主体/规则清单。
- 系统侧与台账侧通过统一“确认核对”抽屉处理一对一、一对多、多对一、多对多。
- 系统侧强制核对是兜底能力，不作为单行高频操作。
- 归档批次与已付款状态用于结果追溯，已归档或已付款记录不可取消核对。

## Agent 记忆策略

- 共享项目知识应写入 `docs/`，优先放在 `docs/reference/`、模块 spec、PRD 或操作手册中。
- `.claude/memory/`、`.codex/` 和其他 agent 本地状态只作为本机工具记忆，不作为项目真源。
- 修改规则、偏好、项目结构后，应同步更新 `AGENTS.md`、`CLAUDE.md` 和相关 `docs/` 文档。
