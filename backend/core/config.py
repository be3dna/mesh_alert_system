from datetime import UTC, datetime

from pydantic import PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str | None = None
    DATABASE_URL: str | None = None
    AUTH_SESSION_SECONDS: PositiveInt = 8 * 60 * 60
    AUTH_COOKIE_SECURE: bool = True
    AUTH_ORIGIN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

DEFAULT_DATETIME_FUNK=lambda: datetime.now(UTC)  # TODO: is UTC best choise? maybe msk?