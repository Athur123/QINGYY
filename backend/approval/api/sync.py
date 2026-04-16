from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.approval.models import ApprovalTemplate
from backend.approval.config import get_builtin_template
from backend.approval.services.template_sync import sync_template_to_wecom

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class SyncResponse(BaseModel):
    code: int
    message: str
    data: dict

@router.post("/templates/{template_type}/sync", response_model=SyncResponse)
def sync_template(
    template_type: str,
    db: Session = Depends(get_db)
):
    """同步模板到企业微信"""
    # 获取内置模板配置
    builtin = get_builtin_template(template_type)
    if not builtin:
        raise HTTPException(status_code=404, detail="Template not found")

    try:
        # 同步到企业微信
        template_id = sync_template_to_wecom(template_type, builtin)

        return SyncResponse(
            code=0,
            message="同步成功",
            data={"template_id": template_id}
        )
    except Exception as e:
        return SyncResponse(
            code=1,
            message=f"同步失败: {str(e)}",
            data={}
        )