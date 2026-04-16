from sqlalchemy import Column, BigInteger, String, DateTime, JSON
from backend.approval.models.base import Base
import enum
from datetime import datetime


class ApprovalStatus(str, enum.Enum):
    PENDING = "PENDING"           # 待审批
    APPROVED = "APPROVED"         # 已审批
    REJECTED = "REJECTED"         # 已拒绝
    CANCELLED = "CANCELLED"       # 已撤回

class Platform(str, enum.Enum):
    WECOM = "wecom"
    DINGTALK = "dingtalk"

class ApprovalRecord(Base):
    __tablename__ = "approval_record"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_type = Column(String(50), nullable=False, index=True)  # 单据类型
    document_id = Column(BigInteger, nullable=False, index=True)     # 青阳云原始单据ID
    platform = Column(String(20), nullable=False)                  # 平台
    platform_instance_id = Column(String(100), nullable=False, unique=True)  # 第三方审批实例ID
    applicant_mobile = Column(String(20), nullable=False)           # 申请人手机号
    applicant_name = Column(String(100))                           # 申请人姓名
    status = Column(String(20), nullable=False, default=ApprovalStatus.PENDING)
    push_time = Column(DateTime, default=datetime.now)              # 推送时间
    callback_time = Column(DateTime, nullable=True)                 # 回调时间
    form_data = Column(JSON)                                       # 推送时提交的表单数据
    result_data = Column(JSON, nullable=True)                      # 回调时接收的表单结果
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
