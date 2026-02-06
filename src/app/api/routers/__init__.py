from fastapi import APIRouter

from .bbb import router as bbb_router
from .meeting import router as meeting_router
from .user import router as user_router
from .whiteboard import router as whiteboard_router
from .widget import router as widget_router

api_router = APIRouter(prefix='/api/v1')

api_router.include_router(bbb_router)
api_router.include_router(meeting_router)
api_router.include_router(user_router)
api_router.include_router(whiteboard_router)
api_router.include_router(widget_router)

__all__ = ('api_router',)
