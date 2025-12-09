from pydantic import Field
from fastapi import Query

from .query import QuerySchema
from app.domain.enums import UserRole


class MeetingCreate(QuerySchema):
    name: str = Field(...)
    meeting_ID: str | None = Field(None, alias='meetingID')

    @classmethod
    def from_query(
        cls,
        name: str = Query(..., alias='name'),
        meeting_ID: str | None = Query(None, alias='meetingID'),
    ):
        return cls(
            name=name,
            meeting_ID=meeting_ID
        )


class JoinParams(QuerySchema):
    full_name: str = Field(...)
    meeting_ID: str = Field(..., alias='meetingID')
    # role: UserRole | None = None

    @classmethod
    def from_query(
        cls,
        full_name: str = Query(..., alias='fullName'),
        meeting_ID: str = Query(..., alias='meetingID'),
    ):
        return cls(
            full_name=full_name,
            meeting_ID=meeting_ID
        )
