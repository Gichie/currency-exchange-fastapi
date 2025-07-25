from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from src.schemas.currency import CurrencyBase


class ExchangeRateSchema(BaseModel):
    id: int
    base_currency: CurrencyBase = Field(serialization_alias="baseCurrency")
    target_currency: CurrencyBase = Field(serialization_alias="targetCurrency")
    rate: Decimal = Field(gt=0, max_digits=17, decimal_places=6)


class ExchangeRateCreate(BaseModel):
    base_currency_code: str = Field(pattern="^[a-zA-Z]{3}$", alias="baseCurrencyCode")
    target_currency_code: str = Field(pattern="^[a-zA-Z]{3}$", alias="targetCurrencyCode")
    rate: Decimal = Field(gt=0, max_digits=17, decimal_places=6)

    @model_validator(mode='after')
    def check_currencies_not_same(self) -> 'ExchangeRateCreate':
        if self.base_currency_code == self.target_currency_code:
            raise ValueError("Валюты не могут быть одинаковыми")
        return self


class ExchangeRateUpdate(BaseModel):
    rate: Decimal = Field(gt=0, max_digits=17, decimal_places=6)
