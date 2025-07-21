import logging
from typing import Sequence

from src.exceptions.exceptions import CurrencyNotExistError
from src.models.currency import Currency
from src.repositories.currency import CurrencyRepository
from src.schemas.currency import CurrencyCreate

log = logging.getLogger(__name__)


class CurrencyService:
    def __init__(self, repository: CurrencyRepository):
        self.repository = repository

    async def create_currency(self, currency_data: CurrencyCreate) -> Currency:
        code: str = currency_data.code
        name: str = currency_data.name
        sign: str = currency_data.sign

        async with self.repository.session.begin():
            if await self.repository.currency_exists(code):
                raise Exception

            new_currency = await self.repository.create_currency(code, name, sign)

        await self.repository.session.refresh(new_currency)

        return new_currency

    async def get_all_currencies(self) -> Sequence[Currency]:
        async with self.repository.session.begin():
            all_currencies = await self.repository.get_all_currencies()

        return all_currencies

    async def get_currency_by_code(self, code: str) -> Currency:
        currency = await self.repository.get_currency_by_code(code.upper())
        if currency:
            return currency
        log.warning(f"Данной валюты: {code} нет в БД")
        raise CurrencyNotExistError
