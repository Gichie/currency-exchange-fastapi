from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db.session import get_session
from src.repositories.currency import CurrencyRepository
from src.repositories.exchange_rate_repository import ExchangeRateRepository
from src.services.currency_service import CurrencyService
from src.services.exchange_rate_service import ExchangeRateService


def get_currency_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> CurrencyRepository:
    """
    Провайдер для CurrencyRepository.

    Создает экземпляр репозитория для операций с валютами с активной сессией БД.
    """
    return CurrencyRepository(session=session)


def get_currency_service(
        repository: Annotated[CurrencyRepository, Depends(get_currency_repository)],
) -> CurrencyService:
    """Провайдер для CurrencyService. Создает экземпляр сервиса для валют с готовым репозиторием."""
    return CurrencyService(repository=repository)


def get_exchange_rate_repository(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> ExchangeRateRepository:
    """
    Провайдер для CurrencyRepository.

    Создает экземпляр репозитория для операций с обменными курсами с активной сессией БД.
    """
    return ExchangeRateRepository(session=session)


def get_exchange_rate_service(
        repository: Annotated[ExchangeRateRepository, Depends(get_exchange_rate_repository)],
        currency_service: Annotated[CurrencyService, Depends(get_currency_service)],
) -> ExchangeRateService:
    """
    Провайдер для CurrencyService.

    Создает экземпляр сервиса для обменного курса с готовым репозиторием.
    """
    return ExchangeRateService(repository=repository, currency_service=currency_service)
