from pydantic import Field
from .base import BaseSchema, CamelSchema
from app.domain.enums import UserRole


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
