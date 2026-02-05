import logging
import httpx

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from app.data.models import Widget
from app.data.repositories import WidgetRepository
from app.domain.entities import ConfigUpdate, UserData, WidgetCreate, WidgetResponse


logger = logging.getLogger(__name__)


class WidgetService:
    def __init__(
        self,
        session: AsyncSession,
        widget_repo: WidgetRepository,
    ):
        self.session = session
        self.widget_repo = widget_repo

    async def create_widget(self, widget: WidgetCreate) -> WidgetResponse:
        widget_obj = await self.widget_repo.get_by_id(id=widget.id)
        if widget_obj:
            return WidgetResponse.model_validate(widget)
        
        widget_dict = widget.model_dump()
        widget_obj = Widget(**widget_dict)

        async with self.session.begin():
            await self.widget_repo.add(widget_obj)
            new_widget = WidgetResponse.model_validate(widget_obj)

        return new_widget

    async def update_config(self, user_data: UserData, data: ConfigUpdate) -> list[int]:
        widget_ids = await self.widget_repo.get_ids_by_whiteboard_id(
            whiteboard_id=data.whiteboard_id
        )

        updated_widgets = []
        async with httpx.AsyncClient(timeout=20.0) as client:
            for widget_id in widget_ids:
                try:
                    response = await client.put(
                        url=settings.WHITEBOARD_BASE_URL + f'/api/widget/{widget_id}',
                        json={
                            'config': data.config,
                        },
                        headers={
                            'Authorization': user_data.token,
                        },
                    )
                    response.raise_for_status()
                    updated_widgets.append(widget_id)
                except Exception:
                    logger.exception(
                        'Error while updating widget with ID %r',
                        widget_id
                    )

        return updated_widgets
