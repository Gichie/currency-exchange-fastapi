import logging
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.exc import IntegrityError

from src.exceptions.exceptions import ExchangeRateNotExistsError, ExchangeRateExistsError, \
    SameCurrencyConversionError
from src.models.exchange_rate import ExchangeRate
from src.repositories.exchange_rate_repository import ExchangeRateRepository
from src.schemas.exchange_rate import ExchangeRateCreate, ExchangeRateUpdate, ExchangeRateSchema, \
    ExchangeCurrencyResponse
from src.services.currency_service import CurrencyService

log = logging.getLogger(__name__)


class ExchangeRateService:
    def __init__(self, repository: ExchangeRateRepository, currency_service: CurrencyService):
        self.repository = repository
        self.currency_service = currency_service

    async def get_all_exchange_rates(self) -> list[ExchangeRate]:
        return await self.repository.get_all_exchange_rates()

    @staticmethod
    def parse_codes(code_pair: str) -> tuple[str, str]:
        base_code = code_pair[:3].upper()
        target_code = code_pair[3:].upper()
        return base_code, target_code

    async def get_exchange_rate_by_codes(self, base_code: str, target_code: str) -> ExchangeRate:
        exchange_rate = await self.repository.get_rate_by_codes(base_code, target_code)

        if not exchange_rate:
            log.warning(f"Обменного курса данных валют ({base_code}/{target_code}) нет в БД")
            raise ExchangeRateNotExistsError()

        return exchange_rate

    async def exchange_currencies(self, base_currency: str, target_currency: str, amount: Decimal):
        base_currency = base_currency.upper()
        target_currency = target_currency.upper()
        straight_exchange_rate = None

        if base_currency == target_currency:
            raise SameCurrencyConversionError()

        try:
            straight_exchange_rate = await self.get_exchange_rate_by_codes(base_currency, target_currency)
            rate = straight_exchange_rate.rate
        except ExchangeRateNotExistsError:
            try:
                log.info(
                    f"Попытка конвертировать по обратному курсу {target_currency}/{base_currency}"
                )
                reverse_exchange_rate = await self.get_exchange_rate_by_codes(target_currency, base_currency)
                rate = 1 / reverse_exchange_rate.rate
            except ExchangeRateNotExistsError:
                log.info("Попытка конвертировать через USD")
                rate = await self._conversion_through_usd(base_currency, target_currency)

        rate = rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)

        converted_amount = (rate * amount).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if straight_exchange_rate:
            base_data = ExchangeRateSchema.model_validate(straight_exchange_rate)
            response_schema = ExchangeCurrencyResponse(
                **base_data.model_dump(), amount=amount, converted_amount=converted_amount
            )
        else:
            base_currency_model = await self.currency_service.get_currency_by_code(base_currency)
            target_currency_model = await self.currency_service.get_currency_by_code(target_currency)

            prepared_data = {
                "id": 1,
                "base_currency": base_currency_model,
                "target_currency": target_currency_model,
                "rate": rate,
                "amount": amount,
                "converted_amount": converted_amount
            }
            response_schema = ExchangeCurrencyResponse.model_validate(prepared_data)

        return response_schema

    async def _conversion_through_usd(self, base_currency: str, target_currency: str):
        usd_base_rate = await self.get_exchange_rate_by_codes("USD", base_currency)
        usd_target_rate = await self.get_exchange_rate_by_codes("USD", target_currency)
        base_to_target_rate = usd_target_rate.rate / usd_base_rate.rate
        return base_to_target_rate

    async def create_exchange_rate(self, exchange_rate: ExchangeRateCreate) -> ExchangeRate:
        base_code = exchange_rate.base_currency_code.upper()
        target_code = exchange_rate.target_currency_code.upper()
        rate = exchange_rate.rate

        async with self.repository.session.begin():
            base_id, target_id = await self._get_pair_currencies_id(
                base_code, target_code
            )
            try:
                new_exchange_rate = await self.repository.create_exchange_rate(
                    base_id, target_id, rate
                )
            except IntegrityError:
                raise ExchangeRateExistsError()

        await self.repository.session.refresh(new_exchange_rate, ['base_currency', 'target_currency'])

        return new_exchange_rate

    async def _get_pair_currencies_id(
            self, base_currency_code: str, target_currency_code: str
    ) -> tuple[int, int]:
        currencies_data = await self.currency_service.get_codes_and_id_by_codes(
            [base_currency_code, target_currency_code]
        )
        base_id = currencies_data[base_currency_code]
        target_id = currencies_data[target_currency_code]
        return base_id, target_id

    async def update_exchange_rate(
            self, base_code: str, target_code: str, rate_form: ExchangeRateUpdate
    ) -> ExchangeRate:
        rate = rate_form.rate

        async with self.repository.session.begin():
            base_id, target_id = await self._get_pair_currencies_id(
                base_code, target_code
            )

            exchange_rate = await self.repository.update_exchange_rate(base_id, target_id, rate)

        return exchange_rate
