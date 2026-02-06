import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_statistics_service
from app.domain.services import StatisticsService

logger = logging.getLogger(__name__)


router = APIRouter(tags=['Whiteboard'])


@router.post('/stats/module/create')
async def create_stats_module(
    name: str,
    statistics_service: Annotated[
        StatisticsService,
        Depends(get_statistics_service),
    ],
):
    logger.info('Инициализация модуля статистики %r', name)
    response = await statistics_service.create_stats_module(name=name)
    logger.info('Модуль статистики %r инициализирован', name)
    return response


@router.get('/stats/module/metrics')
async def get_current_metrics(
    statistics_service: Annotated[
        StatisticsService,
        Depends(get_statistics_service),
    ],
):
    logger.info('Получение метрик')
    response = await statistics_service.get_current_metrics()
    logger.info('Метрики получены')
    return response


@router.put('/stats/module/metrics')
async def update_metrics(
    metrics: dict,
    statistics_service: Annotated[
        StatisticsService,
        Depends(get_statistics_service),
    ],
):
    logger.info('Обновление метрик')
    response = await statistics_service.update_metrics(metrics=metrics)
    logger.info('Метрики обновлены')
    return response
