import pytest
from unittest.mock import Mock, patch
from approval.platforms.wecom import WeComAdapter

def test_verify_callback_valid_signature():
    """测试企业微信回调验签"""
    with patch('approval.platforms.wecom.load_config') as mock_config:
        mock_config.return_value.wecom.callback_token = "test_token"
        adapter = WeComAdapter()

        request_data = {"timestamp": "123", "nonce": "456"}
        # 手动计算正确签名
        import hashlib
        sort_str = sorted(["test_token", "123", "456"])
        correct_sig = hashlib.sha1("".join(sort_str).encode()).hexdigest()

        assert adapter.verify_callback(request_data, correct_sig) == True

def test_parse_callback_approval_finish():
    """测试解析审批完成回调"""
    with patch('approval.platforms.wecom.load_config') as mock_config:
        mock_config.return_value.wecom.callback_token = "test_token"
        adapter = WeComAdapter()

        request_data = {
            "Event": "approval_chain_finish",
            "InstanceId": "instance_123",
            "ApprovalStatus": 2  # 已通过
        }

        result = adapter.parse_callback(request_data)

        assert result.instance_id == "instance_123"
        assert result.status == "APPROVED"

def test_parse_callback_rejected():
    """测试解析审批拒绝回调"""
    with patch('approval.platforms.wecom.load_config') as mock_config:
        mock_config.return_value.wecom.callback_token = "test_token"
        adapter = WeComAdapter()

        request_data = {
            "Event": "approval_chain_finish",
            "InstanceId": "instance_456",
            "ApprovalStatus": 3  # 已拒绝
        }

        result = adapter.parse_callback(request_data)

        assert result.instance_id == "instance_456"
        assert result.status == "REJECTED"
