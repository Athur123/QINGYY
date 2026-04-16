from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from backend.approval.models import PlatformAuth

router = APIRouter()

def get_db():
    # TODO: 从数据库连接池获取session
    pass

class AuthConfig(BaseModel):
    platform: str
    corpid: str
    secret: str
    agentid: str

class AuthSaveRequest(BaseModel):
    platform: str
    corpid: str
    secret: str
    agentid: str

class AuthResponse(BaseModel):
    code: int
    message: str
    data: Optional[AuthConfig]

@router.get("/auth/{platform}", response_model=AuthResponse)
def get_auth_config(
    platform: str,
    db: Session = Depends(get_db)
):
    """获取鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == platform
    ).first()

    if not auth:
        return AuthResponse(code=0, message="success", data=None)

    return AuthResponse(
        code=0,
        message="success",
        data=AuthConfig(
            platform=auth.platform,
            corpid=auth.corpid,
            secret="******",  # 脱敏
            agentid=auth.agentid
        )
    )

@router.put("/auth", response_model=AuthResponse)
def save_auth_config(
    request: AuthSaveRequest,
    db: Session = Depends(get_db)
):
    """保存鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == request.platform
    ).first()

    if auth:
        auth.corpid = request.corpid
        auth.secret = request.secret
        auth.agentid = request.agentid
    else:
        auth = PlatformAuth(
            platform=request.platform,
            corpid=request.corpid,
            secret=request.secret,
            agentid=request.agentid
        )
        db.add(auth)

    db.commit()

    return AuthResponse(
        code=0,
        message="success",
        data=AuthConfig(
            platform=request.platform,
            corpid=request.corpid,
            secret="******",
            agentid=request.agentid
        )
    )

@router.post("/auth/{platform}/verify")
def verify_auth_config(
    platform: str,
    db: Session = Depends(get_db)
):
    """验证鉴权配置"""
    auth = db.query(PlatformAuth).filter(
        PlatformAuth.platform == platform
    ).first()

    if not auth:
        return {"code": 1, "message": "配置不存在"}

    # TODO: 调用企业微信API验证
    return {"code": 0, "message": "验证成功"}