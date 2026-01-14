import json
from urllib.parse import parse_qs
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Request

from config import settings
from app.dependencies import get_current_user_data, get_meeting_service, get_statistics_service
from app.domain.services import MeetingService, StatisticsService
from app.domain.entities import JoinParams, MeetingCreate, MeetingResponse, UserData


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


@router.get('/end')
async def end_meeting(
    meeting_ID: Annotated[str, Query(..., alias='meetingID')],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
):
    await meeting_service.end_meeting(meeting_ID=meeting_ID)
    return {'status': 'success'}


@router.get('/active')
async def get_active_meeting(
    whiteboard_id: Annotated[int, Query(..., alias='whiteboardId')],
    meeting_service: Annotated[MeetingService, Depends(get_meeting_service)],
) -> MeetingResponse | None:
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


@router.post('/events')
async def get_events(
    request: Request,
    statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)],
):
    raw_body = await request.body()
    decoded_body = raw_body.decode()

    raw_event = parse_qs(decoded_body)['event'][0]
    event = json.loads(raw_event)[0]
    
    event_type = event['data']['id']
    internal_meeting_id = event['data']['attributes']['meeting']['internal-meeting-id']

    if event_type != 'rap-archive-ended':
        return
    
    await statistics_service.process_stats(internal_meeting_id=internal_meeting_id)
