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
        await self.session.flush([new_currency])
        return new_currency

    async def get_all_currencies(self) -> list[Currency]:
        """Получает список всех валют."""
        result = await self.session.execute(select(Currency))
        return result.scalars().all()
