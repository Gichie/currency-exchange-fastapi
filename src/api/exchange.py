import logging
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.core.dependencies import get_exchange_rate_service
from src.schemas.exchange_rate import ExchangeCurrencyResponse
from src.services.exchange_rate_service import ExchangeRateService

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/exchange", response_model=ExchangeCurrencyResponse)
async def exchange_currencies(
        base_currency: Annotated[str, Query(alias='from', pattern="^[a-zA-Z]{3}$")],
        target_currency: Annotated[str, Query(alias='to', pattern="^[a-zA-Z]{3}$")],
        amount: Annotated[Decimal, Query(gt=0, max_digits=18, decimal_places=2)],
        service: ExchangeRateService = Depends(get_exchange_rate_service),
):
    log.info(f"Запрос на конвертацию валют {base_currency}/{target_currency}. Количество: {amount}.")
    response = await service.exchange_currencies(base_currency, target_currency, amount)
    return response
