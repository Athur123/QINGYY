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