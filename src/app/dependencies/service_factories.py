from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.data.repositories import MeetingRepository, UserRepository
from app.domain.services import MeetingService, UserService


def get_meeting_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> MeetingService:
    meeting_repo = MeetingRepository(session)
    user_repo = UserRepository(session)
    return MeetingService(session=session, meeting_repo=meeting_repo, user_repo=user_repo)

def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
    user_repo = UserRepository(session)
    return UserService(session=session, user_repo=user_repo)
