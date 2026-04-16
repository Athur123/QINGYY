import time
import hmac
import hashlib
import base64
from typing import Dict, Any

import httpx

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
        secret = self.config.callback_secret
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
