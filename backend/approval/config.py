import os
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
