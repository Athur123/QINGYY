---
name: memory-keeper
description: 自动分析项目变更并更新 memory 系统
---

# Memory Keeper

## 触发条件

当用户完成以下操作后调用此 skill：
- 提交了新的 commit
- 修改了原型页面、样式、设计文档
- 需要整理或检索项目知识

## 工作流程

### 1. 分析变更范围

运行 `scripts/update-memory.sh` 获取变更摘要。

### 2. 判断变更类型

根据变更文件路径，判断属于哪类知识：

| 路径模式 | 知识类型 | 目标 memory 文件 |
|---------|---------|----------------|
| `prototype/employee-*` | 员工管理 | `memory/business_employee.md` |
| `prototype/settlement-*` | 结算方案 | `memory/business_settlement.md` |
| `prototype/approval-*` | 审批模板 | `memory/business_approval.md` |
| `prototype/*insurance*` / `prototype/*rule*` | 险种/参保规则 | `memory/business_insurance_types.md` |
| `prototype/*policy*` | 社保政策 | `memory/business_social_insurance.md` |
| `styles/*` | 前端组件架构 | `memory/architecture_frontend.md` |
| `docs/superpowers/sql/*` | 数据结构 | `memory/architecture_data_models.md` |
| `docs/superpowers/specs/*` | 设计规格 | 更新 `MEMORY.md` 索引 |
| `docs/superpowers/plans/*` | 实现计划 | 更新 `MEMORY.md` 索引 |
| `CLAUDE.md` | 项目概述 | `memory/project_overview.md` |

### 3. 提取知识

对每个变更文件：
- 如果文件是 **新增** 的功能/页面/组件，创建或更新对应 memory 文件
- 如果文件是 **修改** 已有功能，更新对应 memory 文件中的描述
- 如果文件是 **删除**，从 memory 中移除相关内容

### 4. 更新索引

更新 `MEMORY.md` 中的变更记录段，添加新的变更摘要行。

## 知识提取规则

- **只记录非显而易见的信息**：代码能直接看出的不记
- **记录 WHY 而非 WHAT**：动机、约束、决策原因
- **保持简洁**：每个 memory 文件控制在 50 行以内
- **定期清理**：超过 30 天的变更记录自动归档

## 检索方式

当用户询问项目相关问题时：
1. 先读 `MEMORY.md` 获取索引
2. 根据关键词匹配 memory 文件名
3. 读取相关 memory 文件
4. 如需更详细信息，用 Grep 在 `docs/` 和 `prototype/` 中搜索