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