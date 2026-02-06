from fastapi import Query
from pydantic import Field

from .base import CamelSchema
from .query import QuerySchema


class MeetingCreate(QuerySchema):
    name: str = Field(...)
    meeting_ID: str = Field(..., alias='meetingID')
    whiteboard_id: int | None = Field(None)

    @classmethod
    def from_query(
        cls,
        name: str = Query(..., alias='name'),
        meeting_ID: str = Query(..., alias='meetingID'),
        whiteboard_id: int | None = Query(None, alias='whiteboardId'),
    ):
        return cls(
            name=name,
            meeting_ID=meeting_ID,
            whiteboard_id=whiteboard_id,
        )


class MeetingResponse(CamelSchema):
    name: str
    meeting_ID: str = Field(..., alias='meetingID')


class JoinParams(QuerySchema):
    meeting_ID: str = Field(..., alias='meetingID')

    @classmethod
    def from_query(
        cls,
        meeting_ID: str = Query(..., alias='meetingID'),
    ):
        return cls(
            meeting_ID=meeting_ID,
        )
