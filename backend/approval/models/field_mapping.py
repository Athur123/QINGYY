from sqlalchemy import Column, BigInteger, String, Boolean, DateTime
from backend.approval.models.base import Base
from datetime import datetime

class FieldMappingConfig(Base):
    __tablename__ = "field_mapping_config"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    document_type = Column(String(50), nullable=False, index=True)
    platform = Column(String(20), nullable=False)
    qy_field = Column(String(100), nullable=False)      # 青阳云字段名
    third_party_field = Column(String(100), nullable=False)  # 第三方表单字段名
    required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
