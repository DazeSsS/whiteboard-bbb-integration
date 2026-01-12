import httpx
import hashlib
from xml.etree import ElementTree

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from app.data.models import Meeting
from app.data.repositories import MeetingRepository, UserRepository
from app.domain.entities import JoinParams, MeetingCreate, MeetingResponse, UserData
from app.domain.enums import ReturnCode, UserRole
from app.domain.exceptions import AlreadyExistsException, CodeFailed, NotFoundException


class MeetingService:
    def __init__(
        self,
        session: AsyncSession,
        meeting_repo: MeetingRepository,
        user_repo: UserRepository
    ):
        self.session = session
        self.meeting_repo = meeting_repo
        self.user_repo = user_repo

    @staticmethod
    def generate_checksum(call_name: str, query: str) -> str:
        string = (
            call_name +
            query +
            settings.BBB_SECRET
        )
        result = hashlib.sha1(string.encode()).hexdigest()
        return result

    async def create_meeting(self, meeting: MeetingCreate, user_data: UserData):
        meeting.record = 'true'
        meeting.meta_whiteboard = meeting.whiteboard_id
        query_string = meeting.to_query_string()

        checksum = self.generate_checksum(
            call_name='create',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/create?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)
        returncode = root.find('returncode').text
        
        if returncode == ReturnCode.FAILED:
            message_key = root.find('messageKey').text
            message = root.find('message').text
            
            detail = f'{message_key}: {message}'

            raise CodeFailed(detail=detail)

        internal_id = root.find('internalMeetingID').text
        try:
            async with self.session.begin():
                new_meeting_obj = Meeting(
                    id=internal_id,
                    text_id=meeting.meeting_ID,
                    name=meeting.name,
                    whiteboard_id=meeting.whiteboard_id
                )
                await self.meeting_repo.add(new_meeting_obj)
        except IntegrityError as exc:
            pass

        join_params = JoinParams(meeting_ID=meeting.meeting_ID)
        request = await self.get_join_link(join_params=join_params, user_data=user_data)
        return request

    async def get_join_link(self, join_params: JoinParams, user_data: UserData):
        async with self.session.begin():
            user = await self.user_repo.get_by_id(id=user_data.id)
            if user is None:
                raise NotFoundException(entity_name='User')
            
            meeting = await self.meeting_repo.get_last_by_meeting_ID(meeting_ID=join_params.meeting_ID)
            if user is None:
                raise NotFoundException(entity_name='Meeting')
        
            user.token = user_data.token
        
            join_params.userID = user.id
            join_params.fullName = user.name
            join_params.role = user.role
            join_params.redirect = 'true'
            join_params.logoutURL = f'{settings.WHITEBOARD_BASE_URL}{settings.WHITEBOARD_URL_PATH}/{meeting.whiteboard_id}'

        query_string = join_params.to_query_string()

        checksum = self.generate_checksum(
            call_name='join',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/join?{query_string}&checksum={checksum}'

        return request
    
    async def end_meeting(self, meeting_ID: str):
        query_string = f'meetingID={meeting_ID}'
        checksum = self.generate_checksum(
            call_name='end',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/end?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            await client.get(request)

    async def get_meeting_info(self, meeting_ID: str):
        query_string = f'meetingID={meeting_ID}'
        checksum = self.generate_checksum(
            call_name='getMeetingInfo',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/getMeetingInfo?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        return response.text
    
    async def get_active_meeting(self, whiteboard_id: int):
        query_string = f''
        checksum = self.generate_checksum(
            call_name='getMeetings',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/getMeetings?checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)
        print(response.text)
        returncode = root.find('returncode').text
        
        if returncode == ReturnCode.FAILED:
            message_key = root.find('messageKey').text
            message = root.find('message').text
            
            detail = f'{message_key}: {message}'

            raise CodeFailed(detail=detail)

        meetings_elem = root.find('meetings')
        if meetings_elem is None:
            return []

        active_meeting = None
        for meeting_elem in meetings_elem.findall('meeting'):
            meeting_ID = meeting_elem.find('meetingID').text
            is_active = meeting_elem.find('endTime').text == '0'

            metadata = meeting_elem.find('metadata')
            whiteboard_elem = metadata.find('whiteboard')
            if whiteboard_elem is not None:
                whiteboard = int(whiteboard_elem.text)

            if is_active and (whiteboard == whiteboard_id):
                active_meeting = MeetingResponse(meeting_ID=meeting_ID)
                break

        return active_meeting

    async def get_recordings(self, meeting_ID: str | None):
        query_string = f'meetingID={meeting_ID}'
        checksum = self.generate_checksum(
            call_name='getRecordings',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/getRecordings?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        return response.text

    async def get_whiteboard_id(self, internal_meeting_id: str) -> int | None:
        whiteboard_id = await self.meeting_repo.get_whiteboard_id_by_meeting_internal_id(
            internal_id=internal_meeting_id
        )
        return whiteboard_id
