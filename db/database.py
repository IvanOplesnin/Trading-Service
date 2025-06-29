from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

DATABASE_URL = settings.db_url


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as s:
        try:
            yield s
        finally:
            await s.close()
