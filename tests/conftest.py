import logging.config
from collections.abc import Generator
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
import yaml
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import OperationalError

from src.core.config import LOGGING_CONFIG_PATH
from src.core.dependencies import get_currency_service
from src.main import app
from src.schemas.currency import CurrencyScheme
from src.services.currency_service import CurrencyService

CURRENCIES = [
    CurrencyScheme(id=1, code="USD", name="USDUSDUSD", sign="$"),
    CurrencyScheme(id=2, code="EUR", name="EUROPIAN", sign="eu")
]


def setup_project_logging() -> None:
    """
    Настраивает логгирование для проекта на основе YAML-конфига.

    Эта функция будет вызвана до того, как pytest перехватит управление.
    """
    config_path = LOGGING_CONFIG_PATH
    if config_path.is_file():
        with open(config_path) as f:
            logging_config = yaml.safe_load(f)
        logging.config.dictConfig(logging_config)
        print("\nКастомная конфигурация логгирования применена.")
    else:
        print(f"\nВнимание: Файл конфигурации логгирования не найден: {config_path}")


def pytest_configure() -> None:
    """Позволяет настроить конфигурацию перед запуском тестов."""
    setup_project_logging()


@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура, которая создает и предоставляет AsyncClient для тестов."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture
def mock_currency_service_db_error() -> Generator[AsyncMock]:
    """
    Фикстура для мокирования CurrencyService с ошибкой базы данных.

    Автоматически очищает dependency_overrides после завершения теста.
    """
    mock_service = AsyncMock(spec=CurrencyService)
    exc = OperationalError("DB connection failed", params=None, orig=BaseException())
    mock_service.get_all_currencies.side_effect = exc

    app.dependency_overrides[get_currency_service] = lambda: mock_service

    yield mock_service

    del app.dependency_overrides[get_currency_service]


@pytest.fixture
def mock_currency_service() -> Generator[AsyncMock]:
    """
    Фикстура для мокирования CurrencyService.

    Автоматически очищает dependency_overrides после завершения теста.
    """
    mock_service = AsyncMock(spec=CurrencyService)
    mock_service.get_all_currencies.return_value = CURRENCIES

    app.dependency_overrides[get_currency_service] = lambda: mock_service

    yield mock_service

    del app.dependency_overrides[get_currency_service]
