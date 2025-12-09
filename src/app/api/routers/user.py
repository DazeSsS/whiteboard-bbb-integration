from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from config import settings

from app.dependencies import get_user_service
from app.domain.services import UserService
from app.domain.entities import UserCreate, UserResponse


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/{internal_ID}')
async def get_user(
    internal_ID: int,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await user_service.get_user(internal_ID=internal_ID)
    return user


@router.post('/{internal_ID}')
async def create_user(
    user: UserCreate,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await user_service.create_user(user=user)
    return user
