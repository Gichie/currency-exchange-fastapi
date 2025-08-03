from collections.abc import Sequence

from sqlalchemy import Row, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.currency import Currency


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_currency(self, code: str, name: str, sign: str) -> Currency:
        new_currency = Currency(code=code, name=name, sign=sign)
        self.session.add(new_currency)
        await self.session.flush()
        return new_currency

    async def get_all_currencies(self) -> Sequence[Currency]:
        """Получает список всех валют."""
        query_result = await self.session.execute(select(Currency))
        return query_result.scalars().all()

    async def get_currency_by_code(self, code: str) -> Currency | None:
        """Получает одну валюту по её коду."""
        query = select(Currency).where(Currency.code == code)
        query_result = await self.session.execute(query)
        return query_result.scalar_one_or_none()

    async def get_codes_and_id_by_codes(self, codes: list[str]) -> Sequence[Row]:
        """Получает список кортежей (code, id) по списку кодов валют."""
        query = select(Currency.code, Currency.id).where(Currency.code.in_(codes))
        query_result = await self.session.execute(query)
        return query_result.all()
