from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.base import SQLAlchemyRepository
from app.data.models import User
from app.domain.entities import query


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def update_name(self, user_id: int, name: str):
        query = (
            update(User)
            .where(User.id == user_id)
            .values(name=name)
            .returning(User)
        )

        result = await self.session.execute(query)
        updated_user = result.scalar_one_or_none()

        if updated_user:
            return await self.session.merge(updated_user)
            
        return None
