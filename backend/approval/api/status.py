from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def status_approval():
    return {"message": "status endpoint"}