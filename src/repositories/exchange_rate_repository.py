from decimal import Decimal

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.exceptions.exceptions import ExchangeRateNotExistsError
from src.models.exchange_rate import ExchangeRate


class ExchangeRateRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_exchange_rates(self) -> list[ExchangeRate]:
        """Получает список всех обменных курсов."""
        query = (select(ExchangeRate).options(
            joinedload(ExchangeRate.base_currency),
            joinedload(ExchangeRate.target_currency)
        ))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_exchange_rate_by_id_pair(self, base_id, target_id) -> ExchangeRate:
        """Получает один обменный курс по заданной кодовой паре валют."""
        query = (select(ExchangeRate).options(
            joinedload(ExchangeRate.base_currency),
            joinedload(ExchangeRate.target_currency)
        )).where(
            ExchangeRate.base_currency_id == base_id, ExchangeRate.target_currency_id == target_id
        )

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def exchange_rate_exists(self, base_code: int, target_code: int) -> bool:
        """Проверяет наличие обменного курса в БД."""
        query = select(exists(ExchangeRate).where(
            ExchangeRate.base_currency_id == base_code, ExchangeRate.target_currency_id == target_code
        ))
        result = await self.session.scalar(query)
        return bool(result)

    async def create_exchange_rate(self, base_id: int, target_id: int, rate: Decimal) -> None:
        """Создает обменный курс для валютной пары."""
        new_exchange_rate = ExchangeRate(
            base_currency_id=base_id, target_currency_id=target_id, rate=rate
        )
        self.session.add(new_exchange_rate)
        await self.session.flush()

    async def update_exchange_rate(self, base_id: int, target_id: int, rate: Decimal) -> ExchangeRate:
        """Обновляет обменный курс для валютной пары."""
        exchange_rate = await self.get_exchange_rate_by_id_pair(base_id, target_id)

        if not exchange_rate:
            raise ExchangeRateNotExistsError()

        exchange_rate.rate = rate
        return exchange_rate


