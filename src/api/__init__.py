from fastapi import APIRouter

from src.api.currencies import router as currencies_router
from src.api.exchange_rate import router as exchange_rates_router
from src.api.exchange import router as exchange_router

main_router = APIRouter()
main_router.include_router(currencies_router, tags=["Currencies"])
main_router.include_router(exchange_rates_router, tags=["Exchange Rates"])
main_router.include_router(exchange_router, tags=["Exchange"])
