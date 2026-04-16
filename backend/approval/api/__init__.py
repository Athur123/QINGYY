from approval.api.push import router as push_router
from approval.api.callback import router as callback_router
from approval.api.status import router as status_router
from approval.api.templates import router as templates_router
from approval.api.auth import router as auth_router

__all__ = ["push_router", "callback_router", "status_router", "templates_router", "auth_router"]
