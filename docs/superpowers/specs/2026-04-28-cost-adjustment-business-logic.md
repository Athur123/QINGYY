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
