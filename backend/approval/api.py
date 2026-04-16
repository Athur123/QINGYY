from fastapi import APIRouter

router = APIRouter()


@router.post("/push")
def push_approval():
    return {"message": "push endpoint"}


@router.post("/callback")
def callback_approval():
    return {"message": "callback endpoint"}


@router.get("/status")
def status_approval():
    return {"message": "status endpoint"}
