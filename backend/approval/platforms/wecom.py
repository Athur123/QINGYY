import hashlib
import time
from typing import Dict, Any, List

import httpx

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
        token = self._get_access_token()
        url = "https://qyapi.weixin.qq.com/cgi-bin/user/getuserid"
        resp = httpx.post(url, params={"access_token": token}, json={"mobile": mobile})
        data = resp.json()
        if data.get("errcode") != 0:
            raise Exception(f"Failed to get userid by mobile: {data}")
        return data["userid"]

    def _get_approvers(self, form_data: ApprovalFormData) -> List[str]:
        """获取审批人列表 - 实际从配置或流程获取"""
        # TODO: 根据业务逻辑确定审批人
        return []

    def query_approval_status(self, instance_id: str) -> ApprovalResult:
        """查询审批状态"""
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
        callback_token = getattr(self.config, 'callback_token', '') or getattr(self.config, 'secret', '')
        timestamp = request_data.get("timestamp", "")
        nonce = request_data.get("nonce", "")

        sort_str = sorted([callback_token, timestamp, nonce])
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
