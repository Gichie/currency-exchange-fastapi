from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.session import get_session
from src.repositories.currency import CurrencyRepository
from src.services.currency_service import CurrencyService


def get_currency_repository(session: AsyncSession = Depends(get_session)) -> CurrencyRepository:
    """Провайдер для CurrencyRepository. Создает экземпляр репозитория с активной сессией БД."""
    return CurrencyRepository(session=session)


def get_currency_service(
        repository: CurrencyRepository = Depends(get_currency_repository)
) -> CurrencyService:
    """Провайдер для CurrencyService. Создает экземпляр сервиса с готовым репозиторием."""
    return CurrencyService(repository=repository)
