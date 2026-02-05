import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from app.dependencies import get_current_user_data, get_user_service
from app.domain.services import UserService
from app.domain.entities import UserCreate, UserData, UserResponse, UserUpdate


logger = logging.getLogger(__name__)


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
    logger.info('Создание профиля для пользователя с ID %s', user_data.id)
    user = await user_service.create_user(user_data=user_data, user=user)
    logger.info('Профиль для пользователя с ID %s создан', user_data.id)
    return user


@router.get('/me')
async def get_user(
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    logger.info('Получение пользователя с ID %s', user_data.id)
    user = await user_service.get_user(user_id=user_data.id)
    logger.info('Пользователь с ID %s получен', user_data.id)
    return user


@router.patch('/me')
async def update_user(
    user: UserUpdate,
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    logger.info('Обновление пользователя с ID %s', user_data.id)
    updated_user = await user_service.update_user_name(user_id=user_data.id, name=user.name)
    logger.info('Пользователь с ID %s обновлён', user_data.id)
    return updated_user


@router.get('/token')
async def get_user_token(
    user_id: Annotated[int, Query(..., alias='userId')],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> str:
    logger.info('Получение токена пользователя с ID %s', user_id)
    token = await user_service.get_user_token(user_id=user_id)
    logger.info('Токен пользователя с ID %s получен', user_id)
    return token
