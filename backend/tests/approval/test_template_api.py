"""
Standalone test for build_wecom_template_content function.
This test bypasses the package import machinery to test the function directly.
"""
import sys
import os

# Load and execute template_sync.py content directly to get the function
template_sync_path = os.path.join(os.path.dirname(__file__), '../../approval/services/template_sync.py')

# Read the file
with open(template_sync_path, 'r') as f:
    content = f.read()

# Replace the backend import with a mock
content = content.replace('from backend.approval.config import load_config, get_builtin_template', '''
# Mock config for testing
def load_config():
    class MockConfig:
        class MockWecom:
            corp_id = "test_corp_id"
            secret = "test_secret"
            agent_id = "test_agent_id"
        wecom = MockWecom()
    return MockConfig()

def get_builtin_template(template_type):
    from backend.approval.config import get_builtin_template as _get
    return _get(template_type)
''')

# Execute in a clean namespace
namespace = {}
exec(content, namespace)
build_wecom_template_content = namespace['build_wecom_template_content']

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

def test_build_wecom_template_content_date():
    """测试日期字段转换"""
    form_config = {
        "name": "考勤审批单",
        "fields": [
            {"id": "1", "name": "开始时间", "type": "date"}
        ]
    }

    result = build_wecom_template_content(form_config)
    control = result["template_content"]["controls"][0]
    assert control["property"]["control"] == "Date"

def test_build_wecom_template_content_textarea():
    """测试多行文本字段转换"""
    form_config = {
        "name": "财务单",
        "fields": [
            {"id": "1", "name": "摘要", "type": "textarea"}
        ]
    }

    result = build_wecom_template_content(form_config)
    control = result["template_content"]["controls"][0]
    assert control["property"]["control"] == "Textarea"


if __name__ == "__main__":
    test_build_wecom_template_content()
    test_build_wecom_template_content_date()
    test_build_wecom_template_content_textarea()
    print("All tests passed!")
