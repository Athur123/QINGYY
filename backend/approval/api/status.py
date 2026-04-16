from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from approval.models import ApprovalRecord
from approval.services import ApprovalPushService

router = APIRouter()


def get_db():
    # TODO: 从数据库连接池获取session
    pass


class StatusResponse(BaseModel):
    code: int
    message: str
    data: dict


@router.get("/status/{approval_id}", response_model=StatusResponse)
def get_approval_status(
    approval_id: int,
    db: Session = Depends(get_db)
):
    record = db.query(ApprovalRecord).filter(
        ApprovalRecord.id == approval_id
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Approval not found")

    return StatusResponse(
        code=0,
        message="success",
        data={
            "approval_id": record.id,
            "status": record.status,
            "platform": record.platform,
            "instance_id": record.platform_instance_id,
            "updated_at": record.updated_at.isoformat() if record.updated_at else None
        }
    )
