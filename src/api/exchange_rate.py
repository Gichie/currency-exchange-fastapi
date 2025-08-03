import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Form, Path
from starlette import status

from src.core.dependencies import get_exchange_rate_service
from src.schemas.exchange_rate import ExchangeRateCreate, ExchangeRateSchema, ExchangeRateUpdate
from src.services.exchange_rate_service import ExchangeRateService

log = logging.getLogger(__name__)
router = APIRouter()


@router.get("/exchangeRates", response_model=list[ExchangeRateSchema])
async def get_exchange_rates(service: ExchangeRateService = Depends(get_exchange_rate_service)) -> Any:
    all_exchange_rates = await service.get_all_exchange_rates()
    return list(all_exchange_rates)


@router.get("/exchangeRate/{code_pair}", response_model=ExchangeRateSchema)
async def exchange_rate_by_code_pair(
        code_pair: Annotated[str, Path(pattern="^[a-zA-Z]{6}$")],
        service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> Any:
    log.info(f"Запрос на получение обменного курса по валютной паре. "
             f"Method: GET. Path: /exchangeRate/{code_pair}")

    base_currency, target_currency = service.parse_codes(code_pair)
    return await service.get_exchange_rate_by_codes(base_currency, target_currency)


@router.post("/exchangeRates", response_model=ExchangeRateSchema, status_code=status.HTTP_201_CREATED)
async def create_exchange_rate(
        exchange_rate: Annotated[ExchangeRateCreate, Form()],
        service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> Any:
    log.info("Запрос на создание обменного курса. Method: POST. Path: /exchangeRates")
    return await service.create_exchange_rate(exchange_rate)


@router.patch("/exchangeRate/{code_pair}", response_model=ExchangeRateSchema)
async def update_exchange_rate(
        code_pair: Annotated[str, Path(pattern="^[a-zA-Z]{6}$")],
        rate_form: Annotated[ExchangeRateUpdate, Form()],
        service: ExchangeRateService = Depends(get_exchange_rate_service),
) -> Any:
    log.info(f"Запрос на обновление обменного курса. Method: PATCH. Path: /exchangeRate/{code_pair}")
    base_currency, target_currency = service.parse_codes(code_pair)
    return await service.update_exchange_rate(base_currency, target_currency, rate_form)
