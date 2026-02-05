import asyncio
import logging
from pprint import pprint

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from config import settings, Environment
from app.logging import setup_logging
from app.dependencies import get_statistics_service


DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)


async def get_stats(internal_id: str):
    setup_logging(
        level=logging.WARNING if settings.ENVIRONMENT == Environment.PROD else logging.DEBUG
    )
    async with AsyncSession(engine) as session:
        stats_service = get_statistics_service(session)
        meeting_stats = await stats_service.process_stats(internal_meeting_id=internal_id)
        pprint(meeting_stats)


if __name__ == '__main__':
    internal_id = input('Введите внутренний идентификатор встречи: ')
    asyncio.run(get_stats(internal_id=internal_id))
