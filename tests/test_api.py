from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from starlette import status

from src.schemas.currency import CurrencyScheme
from tests.conftest import CURRENCIES


@pytest.mark.asyncio
async def test_currencies(ac: AsyncClient, mock_currency_service: AsyncMock):
    """Тестирует эндпоинт получения списка валют."""
    response = await ac.get("/currencies")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == CURRENCIES
    mock_currency_service.get_all_currencies.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_currencies_database_error(
        ac: AsyncClient, mock_currency_service_db_error: AsyncMock
):
    """Тест: вызов ошибки в БД."""
    response = await ac.get("/currencies")

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.json() == {"message": "Сервис временно недоступен. Ошибка в базе данных."}

    mock_currency_service_db_error.get_all_currencies.assert_called_once()


@pytest.mark.asyncio
async def test_get_currency_by_code(ac: AsyncClient, mock_currency_service: AsyncMock):
    """Тест: получение существующей валюты по коду."""
    mock_currency_service.get_currency_by_code.return_value = CurrencyScheme(**CURRENCIES[0])

    response = await ac.get("/currency/USD")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == CURRENCIES[0]
    mock_currency_service.get_currency_by_code.assert_awaited_once_with('USD')


@pytest.mark.asyncio
async def test_create_currency_success(ac: AsyncClient, mock_currency_service: AsyncMock):
    """Тест: успешное создание новой валюты."""

    new_currency_data = {"code": "JPY", "name": "Japanese Yen", "sign": "¥"}

    created_currency_model = CurrencyScheme(id=99, **new_currency_data)

    mock_currency_service.create_currency.return_value = created_currency_model

    response = await ac.post("/currencies", data=new_currency_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == created_currency_model.model_dump()

    expected_payload_object = CurrencyScheme(**new_currency_data)
    mock_currency_service.create_currency.assert_awaited_once_with(expected_payload_object)