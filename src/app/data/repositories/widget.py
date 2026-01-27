from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.base import SQLAlchemyRepository
from app.data.models import Widget


class WidgetRepository(SQLAlchemyRepository[Widget]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Widget)
    
    async def get_ids_by_whiteboard_id(self, whiteboard_id: int) -> list[int]:
        query = (
            select(Widget.id)
            .where(Widget.whiteboard_id == whiteboard_id)
        )
        result = await self.session.scalars(query)
        return result.all()
