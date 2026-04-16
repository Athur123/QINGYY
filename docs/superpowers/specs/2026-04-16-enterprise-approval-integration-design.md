# 企业微信/钉钉审批集成设计方案

## 1. 概述

### 1.1 背景与目标

青阳云 HRO 系统需要与企业微信、钉钉实现审批流程对接，让员工可以在企业微信或钉钉中完成审批操作，无需切换系统。

### 1.2 设计范围

| 单据类型 | 说明 |
|---------|------|
| 财务应收/应付单 | 账单生成后触发审批，财务人员确认金额、收款方信息 |
| 考勤审批单 | 请假、加班、调休等，需直属上级和HR确认 |
| 其他审批单 | 扩展支持其他审批流程类型 |

### 1.3 集成平台

- 企业微信（WeCom）
- 钉钉（DingTalk）
- 双平台独立运行，互不影响

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        青阳云 HRO 系统                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  财务应收单  │  │  考勤审批单  │  │   其他单据   │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         └────────────────┼────────────────┘                    │
│                          ▼                                     │
│              ┌───────────────────────┐                        │
│              │    统一审批推送服务      │                        │
│              │  (ApprovalPushService)  │                        │
│              └───────────┬───────────┘                        │
│                          │                                    │
└──────────────────────────┼────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
┌─────────────────────┐       ┌─────────────────────┐
│    企业微信 SDK      │       │     钉钉 SDK         │
│  (WecomAdapter)     │       │   (DingTalkAdapter)  │
└─────────┬───────────┘       └──────────┬──────────┘
          │                              │
          ▼                              ▼
┌─────────────────────┐       ┌─────────────────────┐
│    企业微信审批      │       │     钉钉审批        │
│   (审批表单+流程)    │       │   (审批表单+流程)    │
└─────────────────────┘       └─────────────────────┘
```

### 2.2 核心组件

| 组件 | 职责 |
|-----|------|
| ApprovalPushService | 统一审批推送服务，屏蔽平台差异 |
| WecomAdapter | 企业微信 SDK 适配器，负责推送、回调、查询 |
| DingTalkAdapter | 钉钉 SDK 适配器，负责推送、回调、查询 |
| FieldMappingService | 字段映射服务，青阳云字段 ↔ 第三方表单字段双向映射 |
| ApprovalCallbackController | 接收第三方 Webhook 回调的 API |

### 2.3 架构模式

采用 **官方SDK + 轻量包装** 模式：

- 直接使用企业微信/钉钉官方提供的 SDK
- 只做轻量级包装，适配青阳云的数据格式
- 审批表单设计在第三方平台完成，青阳云负责推送数据和接收结果

---

## 3. 功能设计

### 3.1 身份映射

**方案**：手机号自动匹配

- 青阳云员工手机号 = 企业微信/钉钉注册手机号
- 推送审批时，根据手机号自动查找对应的第三方用户ID
- 无需员工手动绑定，用户无感知

### 3.2 字段映射

审批表单在企业微信/钉钉设计，青阳云只负责数据推送和接收。

**双向映射规则**：

| 青阳云字段 | 第三方表单字段 | 说明 |
|-----------|--------------|------|
| 申请人姓名 | applicant_name | 发起人信息 |
| 申请金额 | amount | 财务单金额 |
| 费用类型 | expense_type | 如：服务费、工资等 |
| 收款方 | payee | 付款对象 |
| 摘要 | remark | 审批备注 |
| ... | 自定义字段 | 由第三方表单定义 |

**映射配置表**（数据库存储）：

```json
{
  "document_type": "finance_receivable",
  "platform": "wecom",
  "field_mappings": [
    { "qy_field": "amount", "third_party_field": "amount", "required": true },
    { "qy_field": "payee", "third_party_field": "payee_name", "required": true }
  ]
}
```

### 3.3 审批推送流程

```
1. 青阳云创建/提交单据
       ↓
2. ApprovalPushService 构建推送数据
   - 根据单据类型查找字段映射配置
   - 根据手机号查询第三方用户ID
   - 按第三方格式组装表单数据
       ↓
3. 调用适配器推送到目标平台
   - WecomAdapter.pushApproval()
   - DingTalkAdapter.pushApproval()
       ↓
4. 第三方创建审批实例
   - 返回审批单号（instance_id）
       ↓
5. 青阳云保存审批单号和状态
   - status: PENDING_APPROVAL
```

### 3.4 结果回调机制

采用 **Webhook + 轮询** 双重保障：

#### 3.4.1 Webhook 回调（主）

```
企业微信/钉钉审批完成
       ↓
POST /api/approval/callback
{
  "platform": "wecom",
  "instance_id": "xxx",
  "status": "APPROVED",  // APPROVED / REJECTED
  "approver": "手机号",
  "comment": "同意",
  "form_fields": { ... }  // 表单字段值
}
       ↓
青阳云更新单据状态
```

#### 3.4.2 轮询查询（兜底）

```
定时任务（如每5分钟）
       ↓
查询已推送但超时的审批单
       ↓
调用第三方API查询最新状态
       ↓
更新青阳云单据状态
```

### 3.5 状态处理

审批通过后，青阳云直接标记状态为"已审批"：

| 第三方状态 | 青阳云状态 |
|-----------|-----------|
| PENDING | 待审批 |
| APPROVED | 已审批 |
| REJECTED | 已拒绝 |
| CANCELLED | 已撤回 |

---

## 4. 数据模型

### 4.1 审批记录表（approval_record）

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | BIGINT | 主键 |
| document_type | VARCHAR | 单据类型：finance_receivable, attendance, ... |
| document_id | BIGINT | 青阳云原始单据ID |
| platform | VARCHAR | 平台：wecom, dingtalk |
| platform_instance_id | VARCHAR | 第三方审批实例ID |
| applicant_mobile | VARCHAR | 申请人手机号 |
| applicant_name | VARCHAR | 申请人姓名 |
| status | VARCHAR | 审批状态 |
| push_time | DATETIME | 推送时间 |
| callback_time | DATETIME | 回调时间（审批完成时间） |
| form_data | JSON | 推送时提交的表单数据 |
| result_data | JSON | 回调时接收的表单结果 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### 4.2 字段映射配置表（field_mapping_config）

| 字段 | 类型 | 说明 |
|-----|------|------|
| id | BIGINT | 主键 |
| document_type | VARCHAR | 单据类型 |
| platform | VARCHAR | 平台 |
| qy_field | VARCHAR | 青阳云字段名 |
| third_party_field | VARCHAR | 第三方表单字段名 |
| required | BOOLEAN | 是否必填 |
| created_at | DATETIME | 创建时间 |

---

## 5. API 设计

### 5.1 推送审批

```
POST /api/approval/push
Content-Type: application/json

Request:
{
  "document_type": "finance_receivable",
  "document_id": 12345,
  "platform": "wecom",  // wecom / dingtalk / auto
  "applicant_mobile": "13800138000",
  "form_data": {
    "amount": 10000.00,
    "payee": "某公司",
    "remark": "月度服务费"
  }
}

Response:
{
  "code": 0,
  "message": "success",
  "data": {
    "approval_id": "xxx",
    "platform": "wecom",
    "instance_id": "yyy",
    "status": "PENDING_APPROVAL"
  }
}
```

### 5.2 Webhook 回调

```
POST /api/approval/callback/{platform}

企业微信格式:
{
  "event": "approval_chain_finish",
  "token": "xxx",
  "instance_id": "yyy",
  "approval_id": "zzz"
}

钉钉格式:
{
  "eventType": "approval_instance_finish",
  "processInstanceId": "yyy"
}

Response:
{
  "code": 0,
  "message": "success"
}
```

### 5.3 主动查询状态

```
GET /api/approval/status/{approval_id}

Response:
{
  "code": 0,
  "message": "success",
  "data": {
    "approval_id": "xxx",
    "status": "APPROVED",
    "platform": "wecom",
    "instance_id": "yyy",
    "updated_at": "2026-04-16 10:00:00"
  }
}
```

---

## 6. 安全设计

### 6.1 回调验签

- 企业微信：验证 msg_signature 参数
- 钉钉：验证签名字符串

### 6.2 敏感数据

- 手机号加密存储
- 回调 IP 白名单限制

---

## 7. 配置管理

### 7.1 平台配置（settings.local.json）

```json
{
  "wecom": {
    "corp_id": "xxx",
    "agent_id": "xxx",
    "secret": "xxx"
  },
  "dingtalk": {
    "app_key": "xxx",
    "app_secret": "xxx"
  }
}
```

### 7.2 字段映射配置

在数据库中管理，支持按单据类型和平台配置不同的映射规则。

---

## 8. 错误处理

| 错误场景 | 处理方式 |
|---------|---------|
| 推送失败（网络/SDK） | 重试3次，间隔指数退避 |
| 推送用户不存在 | 记录日志，标记失败，通知管理员 |
| Webhook 回调失败 | 记录日志，返回失败，第三方会重试 |
| 轮询发现异常状态 | 记录日志，发送告警 |

---

## 9. 实现优先级

### Phase 1 - MVP
1. 企业微信适配器 + 财务单据推送
2. Webhook 回调接收
3. 轮询兜底

### Phase 2 - 扩展
1. 钉钉适配器
2. 考勤审批单支持
3. 管理后台（映射配置）

### Phase 3 - 完善
1. 其他单据类型扩展
2. 监控告警
3. 性能优化
