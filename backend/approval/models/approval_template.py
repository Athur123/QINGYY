from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ApprovalTemplate(Base):
    """审批模板"""
    __tablename__ = "approval_template"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)              # 模板名称
    type = Column(String(50), nullable=False, index=True)  # 模板类型
    platform = Column(String(20), nullable=False)          # 平台：wecom, dingtalk
    wecom_template_id = Column(String(100), nullable=True)   # 企业微信模板ID
    form_config = Column(JSON, nullable=False)               # 表单配置（内置）
    sync_status = Column(String(20), default="unsynced")    # 同步状态
    auto_sync = Column(Boolean, default=False)              # 是否自动同步
    last_sync_time = Column(DateTime, nullable=True)        # 最后同步时间
    last_error = Column(Text, nullable=True)                 # 最后错误信息
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
