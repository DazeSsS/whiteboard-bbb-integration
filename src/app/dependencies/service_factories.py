from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.models import stats_module
from database import get_async_session

from app.data.repositories import MeetingRepository, StatsModuleRepository, UserRepository
from app.domain.services import MeetingService, StatisticsService, UserService


def get_meeting_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> MeetingService:
    meeting_repo = MeetingRepository(session)
    user_repo = UserRepository(session)
    return MeetingService(session=session, meeting_repo=meeting_repo, user_repo=user_repo)

def get_statistics_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> StatisticsService:
    meeting_repo = MeetingRepository(session)
    stats_module_repo = StatsModuleRepository(session)
    return StatisticsService(session=session, meeting_repo=meeting_repo, stats_module_repo=stats_module_repo)

def get_user_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> UserService:
    user_repo = UserRepository(session)
    return UserService(session=session, user_repo=user_repo)
