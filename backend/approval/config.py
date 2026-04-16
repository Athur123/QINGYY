import os
from pydantic import BaseModel
from typing import Dict, Optional


class WeComConfig(BaseModel):
    corp_id: str
    agent_id: str
    secret: str
    callback_token: str = ""  # 企业微信回调Token


class DingTalkConfig(BaseModel):
    app_key: str
    app_secret: str
    callback_secret: str = ""  # 钉钉回调签名密钥


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
            callback_secret=os.getenv("DINGTALK_CALLBACK_SECRET", ""),
        ),
        callback_url=os.getenv("CALLBACK_URL", "https://qy-cloud.com/api/approval/callback"),
    )


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


def get_builtin_template(template_type: str) -> dict:
    """获取内置模板配置"""
    return BUILTIN_TEMPLATES.get(template_type)


def get_all_builtin_templates() -> dict:
    """获取所有内置模板"""
    return BUILTIN_TEMPLATES
