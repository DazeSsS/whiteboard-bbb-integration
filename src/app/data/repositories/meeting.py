from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories.base import SQLAlchemyRepository
from app.data.models import Meeting


class MeetingRepository(SQLAlchemyRepository[Meeting]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Meeting)

    async def get_last_by_meeting_ID(self, meeting_ID: str) -> Meeting:
        query = (
            select(Meeting)
            .where(Meeting.text_id == meeting_ID)
            .order_by(Meeting.created_at.desc())
        )
        result = await self.session.scalar(query)
        return result

    async def get_whiteboard_id_by_meeting_internal_id(self, internal_id: str) -> int:
        query = (
            select(Meeting.whiteboard_id)
            .where(Meeting.id == internal_id)
        )
        result = await self.session.scalar(query)
        return result
    
    async def update_meeting_stats(self, internal_id: str, stats: dict):
        query = (
            update(Meeting)
            .where(Meeting.id == internal_id)
            .values(analytics=stats)
            .returning(Meeting)
        )
        result = await self.session.execute(query)
        updated_meeting = result.scalar_one_or_none()
        
        if updated_meeting:
            return await self.session.merge(updated_meeting)
        
        return None
