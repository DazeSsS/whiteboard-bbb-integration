from datetime import datetime

from pydantic import Field
from fastapi import Query

from .base import CamelSchema
from app.domain.enums import UserRole


class UserCreate(CamelSchema):
    internal_id: int
    group: str | None = None
    position: str | None = None
    role: str = 'admin'


class UserResponse(UserCreate):
    id: int
    name: str
