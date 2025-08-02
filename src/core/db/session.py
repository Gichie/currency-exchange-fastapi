from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator:
    """
    Зависимость FastAPI для управления жизненным циклом сессии SQLAlchemy.

    Гарантирует, что сессия создается перед обработкой запроса и корректно закрывается
    после его завершения, предотвращая утечки соединений.
    """
    async with new_session() as session:
        yield session
