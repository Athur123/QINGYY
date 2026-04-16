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