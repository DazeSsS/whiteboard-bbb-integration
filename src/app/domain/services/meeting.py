import httpx
import hashlib
from urllib.parse import parse_qs
from xml.etree import ElementTree

from config import settings
from app.domain.entities import BaseSchema, JoinParams, MeetingCreate
from app.domain.enums import ReturnCode, UserRole
from app.domain.exceptions import CodeFailed


class MeetingService:
    @staticmethod
    def generate_checksum(call_name: str, query: str) -> str:
        string = (
            call_name +
            query +
            settings.BBB_SECRET
        )
        result = hashlib.sha1(string.encode()).hexdigest()
        return result

    async def create_meeting(self, meeting: MeetingCreate):
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
        
        join_params = JoinParams(
            full_name='Test',
            meeting_ID=meeting.meeting_ID,
            role=UserRole.MODERATOR.value
        )

        request = await self.get_join_link(join_params=join_params)

        return request

    async def get_join_link(self, join_params: JoinParams):
        if not hasattr(join_params, 'role'):
            join_params.role = UserRole.VIEWER.value

        join_params.redirect = 'false'
        join_params.logoutURL = settings.WHITEBOARD_BASE_URL

        query_string = join_params.to_query_string()

        checksum = self.generate_checksum(
            call_name='join',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/join?{query_string}&checksum={checksum}'

        return request

    async def get_meeting_info(self, meetind_ID):
        query_string = f'meetingID={meetind_ID}'
        checksum = self.generate_checksum(
            call_name='getMeetingInfo',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/getMeetingInfo?{query_string}&checksum={checksum}'

        return request
