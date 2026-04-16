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
