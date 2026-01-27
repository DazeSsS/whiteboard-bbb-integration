from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_current_user_data, get_widget_service
from app.domain.services import WidgetService
from app.domain.entities import ConfigUpdate, UserData, WidgetCreate, WidgetResponse


router = APIRouter(
    tags=['Widget']
)


@router.post('/widgets')
async def create_widget(
    widget: WidgetCreate,
    widget_service: Annotated[WidgetService, Depends(get_widget_service)],
) -> WidgetResponse:
    response = await widget_service.create_widget(widget=widget)
    return response


@router.put('/widgets/config')
async def update_config(
    data: ConfigUpdate,
    user_data: Annotated[UserData, Depends(get_current_user_data)],
    widget_service: Annotated[WidgetService, Depends(get_widget_service)],
) -> list[int]:
    updated_widgets = await widget_service.update_config(
        user_data=user_data,
        data=data,
    )
    return updated_widgets
