from fastapi import APIRouter

router = APIRouter()


@router.post("/")
def push_approval():
    return {"message": "push endpoint"}