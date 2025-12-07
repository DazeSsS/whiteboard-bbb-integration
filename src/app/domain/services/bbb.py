import httpx
import hashlib
from xml.etree import ElementTree 
from urllib.parse import parse_qs

from fastapi import Request

from config import settings
from app.domain.entities import BaseSchema, JoinParams, MeetingCreate
from app.domain.enums import ReturnCode, UserRole
from app.domain.exceptions import CodeFailed


class BBBService:
    @staticmethod
    def generate_checksum(call_name: str, query: str) -> str:
        string = (
            call_name +
            query +
            settings.BBB_SECRET
        )
        result = hashlib.sha1(string.encode()).hexdigest()
        return result

    async def create_meeting(self, meeting: MeetingCreate) -> httpx.Response:
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
        
        meeting_ID = root.find('meetingID').text
        join_params = JoinParams(
            full_name='Test',
            meeting_ID=meeting_ID,
            role=UserRole.MODERATOR.value
        )

        response = await self.get_join_link(join_params=join_params)

        return response

    async def get_join_link(self, join_params: JoinParams):
        if not join_params.role:
            join_params.role = UserRole.VIEWER.value
        join_params.redirect = 'false'
        # join_params.logoutURL = ''

        query_string = join_params.to_query_string()

        checksum = self.generate_checksum(
            call_name='join',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/join?{query_string}&checksum={checksum}'
        print(request)

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)
        returncode = root.find('returncode').text

        if returncode == ReturnCode.FAILED:
            message_key = root.find('messageKey').text
            message = root.find('message').text
            
            detail = f'{message_key}: {message}'

            raise CodeFailed(detail=detail)

        url = root.find('url').text + f'&whiteboardId='

        return url
