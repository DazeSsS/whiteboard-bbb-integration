from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from config import settings

from app.dependencies import get_meeting_service
from app.domain.services import MeetingService
from app.domain.entities import JoinParams, MeetingCreate


router = APIRouter(
    prefix='/meeting',
    tags=['Meetings']
)


@router.post('/create')
async def create_meeting(
    meeting: Annotated[MeetingCreate, Depends(MeetingCreate.from_query)],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.create_meeting(meeting=meeting)
    return response


@router.get('/join')
async def get_join_link(
    join_params: Annotated[JoinParams, Depends(JoinParams.from_query)],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.get_join_link(join_params=join_params)
    return response


@router.get('/{meeting_ID}/info')
async def get_meeting_info(
    meeting_ID: str,
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
):
    response = await meeting_service.get_meeting_info(meetind_ID=meeting_ID)
    return response
