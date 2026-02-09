import asyncio
import logging

from httpx import ConnectTimeout

from app.domain.services import BBBService
from app.logging import setup_logging
from config import Environment, settings

logger = logging.getLogger(__name__)


async def set_hooks():
    bbb_service = BBBService()
    try:
        hook_id = await bbb_service.set_hook(
            callback_url=settings.EVENTS_CALLBACK_URL,
            event_id='meeting-ended',
        )

        if hook_id is not None:
            logger.info(f'meeting-ended hook registered with ID: {hook_id}')
    except ConnectTimeout:
        logger.error('ERROR: connection timeout when registering hook')


if __name__ == '__main__':
    setup_logging(
        level=logging.WARNING
        if settings.ENVIRONMENT == Environment.PROD
        else logging.DEBUG
    )

    asyncio.run(set_hooks())
