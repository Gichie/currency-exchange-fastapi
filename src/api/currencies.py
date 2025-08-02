import logging
from typing import Annotated, Any

from fastapi import APIRouter, Form, Depends, Path
from starlette import status

from src.core.dependencies import get_currency_service
from src.schemas.currency import CurrencyScheme
from src.services.currency_service import CurrencyService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/currencies", response_model=list[CurrencyScheme])
async def get_currencies(service: CurrencyService = Depends(get_currency_service)) -> Any:
    log.info("Запрос на получение списка всех валют. Method: GET. Path: /currencies")
    all_currencies = await service.get_all_currencies()
    return all_currencies


@router.get("/currency/{code}", response_model=CurrencyScheme)
async def get_currency_by_code(
        code: Annotated[str, Path(pattern="^[a-zA-Z]{3}$")],
        service: CurrencyService = Depends(get_currency_service)
) -> Any:
    log.info(f"Запрос на получение одной валюты по коду. Method: GET. Path: /currency/{code}")
    currency = await service.get_currency_by_code(code)
    return currency


@router.post("/currencies", response_model=CurrencyScheme, status_code=status.HTTP_201_CREATED)
async def create_currency(
        currency: Annotated[CurrencyScheme, Form()],
        service: CurrencyService = Depends(get_currency_service)
) -> Any:
    log.info(f"Запрос на создание валюты. Method: POST. Path: /currencies")
    new_currency = await service.create_currency(currency)

    return new_currency
