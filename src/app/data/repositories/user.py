from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.base import SQLAlchemyRepository
from app.data.models import User


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)

    async def get_by_internal_ID(self, internal_ID: int) -> User | None:
        query = (
            select(User)
            .where(User.internal_id == internal_ID)
        )
        result = await self.session.scalar(query)
        return result
