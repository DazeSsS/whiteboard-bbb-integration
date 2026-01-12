from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user_data, get_meeting_service
from app.domain.services.meeting import MeetingService
from app.domain.entities import JoinParams, MeetingCreate, UserData


router = APIRouter(
    prefix='/meetings',
    tags=['Meetings']
)


@router.get('/create')
async def create_meeting(
    meeting: Annotated[MeetingCreate, Depends(MeetingCreate.from_query)],
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.create_meeting(
        meeting=meeting,
        user_data=user_data
    )
    return response


@router.get('/join')
async def get_join_link(
    join_params: Annotated[JoinParams, Depends(JoinParams.from_query)],
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.get_join_link(
        join_params=join_params,
        user_data=user_data
    )
    return response


@router.get('/active')
async def get_active_meeting(
    whiteboard_id: Annotated[int, Query(..., alias='whiteboardId')],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
):
    response = await meeting_service.get_active_meeting(whiteboard_id=whiteboard_id)
    return response


@router.get('/whiteboard')
async def get_whiteboard_id(
    internal_meeting_id: Annotated[str, Query(..., alias='internalMeetingId')],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> int | None:
    whiteboard_id = await meeting_service.get_whiteboard_id(internal_meeting_id=internal_meeting_id)
    return whiteboard_id


@router.get('/recordings')
async def get_recordings(
    meeting_ID: Annotated[str, Query(..., alias='meetingID')],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.get_recordings(meeting_ID=meeting_ID)
    return response


@router.get('/{meeting_ID}/info')
async def get_meeting_info(
    meeting_ID: str,
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> str:
    response = await meeting_service.get_meeting_info(meeting_ID=meeting_ID)
    return response
