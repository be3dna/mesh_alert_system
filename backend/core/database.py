from sqlalchemy import make_url
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings


if settings.DATABASE_URL is None:
    database_url = URL.create(
        drivername="postgresql+asyncpg",
        username=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=settings.DB_NAME,
    )
else:
    database_url = make_url(settings.DATABASE_URL)

engine = create_async_engine(
    database_url,
    echo=True,
    pool_pre_ping=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)


async def get_session():
    async with SessionLocal() as session:
        yield session