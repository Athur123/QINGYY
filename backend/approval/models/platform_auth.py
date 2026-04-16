from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class PlatformAuth(Base):
    """平台鉴权配置"""
    __tablename__ = "platform_auth"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    platform = Column(String(20), nullable=False, unique=True)  # 平台：wecom, dingtalk
    corpid = Column(String(100), nullable=False)                 # 企业ID
    secret = Column(String(500), nullable=False)                  # 应用Secret
    agentid = Column(String(50), nullable=False)                  # 应用AgentId
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
