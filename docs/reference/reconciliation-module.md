---
title: 对账复核模块参考
module: reconciliation
type: reference
status: active
owner: athur
updated: 2026-05-16
source_of_truth: prototype/reconciliation/
---

# 对账复核模块

对账复核是当前原型中较复杂的模块。

## 页面入口

| 页面 | 路径 |
|------|------|
| 汇总页 | `prototype/reconciliation/summary.html` |
| 明细页 | `prototype/reconciliation/unified.html` |

## 数据与交互

- **URL 参数**：`ruleName`、`month`、`groupId`
- **核心数据**：系统费用记录、台账记录、匹配结果、归档批次
- **关键交互**：页签切换、状态筛选、类型筛选、单条/批量操作、确认弹窗、右侧抽屉、归档批次筛选

修改该模块时重点关注汇总页与明细页之间的数据语义、状态流转和筛选逻辑一致性。

涉及确认、归档或匹配逻辑变更时运行：

```bash
python3 scripts/check_reconciliation_confirm_unification.py
```
