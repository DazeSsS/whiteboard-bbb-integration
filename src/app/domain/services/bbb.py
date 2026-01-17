import httpx
from xml.etree import ElementTree

from config import settings
from app.domain.enums import ReturnCode

from .meeting import MeetingService


class BBBService:
    async def set_hook(self, callback_url: str, event_id: str | None) -> str:
        query_string = f'callbackURL={callback_url}'

        if event_id is not None:
            query_string += f'&eventID={event_id}'

        checksum = MeetingService.generate_checksum(
            call_name='hooks/create',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/hooks/create?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)

        if root.get('returncode') == ReturnCode.FAILED:
            return None

        hook_id = root.find('.//hookID').text
        return hook_id
    
    async def list_hooks(self, meeting_ID: str | None):
        query_string = '' if (meeting_ID is None) else f'meetingID={meeting_ID}'

        checksum = MeetingService.generate_checksum(
            call_name='hooks/list',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/hooks/list?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)

        if root.get('returncode') == ReturnCode.FAILED:
            return None

        return response.text
    
    async def destroy_hook(self, hook_id: str):
        query_string = f'hookID={hook_id}'
        checksum = MeetingService.generate_checksum(
            call_name='hooks/destroy',
            query=query_string
        )

        request = f'{settings.BBB_API_URL}/hooks/destroy?{query_string}&checksum={checksum}'

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(request)

        root = ElementTree.fromstring(response.text)

        if root.get('returncode') == ReturnCode.FAILED:
            return None

        return response.text
