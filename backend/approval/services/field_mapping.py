from typing import Dict, Any, List
from sqlalchemy.orm import Session
from approval.models import FieldMappingConfig


class FieldMappingService:
    """字段映射服务"""

    def __init__(self, db: Session):
        self.db = db

    def get_mappings(self, document_type: str, platform: str) -> List[Dict[str, Any]]:
        """获取指定单据类型和平台的字段映射配置"""
        configs = self.db.query(FieldMappingConfig).filter(
            FieldMappingConfig.document_type == document_type,
            FieldMappingConfig.platform == platform
        ).all()

        return [
            {
                "qy_field": c.qy_field,
                "third_party_field": c.third_party_field,
                "required": c.required
            }
            for c in configs
        ]

    def map_to_third_party(self, document_type: str, platform: str, qy_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将青阳云字段数据映射到第三方格式
        qy_data: {"amount": 1000, "payee": "xxx", ...}
        返回: {"amount": 1000, "payee_name": "xxx", ...}
        """
        mappings = self.get_mappings(document_type, platform)
        result = {}

        for mapping in mappings:
            qy_field = mapping["qy_field"]
            tp_field = mapping["third_party_field"]
            if qy_field in qy_data:
                result[tp_field] = qy_data[qy_field]

        return result

    def map_to_qy(self, document_type: str, platform: str, tp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        将第三方字段数据映射回青阳云格式
        """
        mappings = self.get_mappings(document_type, platform)
        result = {}

        for mapping in mappings:
            qy_field = mapping["qy_field"]
            tp_field = mapping["third_party_field"]
            if tp_field in tp_data:
                result[qy_field] = tp_data[tp_field]

        return result