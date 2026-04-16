from fastapi import APIRouter

from .push import router as push_router
from .callback import router as callback_router
from .status import router as status_router

router = APIRouter()

router.include_router(push_router, prefix="/push", tags=["push"])
router.include_router(callback_router, prefix="/callback", tags=["callback"])
router.include_router(status_router, prefix="/status", tags=["status"])
