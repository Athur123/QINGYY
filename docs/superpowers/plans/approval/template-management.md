# 审批模板管理页面实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现审批模板管理页面，包括模板列表、鉴权配置、同步操作

**Architecture:** 前端使用 HTML 原型 + JavaScript，后端使用 FastAPI，数据库存储模板和鉴权配置

**Tech Stack:** HTML/CSS/JavaScript, FastAPI, SQLAlchemy

---

## 文件结构

```
backend/
├── approval/
│   ├── models/
│   │   ├── __init__.py                    # 导出所有模型
│   │   ├── approval_template.py           # 审批模板模型 (新增)
│   │   └── platform_auth.py               # 鉴权配置模型 (新增)
│   ├── api/
│   │   ├── __init__.py
│   │   ├── templates.py                   # 模板列表 API (新增)
│   │   ├── sync.py                        # 同步 API (新增)
│   │   ├── auth.py                        # 鉴权配置 API (新增)
│   │   ├── push.py                        # (已存在)
│   │   ├── callback.py                    # (已存在)
│   │   └── status.py                      # (已存在)
│   ├── services/
│   │   ├── template_sync.py              # 模板同步服务 (新增)
│   │   └── __init__.py
│   └── config.py                          # (已存在，需添加内置模板配置)

prototype/
├── approval-template-management.html       # 模板管理页面原型 (新增)
└── components/
    ├── drawer.js                          # 抽屉组件 (新增)
    └── modal.js                           # 弹窗组件 (新增)
```

---

## 内置审批模板配置

**在 config.py 中添加：**

```python
# 内置审批模板配置
BUILTIN_TEMPLATES = {
    "finance_receivable": {
        "name": "财务应收单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "申请金额", "type": "number"},
            {"id": "3", "name": "收款方", "type": "text"},
            {"id": "4", "name": "费用类型", "type": "radio", "options": ["服务费", "工资", "其他"]},
            {"id": "5", "name": "摘要", "type": "textarea"}
        ]
    },
    "finance_payable": {
        "name": "财务应付单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "付款金额", "type": "number"},
            {"id": "3", "name": "付款方", "type": "text"},
            {"id": "4", "name": "付款方式", "type": "radio", "options": ["转账", "支票", "现金"]},
            {"id": "5", "name": "摘要", "type": "textarea"}
        ]
    },
    "attendance": {
        "name": "考勤审批单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "申请类型", "type": "radio", "options": ["请假", "加班", "调休"]},
            {"id": "3", "name": "开始时间", "type": "date"},
            {"id": "4", "name": "结束时间", "type": "date"},
            {"id": "5", "name": "时长(天)", "type": "number"},
            {"id": "6", "name": "原因", "type": "textarea"}
        ]
    }
}
```

---

## Task 1: 数据模型 - 审批模板

**Files:**
- Create: `backend/approval/models/approval_template.py`
- Modify: `backend/approval/models/__init__.py`

- [ ] **Step 1: 创建 approval_template.py**

```python
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ApprovalTemplate(Base):
    """审批模板"""
    __tablename__ = "approval_template"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)              # 模板名称
    type = Column(String(50), nullable=False, index=True)  # 模板类型
    platform = Column(String(20), nullable=False)          # 平台：wecom, dingtalk
    wecom_template_id = Column(String(100), nullable=True)   # 企业微信模板ID
    form_config = Column(JSON, nullable=False)               # 表单配置（内置）
    sync_status = Column(String(20), default="unsynced")    # 同步状态
    auto_sync = Column(Boolean, default=False)              # 是否自动同步
    last_sync_time = Column(DateTime, nullable=True)        # 最后同步时间
    last_error = Column(Text, nullable=True)                 # 最后错误信息
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

- [ ] **Step 2: 创建 platform_auth.py**

```python
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PlatformAuth(Base):
    """平台鉴权配置"""
    __tablename__ = "platform_auth"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    platform = Column(String(20), nullable=False, unique=True)  # 平台：wecom, dingtalk
    corpid = Column(String(100), nullable=False)                 # 企业ID
    secret = Column(String(500), nullable=False)                  # 应用Secret
    agentid = Column(String(50), nullable=False)                  # 应用AgentId
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

- [ ] **Step 3: 更新 models/__init__.py**

```python
from approval.models.approval_record import ApprovalRecord, ApprovalStatus, Platform
from approval.models.field_mapping import FieldMappingConfig
from approval.models.approval_template import ApprovalTemplate
from approval.models.platform_auth import PlatformAuth

__all__ = [
    "ApprovalRecord", "ApprovalStatus", "Platform",
    "FieldMappingConfig", "ApprovalTemplate", "PlatformAuth"
]
```

- [ ] **Step 4: 验证模型**

```bash
python -c "
from approval.models import ApprovalTemplate, PlatformAuth
print('Models imported successfully')
print(f'ApprovalTemplate fields: {[c.name for c in ApprovalTemplate.__table__.columns]}')
"
```

- [ ] **Step 5: 提交**

```bash
git add backend/approval/models/
git commit -m "feat: add approval template and platform auth models"
```

---

## Task 2: 内置模板配置和初始化

**Files:**
- Modify: `backend/approval/config.py`

- [ ] **Step 1: 添加内置模板配置到 config.py**

```python
# 内置审批模板配置
BUILTIN_TEMPLATES = {
    "finance_receivable": {
        "name": "财务应收单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "申请金额", "type": "number"},
            {"id": "3", "name": "收款方", "type": "text"},
            {"id": "4", "name": "费用类型", "type": "radio", "options": ["服务费", "工资", "其他"]},
            {"id": "5", "name": "摘要", "type": "textarea"}
        ]
    },
    "finance_payable": {
        "name": "财务应付单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "付款金额", "type": "number"},
            {"id": "3", "name": "付款方", "type": "text"},
            {"id": "4", "name": "付款方式", "type": "radio", "options": ["转账", "支票", "现金"]},
            {"id": "5", "name": "摘要", "type": "textarea"}
        ]
    },
    "attendance": {
        "name": "考勤审批单",
        "platform": "wecom",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "申请类型", "type": "radio", "options": ["请假", "加班", "调休"]},
            {"id": "3", "name": "开始时间", "type": "date"},
            {"id": "4", "name": "结束时间", "type": "date"},
            {"id": "5", "name": "时长(天)", "type": "number"},
            {"id": "6", "name": "原因", "type": "textarea"}
        ]
    }
}
```

- [ ] **Step 2: 添加获取内置模板的函数**

```python
def get_builtin_template(template_type: str) -> dict:
    """获取内置模板配置"""
    return BUILTIN_TEMPLATES.get(template_type)

def get_all_builtin_templates() -> dict:
    """获取所有内置模板"""
    return BUILTIN_TEMPLATES
```

- [ ] **Step 3: 提交**

```bash
git add backend/approval/config.py
git commit -m "feat: add builtin template configurations"
```

---

## Task 3: API - 模板列表

**Files:**
- Create: `backend/approval/api/templates.py`
- Modify: `backend/approval/api/__init__.py`

- [ ] **Step 1: 创建 templates.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from approval.models import ApprovalTemplate
from approval.config import get_all_builtin_templates

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class TemplateResponse(BaseModel):
    id: Optional[int]
    name: str
    type: str
    platform: str
    wecom_template_id: Optional[str]
    form_config: dict
    sync_status: str
    auto_sync: bool
    last_sync_time: Optional[str]
    created_at: Optional[str]

class TemplateListResponse(BaseModel):
    code: int
    message: str
    data: List[TemplateResponse]

@router.get("/templates", response_model=TemplateListResponse)
def list_templates(
    search: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取模板列表"""
    # TODO: 从数据库查询
    # 暂时返回内置模板列表
    builtins = get_all_builtin_templates()
    templates = []

    for template_type, config in builtins.items():
        # TODO: 查询数据库中的记录
        templates.append({
            "id": None,
            "name": config["name"],
            "type": template_type,
            "platform": config["platform"],
            "wecom_template_id": None,
            "form_config": config,
            "sync_status": "unsynced",
            "auto_sync": False,
            "last_sync_time": None,
            "created_at": None
        })

    return TemplateListResponse(code=0, message="success", data=templates)

@router.get("/templates/{template_type}", response_model=TemplateResponse)
def get_template(
    template_type: str,
    db: Session = Depends(get_db)
):
    """获取单个模板详情"""
    builtin = get_builtin_template(template_type)
    if not builtin:
        raise HTTPException(status_code=404, detail="Template not found")

    # TODO: 查询数据库中的记录
    return TemplateResponse(
        id=None,
        name=builtin["name"],
        type=template_type,
        platform=builtin["platform"],
        wecom_template_id=None,
        form_config=builtin,
        sync_status="unsynced",
        auto_sync=False,
        last_sync_time=None,
        created_at=None
    )
```

- [ ] **Step 2: 更新 __init__.py**

```python
from approval.api.push import router as push_router
from approval.api.callback import router as callback_router
from approval.api.status import router as status_router
from approval.api.templates import router as templates_router

__all__ = ["push_router", "callback_router", "status_router", "templates_router"]
```

- [ ] **Step 3: 更新 main.py 引入模板路由**

```python
from approval.api import push_router, callback_router, status_router, templates_router

app.include_router(templates_router, prefix="/api/approval", tags=["模板"])
```

- [ ] **Step 4: 提交**

```bash
git add backend/approval/api/templates.py backend/approval/api/__init__.py backend/approval/main.py
git commit -m "feat: add template list API"
```

---

## Task 4: API - 鉴权配置

**Files:**
- Create: `backend/approval/api/auth.py`
- Modify: `backend/approval/api/__init__.py`

- [ ] **Step 1: 创建 auth.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.models import PlatformAuth

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class AuthConfig(BaseModel):
    platform: str
    corpid: str
    secret: str
    agentid: str

class AuthSaveRequest(BaseModel):
    platform: str
    corpid: str
    secret: str
    agentid: str

class AuthResponse(BaseModel):
    code: int
    message: str
    data: Optional[AuthConfig]

@router.get("/auth/{platform}", response_model=AuthResponse)
def get_auth_config(
    platform: str,
    db: Session = Depends(get_db)
):
    """获取鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == platform
    ).first()

    if not auth:
        return AuthResponse(code=0, message="success", data=None)

    return AuthResponse(
        code=0,
        message="success",
        data=AuthConfig(
            platform=auth.platform,
            corpid=auth.corpid,
            secret="******",  # 脱敏
            agentid=auth.agentid
        )
    )

@router.put("/auth", response_model=AuthResponse)
def save_auth_config(
    request: AuthSaveRequest,
    db: Session = Depends(get_db)
):
    """保存鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == request.platform
    ).first()

    if auth:
        auth.corpid = request.corpid
        auth.secret = request.secret
        auth.agentid = request.agentid
    else:
        auth = PlatformAuth(
            platform=request.platform,
            corpid=request.corpid,
            secret=request.secret,
            agentid=request.agentid
        )
        db.add(auth)

    db.commit()

    return AuthResponse(
        code=0,
        message="success",
        data=AuthConfig(
            platform=request.platform,
            corpid=request.corpid,
            secret="******",
            agentid=request.agentid
        )
    )

@router.post("/auth/{platform}/verify")
def verify_auth_config(
    platform: str,
    db: Session = Depends(get_db)
):
    """验证鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == platform
    ).first()

    if not auth:
        return {"code": 1, "message": "配置不存在"}

    # TODO: 调用企业微信API验证
    return {"code": 0, "message": "验证成功"}
```

- [ ] **Step 2: 更新 __init__.py 添加 auth_router**

```python
from approval.api.auth import router as auth_router
```

- [ ] **Step 3: 提交**

```bash
git add backend/approval/api/auth.py
git commit -m "feat: add auth config API"
```

---

## Task 5: API - 同步操作

**Files:**
- Create: `backend/approval/services/template_sync.py`
- Create: `backend/approval/api/sync.py`
- Modify: `backend/approval/api/__init__.py`

- [ ] **Step 1: 创建 template_sync.py**

```python
import httpx
from typing import Optional
from datetime import datetime
from approval.config import load_config, get_builtin_template

def get_wecom_access_token() -> str:
    """获取企业微信 access_token"""
    config = load_config()
    wecom_config = config.wecom

    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        "corpid": wecom_config.corp_id,
        "corpsecret": wecom_config.secret
    }
    resp = httpx.get(url, params=params)
    data = resp.json()

    if data.get("errcode") != 0:
        raise Exception(f"Failed to get access_token: {data}")

    return data["access_token"]

def build_wecom_template_content(form_config: dict) -> dict:
    """将表单配置转换为企业微信模板格式"""
    controls = []

    for field in form_config.get("fields", []):
        control_type_map = {
            "text": "Text",
            "number": "Number",
            "radio": "Selector",
            "textarea": "Textarea",
            "date": "Date"
        }

        control_id = f"field-{field['id']}"
        control = {
            "property": {
                "control": control_type_map.get(field["type"], "Text"),
                "id": control_id,
                "title": [{"text": field["name"], "lang": "zh_CN"}],
                "placeholder": [{"text": f"请输入{field['name']}", "lang": "zh_CN"}],
                "require": 0,
                "un_print": 1
            },
            "config": {}
        }

        # 单选控件需要配置选项
        if field["type"] == "radio" and "options" in field:
            control["config"]["selector"] = {
                "type": "single",
                "options": [
                    {"key": f"option-{i}", "value": {"text": opt, "lang": "zh_CN"}}
                    for i, opt in enumerate(field["options"])
                ]
            }

        controls.append(control)

    return {
        "template_name": [{"text": form_config.get("name", ""), "lang": "zh_CN"}],
        "template_content": {"controls": controls}
    }

def sync_template_to_wecom(template_type: str, form_config: dict) -> str:
    """
    同步模板到企业微信

    Returns: 企业微信模板ID
    """
    token = get_wecom_access_token()
    url = "https://qyapi.weixin.qq.com/cgi-bin/oa/approval/create_template"
    params = {"access_token": token}

    template_content = build_wecom_template_content(form_config)

    resp = httpx.post(url, params=params, json=template_content)
    print(f"Response status: {resp.status_code}")
    print(f"Response body: {resp.text}")

    if resp.status_code == 404:
        raise Exception("API endpoint not found, please check WeCom API documentation")

    data = resp.json()

    if data.get("errcode") != 0:
        raise Exception(f"Failed to sync template: {data}")

    return data.get("template_id")
```

- [ ] **Step 2: 创建 sync.py**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.models import ApprovalTemplate
from approval.config import get_builtin_template
from approval.services.template_sync import sync_template_to_wecom

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class SyncResponse(BaseModel):
    code: int
    message: str
    data: dict

@router.post("/templates/{template_type}/sync", response_model=SyncResponse)
def sync_template(
    template_type: str,
    db: Session = Depends(get_db)
):
    """同步模板到企业微信"""
    # 获取内置模板配置
    builtin = get_builtin_template(template_type)
    if not builtin:
        raise HTTPException(status_code=404, detail="Template not found")

    try:
        # 同步到企业微信
        template_id = sync_template_to_wecom(template_type, builtin)

        return SyncResponse(
            code=0,
            message="同步成功",
            data={"template_id": template_id}
        )
    except Exception as e:
        return SyncResponse(
            code=1,
            message=f"同步失败: {str(e)}",
            data={}
        )
```

- [ ] **Step 3: 更新 __init__.py 添加 sync_router**

```python
from approval.api.sync import router as sync_router
```

- [ ] **Step 4: 提交**

```bash
git add backend/approval/services/template_sync.py backend/approval/api/sync.py
git commit -m "feat: add template sync service and API"
```

---

## Task 6: 前端页面 - 模板管理

**Files:**
- Create: `prototype/approval-template-management.html`

- [ ] **Step 1: 创建 HTML 页面**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>审批模板管理</title>
    <link rel="stylesheet" href="../styles/qingyang-variables.css">
    <link rel="stylesheet" href="../styles/qingyang-components.css">
    <style>
        .page-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 24px;
            background: #fff;
            border-bottom: 1px solid #e2e8f0;
        }
        .page-title {
            font-size: 18px;
            font-weight: 600;
        }
        .template-table {
            width: 100%;
            border-collapse: collapse;
        }
        .template-table th,
        .template-table td {
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        .template-table th {
            background: #f8fafc;
            font-weight: 500;
            color: #64748b;
        }
        .sync-status {
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .sync-status .dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }
        .sync-status.unsynced .dot { background: #94a3b8; }
        .sync-status.syncing .dot { background: #3b82f6; }
        .sync-status.synced .dot { background: #22c55e; }
        .sync-status.failed .dot { background: #ef4444; }
        .btn {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 14px;
            cursor: pointer;
            border: none;
        }
        .btn-primary {
            background: #2563eb;
            color: #fff;
        }
        .btn-secondary {
            background: #f1f5f9;
            color: #475569;
        }
        /* 抽屉样式 */
        .drawer {
            position: fixed;
            top: 0;
            right: -480px;
            width: 480px;
            height: 100vh;
            background: #fff;
            box-shadow: -4px 0 24px rgba(0,0,0,0.1);
            transition: right 0.3s;
            z-index: 1000;
        }
        .drawer.open { right: 0; }
        .drawer-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 16px 20px;
            border-bottom: 1px solid #e2e8f0;
        }
        .drawer-body { padding: 20px; }
        /* 弹窗样式 */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 2000;
        }
        .modal.open { display: flex; align-items: center; justify-content: center; }
        .modal-content {
            background: #fff;
            border-radius: 12px;
            width: 480px;
            max-width: 90%;
        }
    </style>
</head>
<body>
    <div class="page-header">
        <h1 class="page-title">审批模板管理</h1>
        <button class="btn btn-secondary" onclick="openAuthModal()">鉴权设置</button>
    </div>

    <div style="padding: 24px;">
        <table class="template-table">
            <thead>
                <tr>
                    <th>模板名称</th>
                    <th>模板类型</th>
                    <th>同步状态</th>
                    <th>操作</th>
                </tr>
            </thead>
            <tbody id="templateList">
                <!-- 动态填充 -->
            </tbody>
        </table>
    </div>

    <!-- 模板详情抽屉 -->
    <div class="drawer" id="drawer">
        <div class="drawer-header">
            <h3>模板详情</h3>
            <button onclick="closeDrawer()">×</button>
        </div>
        <div class="drawer-body" id="drawerContent">
            <!-- 动态填充 -->
        </div>
    </div>

    <!-- 鉴权配置弹窗 -->
    <div class="modal" id="authModal">
        <div class="modal-content">
            <div class="drawer-header">
                <h3>企业微信鉴权配置</h3>
                <button onclick="closeAuthModal()">×</button>
            </div>
            <div style="padding: 20px;">
                <div style="margin-bottom: 16px;">
                    <label>企业ID (corpid)</label>
                    <input type="text" id="corpid" class="qy-input" style="width:100%">
                </div>
                <div style="margin-bottom: 16px;">
                    <label>应用Secret</label>
                    <input type="password" id="secret" class="qy-input" style="width:100%">
                </div>
                <div style="margin-bottom: 16px;">
                    <label>应用AgentId</label>
                    <input type="text" id="agentid" class="qy-input" style="width:100%">
                </div>
                <div style="text-align:right;">
                    <button class="btn btn-secondary" onclick="closeAuthModal()">取消</button>
                    <button class="btn btn-primary" onclick="saveAuth()">保存</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:8000/api/approval';

        // 加载模板列表
        async function loadTemplates() {
            try {
                const res = await fetch(`${API_BASE}/templates`);
                const data = await res.json();
                renderTemplates(data.data);
            } catch (e) {
                console.error('Failed to load templates:', e);
            }
        }

        // 渲染模板列表
        function renderTemplates(templates) {
            const tbody = document.getElementById('templateList');
            tbody.innerHTML = templates.map(t => `
                <tr>
                    <td>${t.name}</td>
                    <td>${t.type}</td>
                    <td>
                        <span class="sync-status ${t.sync_status}">
                            <span class="dot"></span>
                            <span>${getStatusText(t.sync_status)}</span>
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-secondary" onclick="openDrawer('${t.type}')">详情</button>
                        <button class="btn btn-primary" onclick="syncTemplate('${t.type}')">同步</button>
                    </td>
                </tr>
            `).join('');
        }

        function getStatusText(status) {
            const map = { unsynced: '未同步', syncing: '同步中', synced: '已同步', failed: '同步失败' };
            return map[status] || status;
        }

        // 打开抽屉
        async function openDrawer(templateType) {
            const res = await fetch(`${API_BASE}/templates/${templateType}`);
            const data = await res.json();
            const t = data.data;

            document.getElementById('drawerContent').innerHTML = `
                <div style="margin-bottom:16px;">
                    <label>模板名称:</label>
                    <div>${t.name}</div>
                </div>
                <div style="margin-bottom:16px;">
                    <label>模板类型:</label>
                    <div>${t.type}</div>
                </div>
                <div style="margin-bottom:16px;">
                    <label>企业微信模板ID:</label>
                    <div>${t.wecom_template_id || '-'}</div>
                </div>
                <div style="margin-bottom:16px;">
                    <label>同步状态:</label>
                    <div>${getStatusText(t.sync_status)}</div>
                </div>
                <div style="margin-bottom:24px;">
                    <label>表单配置 (只读):</label>
                    <pre style="background:#f8fafc;padding:12px;border-radius:6px;font-size:12px;">${JSON.stringify(t.form_config.fields, null, 2)}</pre>
                </div>
                <button class="btn btn-primary" style="width:100%" onclick="syncTemplate('${t.type}')">重新同步</button>
            `;

            document.getElementById('drawer').classList.add('open');
        }

        function closeDrawer() {
            document.getElementById('drawer').classList.remove('open');
        }

        // 同步模板
        async function syncTemplate(templateType) {
            if (!confirm('确定要同步此模板到企业微信吗？')) return;

            try {
                const res = await fetch(`${API_BASE}/templates/${templateType}/sync`, { method: 'POST' });
                const data = await res.json();
                alert(data.message);
                if (data.code === 0) {
                    loadTemplates();
                }
            } catch (e) {
                alert('同步失败: ' + e.message);
            }
        }

        // 鉴权配置
        function openAuthModal() {
            document.getElementById('authModal').classList.add('open');
            // 加载现有配置
            fetch(`${API_BASE}/auth/wecom`)
                .then(r => r.json())
                .then(d => {
                    if (d.data) {
                        document.getElementById('corpid').value = d.data.corpid;
                        document.getElementById('agentid').value = d.data.agentid;
                    }
                });
        }

        function closeAuthModal() {
            document.getElementById('authModal').classList.remove('open');
        }

        async function saveAuth() {
            const data = {
                platform: 'wecom',
                corpid: document.getElementById('corpid').value,
                secret: document.getElementById('secret').value,
                agentid: document.getElementById('agentid').value
            };

            try {
                const res = await fetch(`${API_BASE}/auth`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                alert(result.message);
                if (result.code === 0) {
                    closeAuthModal();
                }
            } catch (e) {
                alert('保存失败: ' + e.message);
            }
        }

        // 初始化
        loadTemplates();
    </script>
</body>
</html>
```

- [ ] **Step 2: 提交**

```bash
git add prototype/approval-template-management.html
git commit -m "feat: add approval template management page prototype"
```

---

## Task 7: 集成测试

**Files:**
- Create: `backend/tests/approval/test_template_api.py`

- [ ] **Step 1: 创建测试文件**

```python
import pytest
from unittest.mock import Mock, patch
from approval.services.template_sync import build_wecom_template_content

def test_build_wecom_template_content():
    """测试将表单配置转换为企业微信格式"""
    form_config = {
        "name": "测试模板",
        "fields": [
            {"id": "1", "name": "申请人", "type": "text"},
            {"id": "2", "name": "金额", "type": "number"},
            {"id": "3", "name": "类型", "type": "radio", "options": ["A", "B"]}
        ]
    }

    result = build_wecom_template_content(form_config)

    assert "template_name" in result
    assert "template_content" in result
    assert len(result["template_content"]["controls"]) == 3

    # 验证第一个字段
    control1 = result["template_content"]["controls"][0]
    assert control1["property"]["control"] == "Text"
    assert control1["property"]["title"][0]["text"] == "申请人"

    # 验证单选字段
    control3 = result["template_content"]["controls"][2]
    assert control3["property"]["control"] == "Selector"
    assert "selector" in control3["config"]
```

- [ ] **Step 2: 运行测试**

```bash
cd backend
PYTHONPATH=/Users/athur/PycharmProjects/qyy/backend pytest tests/approval/test_template_api.py -v
```

- [ ] **Step 3: 提交**

```bash
git add backend/tests/approval/test_template_api.py
git commit -m "test: add template sync tests"
```

---

## 实现检查清单

| 任务 | 描述 | 状态 |
|-----|------|-----|
| Task 1 | 数据模型 - 审批模板 | - [ ] |
| Task 2 | 内置模板配置 | - [ ] |
| Task 3 | API - 模板列表 | - [ ] |
| Task 4 | API - 鉴权配置 | - [ ] |
| Task 5 | API - 同步操作 | - [ ] |
| Task 6 | 前端页面 | - [ ] |
| Task 7 | 集成测试 | - [ ] |
