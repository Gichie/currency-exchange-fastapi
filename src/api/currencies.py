import logging
from typing import Annotated

from fastapi import APIRouter, Form, Depends, Path
from starlette import status

from src.core.dependencies import get_currency_service
from src.schemas.currency import CurrencyBase
from src.services.currency_service import CurrencyService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/currencies", response_model=list[CurrencyBase])
async def get_currencies(service: CurrencyService = Depends(get_currency_service)):
    log.info("Запрос на получение списка всех валют. Method: GET. Path: /currencies")
    all_currencies = await service.get_all_currencies()
    return all_currencies


@router.get("/currency/{code}", response_model=CurrencyBase)
async def get_currency_by_code(
        code: Annotated[str, Path(pattern="^[a-zA-Z]{3}$")],
        service: CurrencyService = Depends(get_currency_service)
):
    log.info(f"Запрос на получение одной валюты по коду. Method: GET. Path: /currency/{code}")
    currency = await service.get_currency_by_code(code)
    return currency


@router.get("/currency/", status_code=status.HTTP_400_BAD_REQUEST)
async def get_currency_missing_code():
    log.warning(f"Запрос на получение валюты без кода. Method: GET. Path: /currency/")
    return {"message": "Код валюты не указан"}


@router.post("/currencies", response_model=CurrencyBase, status_code=status.HTTP_201_CREATED)
async def create_currency(
        currency: Annotated[CurrencyBase, Form()],
        service: CurrencyService = Depends(get_currency_service)
):
    log.info(f"Запрос на создание валюты. Method: POST. Path: /currencies")
    new_currency = await service.create_currency(currency)

    return new_currency
