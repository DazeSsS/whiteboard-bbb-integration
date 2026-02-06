from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.repositories import (
    MeetingRepository,
    StatsModuleRepository,
    UserRepository,
    WidgetRepository,
)
from app.domain.services import (
    BBBService,
    MeetingService,
    StatisticsService,
    UserService,
    WidgetService,
)
from database import get_async_session


def get_bbb_service() -> BBBService:
    return BBBService()


def get_meeting_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> MeetingService:
    meeting_repo = MeetingRepository(session)
    user_repo = UserRepository(session)
    return MeetingService(
        session=session,
        meeting_repo=meeting_repo,
        user_repo=user_repo,
    )


def get_statistics_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> StatisticsService:
    meeting_repo = MeetingRepository(session)
    stats_module_repo = StatsModuleRepository(session)
    return StatisticsService(
        session=session,
        meeting_repo=meeting_repo,
        stats_module_repo=stats_module_repo,
    )


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserService:
    user_repo = UserRepository(session)
    return UserService(session=session, user_repo=user_repo)


def get_widget_service(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> WidgetService:
    widget_repo = WidgetRepository(session)
    return WidgetService(session=session, widget_repo=widget_repo)
