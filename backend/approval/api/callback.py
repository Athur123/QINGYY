from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from approval.models import ApprovalRecord, ApprovalStatus
from approval.services import ApprovalPushService

router = APIRouter()


def get_db():
    # TODO: 从数据库连接池获取session
    pass


class CallbackResponse(BaseModel):
    code: int
    message: str


@router.post("/callback/{platform}", response_model=CallbackResponse)
async def receive_callback(
    platform: str,
    request: Request,
    db: Session = Depends(get_db)
):
    body = await request.json()
    service = ApprovalPushService(db)
    adapter = service.get_adapter(platform)

    if not adapter:
        raise HTTPException(status_code=400, detail=f"Unknown platform: {platform}")

    # 验签
    signature = request.headers.get("x-wecom-signature") or request.headers.get("x-dingtalk-signature", "")
    if not adapter.verify_callback(body, signature):
        raise HTTPException(status_code=403, detail="Invalid signature")

    # 解析回调
    result = adapter.parse_callback(body)
    if not result:
        return CallbackResponse(code=0, message="received")

    # 更新审批记录
    record = db.query(ApprovalRecord).filter(
        ApprovalRecord.platform_instance_id == result.instance_id,
        ApprovalRecord.platform == platform
    ).first()

    if record:
        record.status = ApprovalStatus(result.status)
        record.callback_time = datetime.now()
        record.result_data = result.form_fields
        db.commit()

    return CallbackResponse(code=0, message="success")
