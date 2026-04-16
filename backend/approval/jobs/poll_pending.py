from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from approval.models import ApprovalRecord, ApprovalStatus
from approval.services import ApprovalPushService

def poll_pending_approvals(db: Session, timeout_minutes: int = 30):
    """
    轮询已推送但超时的审批单，查询最新状态
    """
    service = ApprovalPushService(db)

    # 查找推送超过timeout_minutes且状态仍为PENDING的记录
    cutoff_time = datetime.now() - timedelta(minutes=timeout_minutes)
    pending_records = db.query(ApprovalRecord).filter(
        ApprovalRecord.status == ApprovalStatus.PENDING,
        ApprovalRecord.push_time < cutoff_time
    ).all()

    for record in pending_records:
        adapter = service.get_adapter(record.platform)
        if not adapter:
            continue

        try:
            result = adapter.query_approval_status(record.platform_instance_id)

            if result.status != "PENDING":
                record.status = ApprovalStatus(result.status)
                record.callback_time = datetime.now()
                record.result_data = result.form_fields
                db.commit()
        except Exception as e:
            # 记录错误但继续处理其他记录
            print(f"Failed to poll approval {record.id}: {e}")
            continue
