from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.services import ApprovalPushService
from approval.config import load_config

router = APIRouter()


def get_db():
    # TODO: 从数据库连接池获取session
    pass


class PushRequest(BaseModel):
    document_type: str
    document_id: int
    platform: str  # wecom / dingtalk / auto
    applicant_mobile: str
    applicant_name: str
    form_data: dict


class PushResponse(BaseModel):
    code: int
    message: str
    data: dict


@router.post("/push", response_model=PushResponse)
def push_approval(
    request: PushRequest,
    db: Session = Depends(get_db)
):
    config = load_config()
    service = ApprovalPushService(db)

    try:
        # 如果platform是auto，选择默认平台
        platform = request.platform
        if platform == "auto":
            platform = "wecom"  # 默认企业微信

        record = service.push(
            document_type=request.document_type,
            document_id=request.document_id,
            platform=platform,
            applicant_mobile=request.applicant_mobile,
            applicant_name=request.applicant_name,
            form_data=request.form_data,
            callback_url=config.callback_url
        )

        return PushResponse(
            code=0,
            message="success",
            data={
                "approval_id": record.id,
                "platform": record.platform,
                "instance_id": record.platform_instance_id,
                "status": record.status
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
