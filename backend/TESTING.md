# 集成测试指南

## 前置条件

1. 企业微信/钉钉开发者账号
2. 已配置好回调地址（需公网可访问）

## 测试步骤

### 1. 配置环境变量

```bash
export WECOM_CORP_ID=xxx
export WECOM_AGENT_ID=xxx
export WECOM_SECRET=xxx
export WECOM_CALLBACK_TOKEN=xxx
export DINGTALK_APP_KEY=xxx
export DINGTALK_APP_SECRET=xxx
export DINGTALK_CALLBACK_SECRET=xxx
export CALLBACK_URL=https://your-domain.com/api/approval/callback
```

### 2. 启动服务

```bash
cd backend
pip install -r requirements.txt
uvicorn approval.main:app --reload --port 8000
```

### 3. 测试推送

```bash
curl -X POST http://localhost:8000/api/approval/push \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "finance_receivable",
    "document_id": 123,
    "platform": "wecom",
    "applicant_mobile": "13800138000",
    "applicant_name": "张三",
    "form_data": {
      "amount": 10000,
      "payee": "某公司",
      "remark": "测试账单"
    }
  }'
```

预期返回：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "approval_id": 1,
    "platform": "wecom",
    "instance_id": "wecom_instance_xxx",
    "status": "PENDING"
  }
}
```

### 4. 模拟回调

在企业微信后台配置好审批流程，然后完成一个审批实例。

回调会发送到 `/api/approval/callback/wecom`。

### 5. 验证状态更新

```bash
curl http://localhost:8000/api/approval/status/1
```

## 运行单元测试

```bash
cd backend
PYTHONPATH=/path/to/project/backend pytest tests/approval/ -v
```
