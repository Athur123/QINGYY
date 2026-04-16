from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def callback_approval():
    return {"message": "callback endpoint"}
