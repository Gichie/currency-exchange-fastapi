from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from currency_exchange.core.config import settings

engine = create_async_engine(settings.ASYNC_DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with new_session() as session:
        yield session
