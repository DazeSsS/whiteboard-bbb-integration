import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings, Environment
from app.logging import setup_logging
from app.middleware import BearerTokenMiddleware
from app.api.exceptions import set_exceptions
from app.api.routers import api_router


setup_logging(
    level=logging.WARNING if settings.ENVIRONMENT == Environment.PROD else logging.DEBUG
)

app = FastAPI(
    title='Big Blue Button'
)

set_exceptions(app)

app.include_router(api_router)

origins = settings.ORIGINS.split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'], 
)

app.add_middleware(BearerTokenMiddleware)
