import asyncio

from httpx import ConnectTimeout

from app.domain.services import BBBService
from config import settings


async def set_hooks():
    bbb_service = BBBService()
    try:
        hook_id = await bbb_service.set_hook(
            callback_url=settings.EVENTS_CALLBACK_URL,
            event_id='meeting-ended',
        )

        if hook_id is not None:
            print(f'meeting-ended hook registered with ID: {hook_id}')
    except ConnectTimeout:
        print('ERROR: connection timeout when registering hook')


if __name__ == '__main__':
    asyncio.run(set_hooks())
