from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import StatsModule
from app.data.repositories.base import SQLAlchemyRepository


class StatsModuleRepository(SQLAlchemyRepository[StatsModule]):
    def __init__(
        self,
        session: AsyncSession,
    ):
        super().__init__(session, StatsModule)

    async def get_first_module(
        self,
    ) -> StatsModule:
        query = select(StatsModule).limit(1)
        result = await self.session.scalar(query)
        return result
