from fastapi import APIRouter
from .meeting import router as meeting_router


api_router = APIRouter(
    prefix='/api/v1'
)

api_router.include_router(meeting_router)
