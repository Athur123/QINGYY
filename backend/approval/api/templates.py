from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.approval.models import ApprovalTemplate
from backend.approval.config import get_all_builtin_templates, get_builtin_template

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class TemplateResponse(BaseModel):
    id: Optional[int]
    name: str
    type: str
    platform: str
    wecom_template_id: Optional[str]
    form_config: dict
    sync_status: str
    auto_sync: bool
    last_sync_time: Optional[str]
    created_at: Optional[str]

class TemplateListResponse(BaseModel):
    code: int
    message: str
    data: List[TemplateResponse]

@router.get("/templates", response_model=TemplateListResponse)
def list_templates(
    type: Optional[str] = None,
    platform: Optional[str] = None,
    sync_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取模板列表，支持按type、platform、sync_status过滤"""
    builtins = get_all_builtin_templates()
    templates = []

    for template_type, config in builtins.items():
        # 按type过滤
        if type and template_type != type:
            continue

        # 按platform过滤
        if platform and config.get("platform") != platform:
            continue

        # TODO: 查询数据库中的记录（当前使用内置模板）
        # 数据库同步后的模板会替换内置模板
        templates.append({
            "id": None,
            "name": config["name"],
            "type": template_type,
            "platform": config["platform"],
            "wecom_template_id": None,
            "form_config": config,
            "sync_status": sync_status or "unsynced",  # 当前默认unsynced
            "auto_sync": False,
            "last_sync_time": None,
            "created_at": None
        })

    return TemplateListResponse(code=0, message="success", data=templates)

@router.get("/templates/{template_type}", response_model=TemplateResponse)
def get_template(
    template_type: str,
    db: Session = Depends(get_db)
):
    """获取单个模板详情"""
    builtin = get_builtin_template(template_type)
    if not builtin:
        raise HTTPException(status_code=404, detail="Template not found")

    # TODO: 查询数据库中的记录
    return TemplateResponse(
        id=None,
        name=builtin["name"],
        type=template_type,
        platform=builtin["platform"],
        wecom_template_id=None,
        form_config=builtin,
        sync_status="unsynced",
        auto_sync=False,
        last_sync_time=None,
        created_at=None
    )