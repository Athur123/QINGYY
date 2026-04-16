import httpx
from typing import Optional
from datetime import datetime
from backend.approval.config import load_config, get_builtin_template

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