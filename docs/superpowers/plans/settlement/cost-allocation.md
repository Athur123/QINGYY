---
title: 员工调动后费用归属调整 — 实现计划
module: settlement
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 员工调动后费用归属调整 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为青阳云HRO系统创建"员工调动后费用归属调整"功能的数据库迁移脚本、API接口设计文档和业务逻辑文档，与已有的HTML原型配合形成完整的设计交付物。

**Architecture:** 本仓库为设计先行原型仓库，不包含实际后端代码。计划产出：
1. SQL迁移脚本 — 新增费用调整日志表 `cost_adjustment_log`，记录每次重算操作的明细
2. API接口设计文档 — 定义检测、预览、重算三个核心接口的请求/响应格式
3. 业务逻辑文档 — 描述检测引擎的6个触发场景与重算拆分算法

**Tech Stack:** MySQL DDL/DML（与现有 `2026-04-25-settlement-entity-migration.sql` 兼容），Markdown API spec

**前置依赖:** 
- `employee_archive_version` 表（2026-04-25迁移已创建）
- `settlement_history` 表（2026-04-25迁移已创建）
- `bill` / `bill_detail` 表（2026-04-25迁移已创建）
- `cost_detail` 表的 snapshot 字段（2026-04-25迁移已添加）
- HTML原型 `insurance-cost-allocation.html` / `employee-cost-detail.html`（已创建）

---

## 文件清单

| 文件 | 操作 | 职责 |
|------|------|------|
| `docs/superpowers/sql/2026-04-28-cost-adjustment-migration.sql` | 创建 | 费用调整日志表 DDL + 回滚脚本 |
| `docs/superpowers/specs/2026-04-28-cost-adjustment-api-design.md` | 创建 | API 接口设计：检测、预览、重算三组接口 |
| `docs/superpowers/specs/2026-04-28-cost-adjustment-business-logic.md` | 创建 | 业务逻辑文档：检测引擎规则 + 重算拆分算法 |

---

### Task 1: 数据库迁移脚本 — 费用调整日志表

**Files:**
- Create: `docs/superpowers/sql/2026-04-28-cost-adjustment-migration.sql`

- [ ] **Step 1: 创建 migration 文件，写入文件头和 `cost_adjustment_log` 表 DDL**

```sql
-- ============================================================
-- 员工调动后费用归属调整 - 数据库迁移脚本
-- 日期：2026-04-28
-- 说明：创建费用调整日志表，记录每次重算操作的明细
-- 前置依赖：employee_archive_version, bill, bill_detail, cost_detail
-- ============================================================

-- ============================================================
-- 费用调整日志表
-- 记录因员工调动、政策调整等触发的费用归属调整操作
-- 每次重算生成一条主记录，明细存储拆分结果
-- ============================================================
CREATE TABLE IF NOT EXISTS `cost_adjustment_log` (
    `log_id` BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '日志ID',
    `employee_id` BIGINT NOT NULL COMMENT '员工ID',
    `trigger_type` VARCHAR(50) NOT NULL COMMENT '触发类型：transfer-调动/重新入职, policy_change-政策调整, manual_backpay-手动补缴, retroactive_enroll-追溯参保, retroactive_approval-审批生效日不一致, rehire_no_stop-离职未停保',
    `bill_month` VARCHAR(7) NOT NULL COMMENT '费用月份（YYYY-MM）',
    `old_settlement_entity_id` BIGINT DEFAULT NULL COMMENT '调整前结算主体',
    `new_settlement_entity_id` BIGINT NOT NULL COMMENT '调整后结算主体',
    `old_customer_id` BIGINT DEFAULT NULL COMMENT '调整前客户',
    `new_customer_id` BIGINT DEFAULT NULL COMMENT '调整后客户',
    `old_project_id` BIGINT DEFAULT NULL COMMENT '调整前项目',
    `new_project_id` BIGINT DEFAULT NULL COMMENT '调整后项目',
    `amount` DECIMAL(10,2) NOT NULL DEFAULT 0.00 COMMENT '涉及金额',
    `status` VARCHAR(20) NOT NULL DEFAULT 'pending' COMMENT '状态：pending-待处理, recalculated-已重算, failed-失败',
    `fail_reason` VARCHAR(512) DEFAULT NULL COMMENT '失败原因',
    `original_bill_id` BIGINT DEFAULT NULL COMMENT '原账单ID',
    `new_bill_id` BIGINT DEFAULT NULL COMMENT '新账单ID（拆分后）',
    `archive_version_id` BIGINT DEFAULT NULL COMMENT '触发时的档案版本号',
    `annotated_original_entity` VARCHAR(128) DEFAULT NULL COMMENT '标注的原归属信息（用于场景四：追溯参保）',
    `operator_id` BIGINT DEFAULT NULL COMMENT '操作人',
    `processed_at` TIMESTAMP NULL DEFAULT NULL COMMENT '处理时间',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX `idx_employee` (`employee_id`),
    INDEX `idx_status` (`status`),
    INDEX `idx_trigger_type` (`trigger_type`),
    INDEX `idx_bill_month` (`bill_month`),
    INDEX `idx_settlement` (`new_settlement_entity_id`, `bill_month`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='费用调整日志表';
```

- [ ] **Step 2: 追加回滚脚本**

```sql
-- ============================================================
-- 回滚脚本（迁移失败时使用）
-- ============================================================

DROP TABLE IF EXISTS `cost_adjustment_log`;
```

- [ ] **Step 3: 提交**

```bash
git add docs/superpowers/sql/2026-04-28-cost-adjustment-migration.sql
git commit -m "feat: 新增费用调整日志表 cost_adjustment_log"
```

---

### Task 2: API 接口设计

**Files:**
- Create: `docs/superpowers/specs/2026-04-28-cost-adjustment-api-design.md`

- [ ] **Step 1: 创建 API 设计文档，写入以下接口定义**

```markdown
# 费用归属调整 — API 接口设计

> 日期：2026-04-28
> 关联设计：`2026-04-28-employee-transfer-cost-allocation-design.md`

## 接口 1: 检测待调整事项

### GET `/api/insurance/cost-allocation/adjustments`

**说明:** 检测所有因员工归属变更影响的未归档账单，返回待处理列表。

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 否 | 筛选状态：`pending` / `processed`，默认 `pending` |
| billMonth | string | 否 | 筛选月份（YYYY-MM） |
| settlementEntityId | number | 否 | 筛选结算主体 |

**响应:**

```json
{
  "code": 0,
  "data": {
    "totalCount": 3,
    "items": [
      {
        "employeeId": 1001,
        "employeeName": "丁霞",
        "phoneMasked": "196***0821",
        "employeeType": "退休返聘",
        "transferCount": 2,
        "affectedMonths": 3,
        "totalAmount": 9463.44,
        "adjustments": [
          {
            "billMonth": "2026-03",
            "oldSettlementEntity": "人才产业园",
            "newSettlementEntity": "人才产业园",
            "amount": 3154.48,
            "status": "unchanged",
            "triggerType": "transfer"
          },
          {
            "billMonth": "2026-04",
            "oldSettlementEntity": "人才产业园",
            "newSettlementEntity": "北京项目",
            "amount": 3154.48,
            "status": "pending",
            "triggerType": "transfer"
          },
          {
            "billMonth": "2026-05",
            "oldSettlementEntity": "人才产业园",
            "newSettlementEntity": "上海项目",
            "amount": 3154.48,
            "status": "pending",
            "triggerType": "transfer"
          }
        ],
        "transferHistory": [
          {
            "effectiveDate": "2026-03",
            "fromProject": "人才产业园",
            "toProject": "北京项目",
            "reason": "transfer"
          },
          {
            "effectiveDate": "2026-04",
            "fromProject": "北京项目",
            "toProject": "上海项目",
            "reason": "transfer"
          }
        ]
      }
    ]
  }
}
```

**检测逻辑:**
1. 遍历所有 `status != 'archived'` 的账单
2. 对于每个账单关联的员工，查询其 `employee_archive_version`
3. 对比账单 `bill_detail` 中的 `settlement_entity_id` 与员工当前版本
4. 若不一致且未归档，标记为 `pending`
5. 场景二（政策调整）: 额外检查 `cost_detail` 中的补差补退费用记录，按历史月份原归属方匹配
6. 场景三（手动补缴）: 检查补缴费用记录，按补缴月份原归属方匹配
7. 场景四（追溯参保）: 追溯期间费用归属当前参保方，标注原归属信息
8. 场景六（离职未停保）: 以停保状态为分界点检测

---

## 接口 2: 预览调整明细

### GET `/api/insurance/cost-allocation/adjustments/{employeeId}/preview`

**说明:** 获取某员工费用调整预览，用于用户确认前展示拆分结果。

**路径参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| employeeId | number | 是 | 员工ID |

**请求参数:**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| billMonth | string | 否 | 筛选特定月份 |

**响应:**

```json
{
  "code": 0,
  "data": {
    "employeeId": 1001,
    "employeeName": "丁霞",
    "phoneMasked": "196***0821",
    "employeeType": "退休返聘",
    "transferHistory": [
      { "effectiveDate": "2026-03", "fromProject": "人才产业园", "toProject": "北京项目" },
      { "effectiveDate": "2026-04", "fromProject": "北京项目", "toProject": "上海项目" }
    ],
    "billSplitPreview": [
      {
        "billMonth": "2026-03",
        "oldSettlementEntity": "人才产业园",
        "newSettlementEntity": "人才产业园",
        "amount": 3154.48,
        "action": "keep",
        "originalBillId": 5001
      },
      {
        "billMonth": "2026-04",
        "oldSettlementEntity": "人才产业园",
        "newSettlementEntity": "北京项目",
        "amount": 3154.48,
        "action": "split",
        "originalBillId": 5001,
        "newBillId": null
      },
      {
        "billMonth": "2026-05",
        "oldSettlementEntity": "人才产业园",
        "newSettlementEntity": "上海项目",
        "amount": 3154.48,
        "action": "split",
        "originalBillId": 5001,
        "newBillId": null
      }
    ],
    "splitResult": [
      {
        "settlementEntity": "人才产业园",
        "billMonths": ["2026-03"],
        "amount": 3154.48
      },
      {
        "settlementEntity": "北京项目",
        "billMonths": ["2026-04"],
        "amount": 3154.48
      },
      {
        "settlementEntity": "上海项目",
        "billMonths": ["2026-05"],
        "amount": 3154.48
      }
    ]
  }
}
```

---

## 接口 3: 执行重算

### POST `/api/insurance/cost-allocation/adjustments/recalculate`

**说明:** 执行费用归属重新核算，拆分账单并更新归属。

**请求体:**

```json
{
  "employeeIds": [1001, 1002],
  "billMonths": ["2026-04", "2026-05"]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| employeeIds | array[number] | 否 | 员工ID列表，与 billMonths 至少填一个 |
| billMonths | array[string] | 否 | 筛选月份 |

**响应:**

```json
{
  "code": 0,
  "data": {
    "total": 2,
    "success": 2,
    "failed": 0,
    "results": [
      {
        "employeeId": 1001,
        "employeeName": "丁霞",
        "status": "success",
        "adjustedMonths": 3,
        "newBillIds": [5002, 5003]
      },
      {
        "employeeId": 1002,
        "employeeName": "萧秀兰",
        "status": "success",
        "adjustedMonths": 2,
        "newBillIds": [5004]
      }
    ]
  }
}
```

**失败响应:**

```json
{
  "code": 0,
  "data": {
    "total": 2,
    "success": 1,
    "failed": 1,
    "results": [
      {
        "employeeId": 1001,
        "employeeName": "丁霞",
        "status": "success",
        "adjustedMonths": 3,
        "newBillIds": [5002, 5003]
      },
      {
        "employeeId": 1002,
        "employeeName": "萧秀兰",
        "status": "failed",
        "failReason": "账单已归档，无法调整"
      }
    ]
  }
}
```

**重算流程:**
1. 校验账单状态：已归档账单跳过，返回失败
2. 按员工+月份维度，将 `bill_detail` 中的明细拆分到不同结算主体
3. 为每个新归属创建新账单（或合并到已有同名账单）
4. 从原账单中移除拆分出去的明细
5. 若原账单只剩部分明细，保留原账单；若全部拆分，原账单标记删除
6. 写入 `cost_adjustment_log` 记录操作明细
7. 更新 `bill_detail` 中的 `settlement_entity_id` 快照
8. 返回新账单ID列表

**并发控制:**
- 同一员工的调整操作互斥，使用行锁（`SELECT ... FOR UPDATE` on `employee_id`）
- 不同员工可并行处理
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/specs/2026-04-28-cost-adjustment-api-design.md
git commit -m "feat: 费用归属调整 API 接口设计 — 检测/预览/重算三组接口"
```

---

### Task 3: 业务逻辑文档

**Files:**
- Create: `docs/superpowers/specs/2026-04-28-cost-adjustment-business-logic.md`

- [ ] **Step 1: 创建业务逻辑文档**

```markdown
# 费用归属调整 — 业务逻辑

> 日期：2026-04-28
> 关联设计：`2026-04-28-employee-transfer-cost-allocation-design.md`

## 检测引擎

### 触发点

| 场景 | 触发条件 | 检测范围 |
|------|---------|---------|
| 调动/重新入职 | `employee_archive_version` 新增记录，`change_reason` IN ('transfer', 'rehire') | 该员工所有未归档账单 |
| 政策调整补差补退 | `cost_detail` 中新增 `fee_type = 'adjustment'` 的费用记录 | 该费用对应的历史月份所有未归档账单 |
| 手动补缴历史月份 | 用户手动创建补缴费用，`fee_type = 'supplement'` | 补缴费用所属月份的所有未归档账单 |
| 追溯参保 | B项目参保生效日期追溯至历史月份 | 追溯期间产生的所有费用记录 |
| 审批生效日不一致 | 异动审批通过且 `effective_date < approval_date` | `effective_date` 至当前月份的所有未归档账单 |
| 离职未停保 | 员工离职且 `insurance_status != 'stopped'` + 以新员工入职 | 离职前所有未停保费用记录 |

### 检测算法

```
FOR each unarchived bill:
    FOR each bill_detail in bill:
        employee = get_employee(bill_detail.employee_id)
        current_version = get_current_archive_version(employee.employee_id)
        
        IF bill_detail.settlement_entity_id != current_version.settlement_entity_id:
            IF bill_detail.settlement_entity_id_snapshot IS NULL:
                MARK as pending_adjustment
                SET old_entity = bill_detail.settlement_entity_id
                SET new_entity = current_version.settlement_entity_id
            ELSE IF bill_detail.settlement_entity_id_snapshot != current_version.settlement_entity_id:
                MARK as pending_adjustment
                SET old_entity = bill_detail.settlement_entity_id_snapshot
                SET new_entity = current_version.settlement_entity_id
        
        // 场景二：政策调整补差补退
        IF cost_detail.fee_type == 'adjustment':
            historical_version = get_archive_version_at_date(
                employee.employee_id, cost_detail.fee_month
            )
            SET cost_detail.settlement_entity_id_snapshot = historical_version.settlement_entity_id
            // 向谁收费就向谁退费
        
        // 场景三：手动补缴
        IF cost_detail.fee_type == 'supplement':
            historical_version = get_archive_version_at_date(
                employee.employee_id, cost_detail.fee_month
            )
            SET cost_detail.settlement_entity_id_snapshot = historical_version.settlement_entity_id
        
        // 场景四：追溯参保
        IF cost_detail.enroll_type == 'retroactive':
            current_version = get_current_archive_version(employee.employee_id)
            SET cost_detail.settlement_entity_id_snapshot = current_version.settlement_entity_id
            SET cost_detail.annotated_original_entity = historical_version.settlement_entity_id
        
        // 场景六：离职未停保
        IF employee.status == 'terminated' AND employee.insurance_status != 'stopped':
            termination_date = employee.termination_date
            IF cost_detail.fee_month <= termination_date:
                SET cost_detail.settlement_entity_id_snapshot = old_entity_before_termination
            ELSE:
                SET cost_detail.settlement_entity_id_snapshot = new_entity_after_rehire
```

### 辅助函数

```sql
-- 获取员工当前档案版本
SELECT * FROM employee_archive_version
WHERE employee_id = ? AND end_date IS NULL
ORDER BY start_date DESC LIMIT 1;

-- 获取指定日期时的档案版本
SELECT * FROM employee_archive_version
WHERE employee_id = ?
  AND start_date <= ?
  AND (end_date IS NULL OR end_date >= ?)
ORDER BY start_date DESC LIMIT 1;

-- 查询员工未归档账单
SELECT b.*, bd.*
FROM bill b
JOIN bill_detail bd ON b.bill_id = bd.bill_id
WHERE bd.employee_id = ?
  AND b.status != 'archived';
```

---

## 重算拆分算法

### 输入

- 员工ID
- 待调整的账单明细列表（含月份、原归属、新归属、金额）

### 输出

- 新账单列表（每个新归属一个账单）
- 原账单更新/删除结果

### 算法

```
GROUP adjustments BY (settlement_entity_id, customer_id, project_id):
    FOR each group:
        IF existing_bill(settlement_entity_id, customer_id, bill_month):
            // 合并到已有账单
            INSERT INTO bill_detail (bill_id, cost_id, employee_id, ...)
            VALUES (existing_bill_id, cost_id, employee_id, ...)
            UPDATE bill SET total_amount = total_amount + group_amount
            SET new_bill_id = existing_bill_id
        ELSE:
            // 创建新账单
            INSERT INTO bill (settlement_entity_id, customer_id, bill_month, total_amount, ...)
            VALUES (settlement_entity_id, customer_id, bill_month, group_amount, ...)
            SET new_bill_id = last_insert_id()
            
            INSERT INTO bill_detail (bill_id, cost_id, employee_id, ...)
            VALUES (new_bill_id, cost_id, employee_id, ...)

// 处理原账单
FOR each original_bill:
    remaining_details = SELECT * FROM bill_detail WHERE bill_id = original_bill_id
    IF remaining_details IS EMPTY:
        // 全部拆分出去，删除原账单
        DELETE FROM bill WHERE bill_id = original_bill_id
    ELSE:
        // 部分拆分，更新原账单金额
        UPDATE bill SET total_amount = SUM(remaining_details.amount)
        WHERE bill_id = original_bill_id

// 记录日志
INSERT INTO cost_adjustment_log (...)
VALUES (...)
```

### 边界情况

| 情况 | 处理 |
|------|------|
| 原账单全部明细都被拆分 | 删除原账单 |
| 新归属已有同名账单（同主体+同客户+同月份） | 合并到已有账单 |
| 重算中途失败 | 回滚所有已创建的新账单和明细 |
| 同一员工多个月份同时调整 | 按月份独立处理，失败不影响其他月份 |
| 账单已归档 | 跳过，返回失败 |
| 员工已不存在 | 跳过，记录错误日志 |

---

## 事务保证

### 重算事务

```
BEGIN TRANSACTION;
    -- 锁定员工记录
    SELECT * FROM employee WHERE employee_id = ? FOR UPDATE;
    
    -- 锁定相关账单
    SELECT * FROM bill WHERE ... FOR UPDATE;
    
    -- 执行拆分
    -- 1. 创建新账单
    -- 2. 迁移明细
    -- 3. 更新/删除原账单
    -- 4. 写入调整日志
    
    -- 任一失败则 ROLLBACK
COMMIT;
```

### 并发安全

- 同一员工的调整操作通过 `employee_id` 行锁互斥
- 不同员工的调整操作可并行执行
- 账单操作通过 `bill_id` 行锁防止并发修改
```

- [ ] **Step 2: 提交**

```bash
git add docs/superpowers/specs/2026-04-28-cost-adjustment-business-logic.md
git commit -m "feat: 费用归属调整业务逻辑文档 — 检测引擎规则与重算拆分算法"
```

---

## 自检清单

| 需求 | 对应 Task |
|------|----------|
| 费用调整日志表（追踪重算操作） | Task 1 |
| 检测接口（GET /adjustments） | Task 2 |
| 预览接口（GET /adjustments/{id}/preview） | Task 2 |
| 重算接口（POST /adjustments/recalculate） | Task 2 |
| 6个场景检测规则 | Task 3 |
| 重算拆分算法 | Task 3 |
| 边界情况处理 | Task 3 |
| 事务与并发控制 | Task 3 |
| 回滚脚本 | Task 1 |

无占位符，无 TODO，所有步骤包含完整代码。
