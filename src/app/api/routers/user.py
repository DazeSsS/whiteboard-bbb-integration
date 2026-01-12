from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.dependencies import get_current_user_data, get_user_service
from app.domain.services import UserService
from app.domain.entities import UserCreate, UserData, UserResponse, UserUpdate


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('')
async def create_user(
    user: UserCreate,
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await user_service.create_user(user_data=user_data, user=user)
    return user


@router.get('/me')
async def get_user(
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    user = await user_service.get_user(user_id=user_data.id)
    return user


@router.patch('/me')
async def update_user(
    user: UserUpdate,
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    updated_user = await user_service.update_user_name(user_id=user_data.id, name=user.name)
    return updated_user


@router.get('/token')
async def get_user_token(
    user_id: Annotated[int, Query(..., alias='userId')],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> str:
    token = await user_service.get_user_token(user_id=user_id)
    return token
