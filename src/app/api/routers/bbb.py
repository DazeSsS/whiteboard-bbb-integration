import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_bbb_service
from app.domain.services import BBBService

logger = logging.getLogger(__name__)


router = APIRouter(prefix='/bbb', tags=['BBB'])


@router.get('/hooks/create')
async def set_hook(
    callback_url: Annotated[str, Query(..., alias='callbackURL')],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
    event_id: Annotated[str | None, Query(..., alias='eventID')] = None,
) -> str:
    logger.info('Создание хука для URL: %s', callback_url)
    response = await bbb_service.set_hook(callback_url=callback_url, event_id=event_id)
    logger.info('Хук создан для URL: %s', callback_url)
    return response


@router.get('/hooks/list')
async def get_hook_list(
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
    meeting_ID: Annotated[str | None, Query(..., alias='meetingID')] = None,
) -> str:
    logger.info('Получение активных хуков')
    response = await bbb_service.list_hooks(meeting_ID=meeting_ID)
    logger.info('Активные хуки получены')
    return response


@router.get('/hooks/destroy')
async def destroy_hook(
    hook_id: Annotated[str, Query(..., alias='hookID')],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
) -> str:
    logger.info('Удаление хука c ID %s', hook_id)
    response = await bbb_service.destroy_hook(hook_id=hook_id)
    logger.info('Хук c ID %s удалён', hook_id)
    return response
