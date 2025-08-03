from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from src.exceptions.exceptions import SameCurrencyConversionError
from src.schemas.currency import CurrencyScheme


class ExchangeRateSchema(BaseModel):
    id: int
    base_currency: CurrencyScheme = Field(serialization_alias="baseCurrency")
    target_currency: CurrencyScheme = Field(serialization_alias="targetCurrency")
    rate: Decimal = Field(gt=0, max_digits=19, decimal_places=6)

    model_config = ConfigDict(from_attributes=True)


class ExchangeRateCreate(BaseModel):
    base_currency_code: str = Field(pattern="^[a-zA-Z]{3}$", alias="baseCurrencyCode")
    target_currency_code: str = Field(pattern="^[a-zA-Z]{3}$", alias="targetCurrencyCode")
    rate: Decimal = Field(gt=0, max_digits=19, decimal_places=6)

    @model_validator(mode="after")
    def check_currencies_not_same(self) -> "ExchangeRateCreate":
        if self.base_currency_code == self.target_currency_code:
            raise SameCurrencyConversionError
        return self


class ExchangeRateUpdate(BaseModel):
    rate: Decimal = Field(gt=0, max_digits=17, decimal_places=6)


class ExchangeCurrencyResponse(BaseModel):
    base_currency: CurrencyScheme = Field(serialization_alias="baseCurrency")
    target_currency: CurrencyScheme = Field(serialization_alias="targetCurrency")
    rate: Decimal = Field(gt=0, max_digits=19, decimal_places=6)
    amount: Decimal = Field(gt=0, max_digits=18, decimal_places=2)
    converted_amount: Decimal = Field(
        ge=0, max_digits=19, decimal_places=2, serialization_alias="convertedAmount",
    )
    model_config = ConfigDict(from_attributes=True)
