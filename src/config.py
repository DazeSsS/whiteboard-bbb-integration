from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEV = 'dev'
    PROD = 'prod'


class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: Environment = Environment.DEV

    # PostgreSQL
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str

    # CORS
    ORIGINS: str

    # App
    APP_RECORDINGS_PATH: str
    EVENTS_CALLBACK_URL: str

    # Big Blue Button
    BBB_SECRET: str
    BBB_API_URL: str
    BBB_RECORDINGS_PATH: str

    # Whitebooard
    WHITEBOARD_BASE_URL: str
    WHITEBOARD_URL_PATH: str

    def get_db_url(self) -> str:
        return (
            f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
            f'{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
