from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_bbb_service
from app.domain.services import BBBService


router = APIRouter(
    prefix='/bbb',
    tags=['BBB']
)


@router.get('/hooks/create')
async def set_hook(
    callback_url: Annotated[str, Query(..., alias='callbackURL')],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
    event_id: Annotated[str | None, Query(..., alias='eventID')] = None,
) -> str:
    response = await bbb_service.set_hook(callback_url=callback_url, event_id=event_id)
    return response


@router.get('/hooks/list')
async def get_hook_list(
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
    meeting_ID: Annotated[str | None, Query(..., alias='meetingID')] = None,
) -> str:
    response = await bbb_service.list_hooks(meeting_ID=meeting_ID)
    return response


@router.get('/hooks/destroy')
async def destroy_hook(
    hook_id: Annotated[str, Query(..., alias='hookID')],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
) -> str:
    response = await bbb_service.destroy_hook(hook_id=hook_id)
    return response