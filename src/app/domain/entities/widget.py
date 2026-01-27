from .base import CamelSchema


class WidgetCreate(CamelSchema):
    id: int
    whiteboard_id: int


class WidgetResponse(WidgetCreate):
    pass


class ConfigUpdate(CamelSchema):
    config: dict
    whiteboard_id: int
