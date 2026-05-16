---
title: 企业微信/钉钉审批集成实现计划
module: approval
type: plan
status: draft
owner: athur
updated: 2026-05-16
source_of_truth: false
---

# 企业微信/钉钉审批集成实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现青阳云与企业微信/钉钉的审批流程集成，支持推送单据到第三方审批并接收审批结果

**Architecture:** 采用官方SDK+轻量包装模式，定义统一接口 ApprovalPlatform，企业微信和钉钉各实现一套适配器。通过Webhook接收回调，轮询作为兜底。

**Tech Stack:** Python (FastAPI), 企业微信SDK, 钉钉SDK, SQLite/MySQL

---

## 文件结构

```
backend/
├── approval/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置管理
│   ├── models/
│   │   ├── __init__.py
│   │   ├── approval_record.py   # 审批记录模型
│   │   └── field_mapping.py    # 字段映射模型
│   ├── services/
│   │   ├── __init__.py
│   │   ├── approval_push.py     # 统一推送服务
│   │   └── field_mapping.py    # 字段映射服务
│   ├── platforms/
│   │   ├── __init__.py
│   │   ├── base.py             # 平台基类
│   │   ├── wecom.py            # 企业微信适配器
│   │   └── dingtalk.py         # 钉钉适配器
│   ├── api/
│   │   ├── __init__.py
│   │   ├── push.py             # 推送API
│   │   ├── callback.py         # 回调API
│   │   └── status.py           # 状态查询API
│   └── utils/
│       ├── __init__.py
│       └── signature.py        # 验签工具
├── tests/
│   └── approval/
│       ├── test_push.py
│       ├── test_wecom.py
│       └── test_dingtalk.py
└── requirements.txt
```

---

## Task 1: 项目初始化和配置

**Files:**
- Create: `backend/requirements.txt`
- Create: `backend/approval/__init__.py`
- Create: `backend/approval/config.py`
- Create: `backend/approval/main.py`

- [ ] **Step 1: 创建 requirements.txt**

```txt
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.0
python-multipart==0.0.6
# 企业微信
wecom-sdk==1.0.0
# 钉钉
dingtalk-sdk==1.0.0
# 数据库
sqlalchemy==2.0.0
pymysql==1.1.0
# 其他
httpx==0.26.0
cryptography==41.0.0
```

- [ ] **Step 2: 创建 config.py - 配置管理**

```python
from pydantic import BaseModel
from typing import Dict, Optional

class WeComConfig(BaseModel):
    corp_id: str
    agent_id: str
    secret: str

class DingTalkConfig(BaseModel):
    app_key: str
    app_secret: str

class PlatformConfig(BaseModel):
    wecom: WeComConfig
    dingtalk: DingTalkConfig

    callback_url: str  # 青阳云暴露给第三方的回调地址

def load_config() -> PlatformConfig:
    # 从环境变量或配置文件加载
    return PlatformConfig(
        wecom=WeComConfig(
            corp_id=os.getenv("WECOM_CORP_ID", ""),
            agent_id=os.getenv("WECOM_AGENT_ID", ""),
            secret=os.getenv("WECOM_SECRET", ""),
        ),
        dingtalk=DingTalkConfig(
            app_key=os.getenv("DINGTALK_APP_KEY", ""),
            app_secret=os.getenv("DINGTALK_APP_SECRET", ""),
        ),
        callback_url=os.getenv("CALLBACK_URL", "https://qy-cloud.com/api/approval/callback"),
    )
```

- [ ] **Step 3: 创建 main.py - FastAPI 入口**

```python
from fastapi import FastAPI
from approval.api import push, callback, status

app = FastAPI(title="青阳云审批集成服务")

app.include_router(push.router, prefix="/api/approval", tags=["推送"])
app.include_router(callback.router, prefix="/api/approval", tags=["回调"])
app.include_router(status.router, prefix="/api/approval", tags=["状态"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

- [ ] **Step 4: 运行验证**

```bash
cd backend && pip install -r requirements.txt
uvicorn approval.main:app --reload --port 8000
curl http://localhost:8000/health
# 预期: {"status":"ok"}
```

- [ ] **Step 5: 提交**

```bash
git add backend/requirements.txt backend/approval/
git commit -m "feat: init approval integration backend structure"
```

---

## Task 2: 数据模型

**Files:**
- Create: `backend/approval/models/__init__.py`
- Create: `backend/approval/models/approval_record.py`
- Create: `backend/approval/models/field_mapping.py`

- [ ] **Step 1: 创建 approval_record.py - 审批记录模型**

```python
from sqlalchemy import Column, BigInteger, String, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"           # 待审批
    APPROVED = "APPROVED"         # 已审批
    REJECTED = "REJECTED"         # 已拒绝
    CANCELLED = "CANCELLED"       # 已撤回

class Platform(str, enum.Enum):
    WECOM = "wecom"
    DINGTALK = "dingtalk"

class ApprovalRecord(Base):
    __tablename__ = "approval_record"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_type = Column(String(50), nullable=False, index=True)  # 单据类型
    document_id = Column(BigInteger, nullable=False, index=True)     # 青阳云原始单据ID
    platform = Column(String(20), nullable=False)                    # 平台
    platform_instance_id = Column(String(100), nullable=False, unique=True)  # 第三方审批实例ID
    applicant_mobile = Column(String(20), nullable=False)           # 申请人手机号
    applicant_name = Column(String(100))                             # 申请人姓名
    status = Column(String(20), nullable=False, default=ApprovalStatus.PENDING)
    push_time = Column(DateTime, default=datetime.now)              # 推送时间
    callback_time = Column(DateTime, nullable=True)                  # 回调时间
    form_data = Column(JSON)                                         # 推送时提交的表单数据
    result_data = Column(JSON, nullable=True)                        # 回调时接收的表单结果
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
```

- [ ] **Step 2: 创建 field_mapping.py - 字段映射模型**

```python
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class FieldMappingConfig(Base):
    __tablename__ = "field_mapping_config"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_type = Column(String(50), nullable=False, index=True)
    platform = Column(String(20), nullable=False)
    qy_field = Column(String(100), nullable=False)      # 青阳云字段名
    third_party_field = Column(String(100), nullable=False)  # 第三方表单字段名
    required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
```

- [ ] **Step 3: 创建 models/__init__.py**

```python
from approval.models.approval_record import ApprovalRecord, ApprovalStatus, Platform
from approval.models.field_mapping import FieldMappingConfig

__all__ = ["ApprovalRecord", "ApprovalStatus", "Platform", "FieldMappingConfig"]
```

- [ ] **Step 4: 创建数据库表并验证**

```bash
# 创建临时脚本验证模型
python -c "
from approval.models import ApprovalRecord, FieldMappingConfig
print('Models imported successfully')
print(f'ApprovalRecord fields: {[c.name for c in ApprovalRecord.__table__.columns]}')
"
```

- [ ] **Step 5: 提交**

```bash
git add backend/approval/models/
git commit -m "feat: add approval record and field mapping models"
```

---

## Task 3: 平台适配器基类

**Files:**
- Create: `backend/approval/platforms/__init__.py`
- Create: `backend/approval/platforms/base.py`

- [ ] **Step 1: 创建 base.py - 平台基类**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel

class ApprovalFormData(BaseModel):
    """审批表单数据"""
    applicant_name: str
    applicant_mobile: str
    fields: Dict[str, Any]  # 表单字段名 -> 值

class ApprovalResult(BaseModel):
    """审批结果"""
    instance_id: str
    status: str  # APPROVED / REJECTED
    approver: Optional[str] = None
    comment: Optional[str] = None
    form_fields: Optional[Dict[str, Any]] = None

class ApprovalPlatform(ABC):
    """审批平台抽象基类"""

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """平台名称: wecom / dingtalk"""
        pass

    @abstractmethod
    def push_approval(self, form_data: ApprovalFormData, callback_url: str) -> str:
        """
        推送审批到第三方平台
        Returns: 第三方审批实例ID
        """
        pass

    @abstractmethod
    def query_approval_status(self, instance_id: str) -> ApprovalResult:
        """查询审批状态"""
        pass

    @abstractmethod
    def verify_callback(self, request_data: Dict, signature: str) -> bool:
        """验证回调签名"""
        pass

    @abstractmethod
    def parse_callback(self, request_data: Dict) -> ApprovalResult:
        """解析回调数据"""
        pass
```

- [ ] **Step 2: 创建 platforms/__init__.py**

```python
from approval.platforms.base import ApprovalPlatform, ApprovalFormData, ApprovalResult

__all__ = ["ApprovalPlatform", "ApprovalFormData", "ApprovalResult"]
```

- [ ] **Step 3: 验证基类可导入**

```bash
python -c "
from approval.platforms import ApprovalPlatform, ApprovalFormData, ApprovalResult
print('Base classes imported successfully')
"
```

- [ ] **Step 4: 提交**

```bash
git add backend/approval/platforms/
git commit -m "feat: add approval platform base class"
```

---

## Task 4: 企业微信适配器

**Files:**
- Create: `backend/approval/platforms/wecom.py`

- [ ] **Step 1: 创建 wecom.py - 企业微信适配器**

```python
import hashlib
import time
from typing import Dict, Any
from approval.platforms.base import ApprovalPlatform, ApprovalFormData, ApprovalResult
from approval.config import load_config

class WeComAdapter(ApprovalPlatform):
    """企业微信审批适配器"""

    def __init__(self):
        self.config = load_config().wecom
        self.token_cache = {}

    @property
    def platform_name(self) -> str:
        return "wecom"

    def _get_access_token(self) -> str:
        """获取access_token，带缓存"""
        cache_key = "wecom_access_token"
        if cache_key in self.token_cache:
            cached = self.token_cache[cache_key]
            if cached["expire_time"] > time.time():
                return cached["token"]

        # 调用企业微信API获取token
        import httpx
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {"corpid": self.config.corp_id, "corpsecret": self.config.secret}
        resp = httpx.get(url, params=params)
        data = resp.json()

        if data.get("errcode") != 0:
            raise Exception(f"Failed to get access_token: {data}")

        token = data["access_token"]
        self.token_cache[cache_key] = {
            "token": token,
            "expire_time": time.time() + 7000  # 提前3分钟过期
        }
        return token

    def push_approval(self, form_data: ApprovalFormData, callback_url: str) -> str:
        """推送审批到企业微信"""
        import httpx

        token = self._get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/approvalapi/create_approval"

        # 构建审批表单数据
        # 注意：具体字段结构需要参考企业微信审批接口文档
        payload = {
            "creator_userid": self._get_userid_by_mobile(form_data.applicant_mobile),
            "approver": self._get_approvers(form_data),
            "notifyer": [],
            "form_data": [
                {"id": "name", "title": "申请人", "value": form_data.applicant_name},
                {"id": "mobile", "title": "手机号", "value": form_data.applicant_mobile},
            ],
        }

        # 添加表单字段
        for field_name, field_value in form_data.fields.items():
            payload["form_data"].append({
                "id": field_name,
                "title": field_name,
                "value": str(field_value)
            })

        resp = httpx.post(
            url,
            params={"access_token": token},
            json=payload
        )
        data = resp.json()

        if data.get("errcode") != 0:
            raise Exception(f"Failed to push approval: {data}")

        return data["instance_id"]

    def _get_userid_by_mobile(self, mobile: str) -> str:
        """根据手机号获取企业微信用户ID"""
        import httpx
        token = self._get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserid"
        resp = httpx.post(url, params={"access_token": token}, json={"mobile": mobile})
        data = resp.json()
        if data.get("errcode") != 0:
            raise Exception(f"Failed to get userid by mobile: {data}")
        return data["userid"]

    def _get_approvers(self, form_data: ApprovalFormData) -> list:
        """获取审批人列表 - 实际从配置或流程获取"""
        # TODO: 根据业务逻辑确定审批人
        return []

    def query_approval_status(self, instance_id: str) -> ApprovalResult:
        """查询审批状态"""
        import httpx
        token = self._get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/approval/getinstanceinfo"
        resp = httpx.get(
            url,
            params={"access_token": token, "approval_id": instance_id}
        )
        data = resp.json()

        if data.get("errcode") != 0:
            raise Exception(f"Failed to query approval: {data}")

        info = data.get("info", {})
        status = info.get("status", 0)
        # 企业微信状态: 1=审批中, 2=已通过, 3=已拒绝, 4=已取消
        status_map = {1: "PENDING", 2: "APPROVED", 3: "REJECTED", 4: "CANCELLED"}

        return ApprovalResult(
            instance_id=instance_id,
            status=status_map.get(status, "UNKNOWN"),
            form_fields=info.get("form_data", [])
        )

    def verify_callback(self, request_data: Dict, signature: str) -> bool:
        """验证企业微信回调签名"""
        # 企业微信回调验签逻辑
        token = self.config.get("callback_token", "")
        timestamp = request_data.get("timestamp", "")
        nonce = request_data.get("nonce", "")

        sort_str = sorted([token, timestamp, nonce])
        sha1 = hashlib.sha1("".join(sort_str).encode()).hexdigest()

        return sha1 == signature

    def parse_callback(self, request_data: Dict) -> ApprovalResult:
        """解析企业微信回调数据"""
        event = request_data.get("Event", "")
        if event == "approval_chain_finish":
            return ApprovalResult(
                instance_id=request_data.get("InstanceId", ""),
                status="APPROVED" if request_data.get("ApprovalStatus") == 2 else "REJECTED",
            )
        return None
```

- [ ] **Step 2: 验证代码语法**

```bash
python -m py_compile backend/approval/platforms/wecom.py && echo "Syntax OK"
```

- [ ] **Step 3: 提交**

```bash
git add backend/approval/platforms/wecom.py
git commit -m "feat: add WeCom approval adapter"
```

---

## Task 5: 钉钉适配器

**Files:**
- Create: `backend/approval/platforms/dingtalk.py`

- [ ] **Step 1: 创建 dingtalk.py - 钉钉适配器**

```python
import time
from typing import Dict, Any
from approval.platforms.base import ApprovalPlatform, ApprovalFormData, ApprovalResult
from approval.config import load_config

class DingTalkAdapter(ApprovalPlatform):
    """钉钉审批适配器"""

    def __init__(self):
        self.config = load_config().dingtalk
        self.token_cache = {}

    @property
    def platform_name(self) -> str:
        return "dingtalk"

    def _get_access_token(self) -> str:
        """获取access_token"""
        cache_key = "dingtalk_access_token"
        if cache_key in self.token_cache:
            cached = self.token_cache[cache_key]
            if cached["expire_time"] > time.time():
                return cached["token"]

        import httpx
        url = "https://api.dingtalk.com/v1.0/oauth2/accessToken"
        resp = httpx.post(url, json={"appKey": self.config.app_key, "appSecret": self.config.app_secret})
        data = resp.json()

        if data.get("errCode") != 0:
            raise Exception(f"Failed to get access_token: {data}")

        token = data["accessToken"]
        self.token_cache[cache_key] = {
            "token": token,
            "expire_time": time.time() + 7000
        }
        return token

    def push_approval(self, form_data: ApprovalFormData, callback_url: str) -> str:
        """推送审批到钉钉"""
        import httpx

        token = self._get_access_token()
        url = "https://api.dingtalk.com/v1.0/approval/create"

        payload = {
            "process_code": self._get_process_code(form_data),
            "originator_user_id": self._get_userid_by_mobile(form_data.applicant_mobile),
            "dept_id": 1,
            "form_data": [
                {"name": "申请人", "value": form_data.applicant_name},
                {"name": "手机号", "value": form_data.applicant_mobile},
            ],
        }

        # 添加表单字段
        for field_name, field_value in form_data.fields.items():
            payload["form_data"].append({
                "name": field_name,
                "value": str(field_value)
            })

        resp = httpx.post(
            url,
            headers={"x-acs-dingtalk-access-token": token},
            json=payload
        )
        data = resp.json()

        if data.get("errCode") != 0:
            raise Exception(f"Failed to push approval: {data}")

        return data["process_instance_id"]

    def _get_process_code(self, form_data: ApprovalFormData) -> str:
        """获取流程码 - 实际从配置或单据类型获取"""
        # TODO: 根据单据类型映射到钉钉流程码
        return "PROC-XXX"

    def _get_userid_by_mobile(self, mobile: str) -> str:
        """根据手机号获取钉钉用户ID"""
        import httpx
        token = self._get_access_token()
        url = "https://api.dingtalk.com/v1.0/contact/users/query"
        resp = httpx.post(
            url,
            headers={"x-acs-dingtalk-access-token": token},
            json={"mobile": mobile}
        )
        data = resp.json()
        if data.get("errCode") != 0:
            raise Exception(f"Failed to get userid by mobile: {data}")
        return data["id"]

    def query_approval_status(self, instance_id: str) -> ApprovalResult:
        """查询审批状态"""
        import httpx
        token = self._get_access_token()
        url = f"https://api.dingtalk.com/v1.0/approval/instances/{instance_id}"
        resp = httpx.get(url, headers={"x-acs-dingtalk-access-token": token})
        data = resp.json()

        if data.get("errCode") != 0:
            raise Exception(f"Failed to query approval: {data}")

        status_map = {"COMPLETED": "APPROVED", "TERMINATED": "REJECTED"}

        return ApprovalResult(
            instance_id=instance_id,
            status=status_map.get(data.get("status", ""), "PENDING"),
            form_fields=data.get("form_data", [])
        )

    def verify_callback(self, request_data: Dict, signature: str) -> bool:
        """验证钉钉回调签名"""
        # 钉钉回调验签逻辑
        import hmac
        import hashlib
        import base64

        secret = self.config.get("callback_secret", "")
        timestamp = request_data.get("timestamp", "")
        sign_str = f"{timestamp}\n{secret}"
        encoded = base64.b64encode(
            hmac.new(secret.encode(), sign_str.encode(), digestmod=hashlib.sha256).digest()
        ).decode()

        return encoded == signature

    def parse_callback(self, request_data: Dict) -> ApprovalResult:
        """解析钉钉回调数据"""
        event_type = request_data.get("eventType", "")
        if event_type == "approval_instance_finish":
            instance_id = request_data.get("processInstanceId", "")
            # 钉钉回调不包含状态，需要主动查询
            return ApprovalResult(instance_id=instance_id, status="PENDING")
        return None
```

- [ ] **Step 2: 验证代码语法**

```bash
python -m py_compile backend/approval/platforms/dingtalk.py && echo "Syntax OK"
```

- [ ] **Step 3: 提交**

```bash
git add backend/approval/platforms/dingtalk.py
git commit -m "feat: add DingTalk approval adapter"
```

---

## Task 6: 统一推送服务

**Files:**
- Create: `backend/approval/services/__init__.py`
- Create: `backend/approval/services/approval_push.py`
- Create: `backend/approval/services/field_mapping.py`

- [ ] **Step 1: 创建 field_mapping.py - 字段映射服务**

```python
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from approval.models import FieldMappingConfig

class FieldMappingService:
    """字段映射服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_mappings(self, document_type: str, platform: str) -> List[Dict[str, Any]]:
        """获取指定单据类型和平台的字段映射配置"""
        configs = self.db.query(FieldMappingConfig).filter(
            FieldMappingConfig.document_type == document_type,
            FieldMappingConfig.platform == platform
        ).all()

        return [
            {
                "qy_field": c.qy_field,
                "third_party_field": c.third_party_field,
                "required": c.required
            }
            for c in configs
        ]

    def map_to_third_party(self, document_type: str, platform: str, qy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将青阳云字段数据映射到第三方格式
        qy_data: {"amount": 1000, "payee": "xxx", ...}
        返回: {"amount": 1000, "payee_name": "xxx", ...}
        """
        mappings = self.get_mappings(document_type, platform)
        result = {}

        for mapping in mappings:
            qy_field = mapping["qy_field"]
            tp_field = mapping["third_party_field"]
            if qy_field in qy_data:
                result[tp_field] = qy_data[qy_field]

        return result

    def map_to_qy(self, document_type: str, platform: str, tp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将第三方字段数据映射回青阳云格式
        """
        mappings = self.get_mappings(document_type, platform)
        result = {}

        for mapping in mappings:
            qy_field = mapping["qy_field"]
            tp_field = mapping["third_party_field"]
            if tp_field in tp_data:
                result[qy_field] = tp_data[tp_field]

        return result
```

- [ ] **Step 2: 创建 approval_push.py - 统一推送服务**

```python
from typing import Optional
from sqlalchemy.orm import Session
from approval.platforms import ApprovalPlatform, ApprovalFormData
from approval.platforms.wecom import WeComAdapter
from approval.platforms.dingtalk import DingTalkAdapter
from approval.models import ApprovalRecord, Platform, ApprovalStatus
from approval.services.field_mapping import FieldMappingService

class ApprovalPushService:
    """统一审批推送服务"""

    def __init__(self, db: Session):
        self.db = db
        self.platforms = {
            "wecom": WeComAdapter(),
            "dingtalk": DingTalkAdapter()
        }

    def push(
        self,
        document_type: str,
        document_id: int,
        platform: str,
        applicant_mobile: str,
        applicant_name: str,
        form_data: dict,
        callback_url: str
    ) -> ApprovalRecord:
        """
        推送审批到第三方平台
        """
        # 获取平台适配器
        adapter = self.platforms.get(platform)
        if not adapter:
            raise ValueError(f"Unknown platform: {platform}")

        # 获取字段映射
        mapping_service = FieldMappingService(self.db)
        tp_fields = mapping_service.map_to_third_party(document_type, platform, form_data)

        # 构建表单数据
        approval_form = ApprovalFormData(
            applicant_name=applicant_name,
            applicant_mobile=applicant_mobile,
            fields=tp_fields
        )

        # 推送到第三方平台
        instance_id = adapter.push_approval(approval_form, callback_url)

        # 保存审批记录
        record = ApprovalRecord(
            document_type=document_type,
            document_id=document_id,
            platform=platform,
            platform_instance_id=instance_id,
            applicant_mobile=applicant_mobile,
            applicant_name=applicant_name,
            status=ApprovalStatus.PENDING,
            form_data=form_data
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def get_adapter(self, platform: str) -> Optional[ApprovalPlatform]:
        return self.platforms.get(platform)
```

- [ ] **Step 3: 创建 services/__init__.py**

```python
from approval.services.approval_push import ApprovalPushService
from approval.services.field_mapping import FieldMappingService

__all__ = ["ApprovalPushService", "FieldMappingService"]
```

- [ ] **Step 4: 验证导入**

```bash
python -c "
from approval.services import ApprovalPushService, FieldMappingService
print('Services imported successfully')
"
```

- [ ] **Step 5: 提交**

```bash
git add backend/approval/services/
git commit -m "feat: add approval push and field mapping services"
```

---

## Task 7: API 接口

**Files:**
- Create: `backend/approval/api/__init__.py`
- Create: `backend/approval/api/push.py`
- Create: `backend/approval/api/callback.py`
- Create: `backend/approval/api/status.py`

- [ ] **Step 1: 创建 push.py - 推送API**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.services import ApprovalPushService
from approval.config import load_config

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class PushRequest(BaseModel):
    document_type: str
    document_id: int
    platform: str  # wecom / dingtalk / auto
    applicant_mobile: str
    applicant_name: str
    form_data: dict

class PushResponse(BaseModel):
    code: int
    message: str
    data: dict

@router.post("/push", response_model=PushResponse)
def push_approval(
    request: PushRequest,
    db: Session = Depends(get_db)
):
    config = load_config()
    service = ApprovalPushService(db)

    try:
        # 如果platform是auto，选择默认平台
        platform = request.platform
        if platform == "auto":
            platform = "wecom"  # 默认企业微信

        record = service.push(
            document_type=request.document_type,
            document_id=request.document_id,
            platform=platform,
            applicant_mobile=request.applicant_mobile,
            applicant_name=request.applicant_name,
            form_data=request.form_data,
            callback_url=config.callback_url
        )

        return PushResponse(
            code=0,
            message="success",
            data={
                "approval_id": record.id,
                "platform": record.platform,
                "instance_id": record.platform_instance_id,
                "status": record.status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
```

- [ ] **Step 2: 创建 callback.py - 回调API**

```python
from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.models import ApprovalRecord, ApprovalStatus
from approval.services import ApprovalPushService

router = APIRouter()

class CallbackResponse(BaseModel):
    code: int
    message: str

@router.post("/callback/{platform}", response_model=CallbackResponse)
async def receive_callback(
    platform: str,
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.json()
    service = ApprovalPushService(db)
    adapter = service.get_adapter(platform)

    if not adapter:
        raise HTTPException(status_code=400, detail=f"Unknown platform: {platform}")

    # 验签
    signature = request.headers.get("x-wecom-signature") or request.headers.get("x-dingtalk-signature", "")
    if not adapter.verify_callback(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # 解析回调
    result = adapter.parse_callback(body)
    if not result:
        return CallbackResponse(code=0, message="received")

    # 更新审批记录
    record = db.query(ApprovalRecord).filter(
        ApprovalRecord.platform_instance_id == result.instance_id,
        ApprovalRecord.platform == platform
    ).first()

    if record:
        record.status = ApprovalStatus(result.status)
        record.callback_time = datetime.now()
        record.result_data = result.form_fields
        db.commit()

    return CallbackResponse(code=0, message="success")
```

- [ ] **Step 3: 创建 status.py - 状态查询API**

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.models import ApprovalRecord
from approval.services import ApprovalPushService

router = APIRouter()

class StatusResponse(BaseModel):
    code: int
    message: str
    data: dict

@router.get("/status/{approval_id}", response_model=StatusResponse)
def get_approval_status(
    approval_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(ApprovalRecord).filter(
        ApprovalRecord.id == approval_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Approval not found")

    return StatusResponse(
        code=0,
        message="success",
        data={
            "approval_id": record.id,
            "status": record.status,
            "platform": record.platform,
            "instance_id": record.platform_instance_id,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        }
    )
```

- [ ] **Step 4: 创建 api/__init__.py**

```python
from approval.api.push import router as push_router
from approval.api.callback import router as callback_router
from approval.api.status import router as status_router

__all__ = ["push_router", "callback_router", "status_router"]
```

- [ ] **Step 5: 验证语法**

```bash
python -m py_compile backend/approval/api/*.py && echo "All API files syntax OK"
```

- [ ] **Step 6: 提交**

```bash
git add backend/approval/api/
git commit -m "feat: add approval API endpoints"
```

---

## Task 8: 轮询任务（兜底机制）

**Files:**
- Create: `backend/approval/jobs/__init__.py`
- Create: `backend/approval/jobs/poll_pending.py`

- [ ] **Step 1: 创建 poll_pending.py - 轮询待处理审批**

```python
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from approval.models import ApprovalRecord, ApprovalStatus
from approval.services import ApprovalPushService

def poll_pending_approvals(db: Session, timeout_minutes: int = 30):
    """
    轮询已推送但超时的审批单，查询最新状态
    """
    service = ApprovalPushService(db)

    # 查找推送超过timeout_minutes且状态仍为PENDING的记录
    cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
    pending_records = db.query(ApprovalRecord).filter(
        ApprovalRecord.status == ApprovalStatus.PENDING,
        ApprovalRecord.push_time < cutoff_time
    ).all()

    for record in pending_records:
        adapter = service.get_adapter(record.platform)
        if not adapter:
            continue

        try:
            result = adapter.query_approval_status(record.platform_instance_id)

            if result.status != "PENDING":
                record.status = ApprovalStatus(result.status)
                record.callback_time = datetime.now()
                record.result_data = result.form_fields
                db.commit()
        except Exception as e:
            # 记录错误但继续处理其他记录
            print(f"Failed to poll approval {record.id}: {e}")
            continue
```

- [ ] **Step 2: 创建 __init__.py**

```python
from approval.jobs.poll_pending import poll_pending_approvals

__all__ = ["poll_pending_approvals"]
```

- [ ] **Step 3: 提交**

```bash
git add backend/approval/jobs/
git commit -m "feat: add polling job for pending approvals"
```

---

## Task 9: 单元测试

**Files:**
- Create: `backend/tests/approval/__init__.py`
- Create: `backend/tests/approval/test_push.py`
- Create: `backend/tests/approval/test_wecom.py`

- [ ] **Step 1: 创建 test_push.py**

```python
import pytest
from unittest.mock import Mock, patch
from approval.services.approval_push import ApprovalPushService
from approval.models import ApprovalRecord

def test_push_creates_record():
    """测试推送创建审批记录"""
    mock_db = Mock()
    mock_db.add = Mock()
    mock_db.commit = Mock()
    mock_db.refresh = Mock()

    with patch('approval.services.approval_push.WeComAdapter') as mock_wecom:
        mock_adapter = Mock()
        mock_adapter.push_approval.return_value = "wecom_instance_123"
        mock_wecom.return_value = mock_adapter

        service = ApprovalPushService(mock_db)
        record = service.push(
            document_type="finance_receivable",
            document_id=1,
            platform="wecom",
            applicant_mobile="13800138000",
            applicant_name="张三",
            form_data={"amount": 1000},
            callback_url="https://callback.com"
        )

        mock_adapter.push_approval.assert_called_once()
        mock_db.add.assert_called_once()
        assert record.platform_instance_id == "wecom_instance_123"
```

- [ ] **Step 2: 创建 test_wecom.py**

```python
import pytest
from unittest.mock import Mock, patch
from approval.platforms.wecom import WeComAdapter

def test_verify_callback_valid_signature():
    """测试企业微信回调验签"""
    adapter = WeComAdapter()

    with patch.object(adapter, 'config', {"callback_token": "test_token"}):
        request_data = {"timestamp": "123", "nonce": "456"}
        # 手动计算正确签名
        import hashlib
        sort_str = sorted(["test_token", "123", "456"])
        correct_sig = hashlib.sha1("".join(sort_str).encode()).hexdigest()

        assert adapter.verify_callback(request_data, correct_sig) == True

def test_parse_callback_approval_finish():
    """测试解析审批完成回调"""
    adapter = WeComAdapter()

    request_data = {
        "Event": "approval_chain_finish",
        "InstanceId": "instance_123",
        "ApprovalStatus": 2  # 已通过
    }

    result = adapter.parse_callback(request_data)

    assert result.instance_id == "instance_123"
    assert result.status == "APPROVED"
```

- [ ] **Step 3: 创建 __init__.py**

```python
# Tests package
```

- [ ] **Step 4: 运行测试**

```bash
cd backend
pytest tests/approval/ -v
```

- [ ] **Step 5: 提交**

```bash
git add backend/tests/
git commit -m "test: add approval integration unit tests"
```

---

## Task 10: 集成测试（手动验证）

**Files:**
- Create: `backend/TESTING.md`

- [ ] **Step 1: 创建测试文档**

```markdown
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
export DINGTALK_APP_KEY=xxx
export DINGTALK_APP_SECRET=xxx
export CALLBACK_URL=https://your-domain.com/api/approval/callback
```

### 2. 启动服务

```bash
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
```

- [ ] **Step 2: 提交**

```bash
git add backend/TESTING.md
git commit -m "docs: add integration testing guide"
```

---

## 实现检查清单

| 任务 | 描述 | 状态 |
|-----|------|-----|
| Task 1 | 项目初始化和配置 | - [ ] |
| Task 2 | 数据模型 | - [ ] |
| Task 3 | 平台适配器基类 | - [ ] |
| Task 4 | 企业微信适配器 | - [ ] |
| Task 5 | 钉钉适配器 | - [ ] |
| Task 6 | 统一推送服务 | - [ ] |
| Task 7 | API接口 | - [ ] |
| Task 8 | 轮询任务 | - [ ] |
| Task 9 | 单元测试 | - [ ] |
| Task 10 | 集成测试文档 | - [ ] |
