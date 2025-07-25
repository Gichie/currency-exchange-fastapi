import logging
from decimal import Decimal

from src.exceptions.exceptions import ExchangeRateNotExistsError, ExchangeRateExistsError
from src.models.exchange_rate import ExchangeRate
from src.repositories.exchange_rate_repository import ExchangeRateRepository
from src.schemas.exchange_rate import ExchangeRateCreate, ExchangeRateUpdate
from src.services.currency_service import CurrencyService

log = logging.getLogger(__name__)


class ExchangeRateService:
    def __init__(self, repository: ExchangeRateRepository, currency_service: CurrencyService):
        self.repository = repository
        self.currency_service = currency_service

    async def get_all_exchange_rates(self) -> list[ExchangeRate]:
        return await self.repository.get_all_exchange_rates()

    async def get_exchange_rate(self, code_pair: str) -> ExchangeRate:
        base_code = code_pair[:3].upper()
        target_code = code_pair[3:].upper()

        base_id, target_id = await self._get_pair_currencies_id(
            base_code, target_code
        )

        exchange_rate = await self.repository.get_exchange_rate_by_id_pair(base_id, target_id)

        if not exchange_rate:
            log.warning(f"Обменного курса данных валют ({base_code}/{target_code}) нет в БД")
            raise ExchangeRateNotExistsError()

        return exchange_rate

    async def create_exchange_rate(self, exchange_rate: ExchangeRateCreate) -> ExchangeRate:
        base_code = exchange_rate.base_currency_code.upper()
        target_code = exchange_rate.target_currency_code.upper()
        rate = exchange_rate.rate

        async with self.repository.session.begin():
            base_id, target_id = await self._get_pair_currencies_id(
                base_code, target_code
            )

            if await self.repository.exchange_rate_exists(base_id, target_id):
                log.warning(
                    f"Заданный обменный курс ({base_code}/{target_code})"
                    f"уже есть в БД."
                )
                raise ExchangeRateExistsError()

            await self.repository.create_exchange_rate(base_id, target_id, rate)

        new_exchange_rate = await self.repository.get_exchange_rate_by_id_pair(base_id, target_id)
        return new_exchange_rate

    async def _get_pair_currencies_id(self, base_currency_code, target_currency_code):
        currencies_data = await self.currency_service.get_codes_and_id_by_codes(
            [base_currency_code, target_currency_code]
        )
        base_id = currencies_data[base_currency_code]
        target_id = currencies_data[target_currency_code]
        return base_id, target_id

    async def update_exchange_rate(self, code_pair: str, rate_form: ExchangeRateUpdate) -> ExchangeRate:
        base_code = code_pair[:3].upper()
        target_code = code_pair[3:].upper()
        rate = rate_form.rate

        async with self.repository.session.begin():
            base_id, target_id = await self._get_pair_currencies_id(
                base_code, target_code
            )

            if not await self.repository.exchange_rate_exists(base_id, target_id):
                log.warning(
                    f"Заданный обменный курс ({base_code}/{target_code})"
                    f"уже есть в БД."
                )
                raise ExchangeRateNotExistsError()

            exchange_rate = await self.repository.update_exchange_rate(base_id, target_id, rate)

        return exchange_rate
