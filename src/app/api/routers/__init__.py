from fastapi import APIRouter
from .bbb import router as bbb_router


api_router = APIRouter(
    prefix='/api/v1'
)

api_router.include_router(bbb_router)
