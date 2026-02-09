import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.data.repositories import UserRepository
from app.domain.enums import UserRole
from app.logging import setup_logging
from config import Environment, settings

logger = logging.getLogger(__name__)

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)


async def set_moderator(
    user_id: int,
):
    async with AsyncSession(engine) as session:
        logger.info('Смена роли...')

        try:
            async with session.begin():
                user_repo = UserRepository(session)
                user = await user_repo.get_by_id(id=user_id)
                user.role = UserRole.MODERATOR
        except Exception:
            logger.error('Ошибка при смене роли...')

        logger.info(
            'Пользователю с идентификатором %s '
            'успешно назначена роль "moderator"',
            user_id
        )


if __name__ == '__main__':
    setup_logging(
        level=logging.WARNING
        if settings.ENVIRONMENT == Environment.PROD
        else logging.DEBUG
    )

    answer = input(
        'Введите идентификатор пользователя, которого нужно сделать модератором: '
    )
    try:
        id = int(answer)
        asyncio.run(set_moderator(user_id=id))
    except Exception:
        print('Ошибка. Идентификатор должен быть числом')
