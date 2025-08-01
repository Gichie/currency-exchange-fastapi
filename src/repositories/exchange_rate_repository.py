from decimal import Decimal

from sqlalchemy import select, exists, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, aliased, contains_eager

from src.exceptions.exceptions import ExchangeRateNotExistsError
from src.models.currency import Currency
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

    async def create_exchange_rate(self, base_id: int, target_id: int, rate: Decimal) -> ExchangeRate:
        """Создает обменный курс для валютной пары."""
        new_exchange_rate = ExchangeRate(
            base_currency_id=base_id, target_currency_id=target_id, rate=rate
        )
        self.session.add(new_exchange_rate)
        await self.session.flush()
        return new_exchange_rate

    async def update_exchange_rate(self, base_id: int, target_id: int, rate: Decimal) -> ExchangeRate:
        """Обновляет обменный курс для валютной пары."""
        stmt = (update(ExchangeRate).where(
            ExchangeRate.base_currency_id == base_id,
            ExchangeRate.target_currency_id == target_id
        ).values(rate=rate).returning(ExchangeRate))

        result = await self.session.execute(stmt)

        updated_exchange_rate = result.scalar_one_or_none()

        if not updated_exchange_rate:
            raise ExchangeRateNotExistsError()

        await self.session.refresh(updated_exchange_rate, ['base_currency', 'target_currency'])

        return updated_exchange_rate

    async def get_rate_by_codes(self, base_code: str, target_code: str) -> ExchangeRate | None:
        BaseCurrency = aliased(Currency)
        TargetCurrency = aliased(Currency)

        query = (
            select(ExchangeRate)
            .join(BaseCurrency, ExchangeRate.base_currency_id == BaseCurrency.id)
            .join(TargetCurrency, ExchangeRate.target_currency_id == TargetCurrency.id)
            .where(BaseCurrency.code == base_code, TargetCurrency.code == target_code)
            .options(
                contains_eager(ExchangeRate.base_currency, alias=BaseCurrency),
                contains_eager(ExchangeRate.target_currency, alias=TargetCurrency)
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_exchange_rates(self, possible_pairs: list[tuple[str, str]]) -> list[ExchangeRate]:
        BaseCurrency = aliased(Currency)
        TargetCurrency = aliased(Currency)

        conditions = [
            and_(
                BaseCurrency.code == base, TargetCurrency.code == target
            ) for base, target in possible_pairs
        ]

        if not conditions:
            return []

        query = (
            select(ExchangeRate)
            .join(BaseCurrency, ExchangeRate.base_currency_id == BaseCurrency.id)
            .join(TargetCurrency, ExchangeRate.target_currency_id == TargetCurrency.id)
            .where(or_(*conditions))
            .options(
                contains_eager(ExchangeRate.base_currency, alias=BaseCurrency),
                contains_eager(ExchangeRate.target_currency, alias=TargetCurrency)
            )
        )

        result = await self.session.execute(query)
        return result.scalars().all()
