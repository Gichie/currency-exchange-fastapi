import logging
from typing import Annotated

from fastapi import APIRouter, Form, Depends

from src.core.dependencies import get_currency_service
from src.models.currency import Currency
from src.schemas.currency import CurrencyCreate, CurrencyRead
from src.services.currency_service import CurrencyService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/currencies", response_model=list[CurrencyRead])
async def get_currencies(service: CurrencyService = Depends(get_currency_service)):
    log.info("Запрос на получение списка всех валют. Method: GET. Path: /currencies")
    all_currencies = await service.get_all_currencies()
    log.info("Список валют успешно получен")
    return all_currencies


@router.get("currency/{code}", response_model=CurrencyRead)
async def get_currency_by_code(service: CurrencyService = Depends(get_currency_service)):
    log.info("Запрос на получение одной валюты по коду. Method: GET. Path: /currency/{code}")
    currency = await service.get_currency_by_code(code)

@router.post("/currencies", response_model=CurrencyRead)
async def create_currency(
        currency: Annotated[CurrencyCreate, Form()],
        service: CurrencyService = Depends(get_currency_service),
) -> Currency:
    new_currency = await service.create_currency(currency)

    return new_currency
