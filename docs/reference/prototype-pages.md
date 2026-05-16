---
title: 原型页面索引
module: prototype
type: reference
status: active
owner: athur
updated: 2026-05-16
source_of_truth: prototype/
---

# 原型页面索引

预览命令（从项目根目录）：

```bash
python3 -m http.server 8080
```

访问：`http://localhost:8080/prototype/<module>/<page>.html`

## 页面列表

| 模块 | 目录 | 主要页面 |
| --- | --- | --- |
| 对账复核 | `prototype/reconciliation/` | `summary.html`、`unified.html` |
| 社保计算 | `prototype/calculator/` | `index.html`、`policy.html`、`region-rules.html`、`sub-account.html`、`formula-recognition.html` |
| 员工管理 | `prototype/employee/` | `detail.html`、`change-field.html`、`cost-detail.html`、`archive-version.html` |
| 结算方案 | `prototype/settlement/` | `plan.html`、`detail.html`、`cost-attribution.html`、`cost-allocation.html` |
| 参保配置 | `prototype/insurance-config/` | `stepper.html`、`field-collection.html`、`global-field.html` |
| 审批管理 | `prototype/approval/` | `template-management.html` |
| 系统 | `prototype/system/` | `log-viewer.html`、`sys-log.html` |

旧版本原型可保留在同模块目录，新页面命名应短、稳定、有业务含义，不使用日期前缀。
