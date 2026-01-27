from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_statistics_service
from app.domain.services import StatisticsService


router = APIRouter(
    tags=['Whiteboard']
)


@router.post('/stats/module/create')
async def create_stats_module(
    name: str,
    statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)],
):
    response = await statistics_service.create_stats_module(name=name)
    return response


@router.get('/stats/module/metrics')
async def get_current_metrics(
    statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)],
):
    response = await statistics_service.get_current_metrics()
    return response


@router.put('/stats/module/metrics')
async def update_metrics(
    metrics: dict,
    statistics_service: Annotated[StatisticsService, Depends(get_statistics_service)],
):
    response = await statistics_service.update_metrics(metrics=metrics)
    return response
