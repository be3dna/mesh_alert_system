from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings


database_url = URL.create(
    drivername="postgresql+asyncpg",
    username=settings.DB_USER,
    password=settings.DB_PASSWORD,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
)

engine = create_async_engine(
    database_url,
    echo=True,
    pool_pre_ping=True
)