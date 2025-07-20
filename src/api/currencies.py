from typing import Annotated

from fastapi import APIRouter, Form, Depends

from src.core.dependencies import get_currency_service
from src.models.currency import Currency

from src.schemas.currency import CurrencyCreate, CurrencyRead
from src.services.currency_service import CurrencyService

router = APIRouter()


@router.get("/", response_model=list[CurrencyRead])
async def get_currencies(service: CurrencyService = Depends(get_currency_service)):
    all_currencies = await service.get_all_currencies()
    return all_currencies


@router.post("/", response_model=CurrencyRead)
async def create_currency(
        currency: Annotated[CurrencyCreate, Form()],
        service: CurrencyService = Depends(get_currency_service),
) -> Currency:
    new_currency = await service.create_currency(currency)

    return new_currency
