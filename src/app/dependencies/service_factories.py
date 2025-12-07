from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from app.domain.services import BBBService


def get_bbb_service(session: Annotated[AsyncSession, Depends(get_async_session)]) -> BBBService:
    return BBBService()
