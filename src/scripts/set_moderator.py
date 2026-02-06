import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.data.repositories import UserRepository
from app.domain.enums import UserRole
from config import settings

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(DATABASE_URL)


async def set_moderator(
    user_id: int,
):
    async with AsyncSession(engine) as session:
        print('Смена роли...')

        try:
            async with session.begin():
                user_repo = UserRepository(session)
                user = await user_repo.get_by_id(id=user_id)
                user.role = UserRole.MODERATOR
        except Exception:
            print('Ошибка при смене роли...')

        print(
            f'Пользователю с идентификатором {user_id} '
            f'успешно назначена роль "moderator"'
        )


if __name__ == '__main__':
    answer = input(
        'Введите идентификатор пользователя, которого нужно сделать модератором: '
    )
    try:
        id = int(answer)
        asyncio.run(set_moderator(user_id=id))
    except Exception:
        print('Ошибка. Идентификатор должен быть числом')
