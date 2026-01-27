from pydantic import Field

from app.domain.enums import UserRole

from .base import BaseSchema, CamelSchema


class UserCreate(CamelSchema):
    name: str = Field(min_length=1)


class UserUpdate(UserCreate):
    name: str = Field(min_length=1)


class UserResponse(UserCreate):
    id: int
    role: UserRole


class UserData(BaseSchema):
    id: int
    token: str
