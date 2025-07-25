from typing import Sequence

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.currency import Currency


class CurrencyRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def currency_exists(self, code: str) -> bool:
        """
        Проверяет существование валюты по её коду.

        Возвращает True, если валюта существует, иначе False.
        """
        query = select(exists(Currency).where(Currency.code == code))
        result = await self.session.scalar(query)
        return bool(result)

    async def create_currency(self, code: str, name: str, sign: str) -> Currency:
        new_currency = Currency(code=code, name=name, sign=sign)
        self.session.add(new_currency)
        await self.session.flush()
        return new_currency

    async def get_all_currencies(self) -> Sequence[Currency]:
        """Получает список всех валют."""
        result = await self.session.execute(select(Currency))
        return result.scalars().all()

    async def get_currency_by_code(self, code: str):
        """Получает одну валюту по её коду."""
        query = select(Currency).where(Currency.code == code)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_codes_and_id_by_codes(self, codes: list[str]) -> list[tuple[str, int]]:
        """Получает список кортежей (code, id) по списку кодов валют."""
        query = select(Currency.code, Currency.id).where(Currency.code.in_(codes))
        result = await self.session.execute(query)
        return result.all()
