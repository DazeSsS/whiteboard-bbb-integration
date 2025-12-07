from typing import Annotated

from fastapi import APIRouter, Depends, Request

from config import settings

from app.dependencies import get_bbb_service
from app.domain.services import BBBService
from app.domain.entities import JoinParams, MeetingCreate


router = APIRouter(
    prefix='/meeting',
    tags=['Big Blue Button']
)

@router.get('/create')
async def create_meeting(
    meeting: Annotated[MeetingCreate, Depends(MeetingCreate.from_query)],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
) -> str | None:
    response = await bbb_service.create_meeting(meeting=meeting)
    return response


@router.get('/join')
async def get_join_link(
    join_params: Annotated[JoinParams, Depends(JoinParams.from_query)],
    bbb_service: Annotated[BBBService, Depends(get_bbb_service)],
) -> str | None:
    response = await bbb_service.get_join_link(join_params=join_params)
    return response
