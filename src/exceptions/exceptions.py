class CurrencyExchangeError(Exception):
    """Базовое исключение."""


class CurrencyNotExistsError(CurrencyExchangeError):
    """Исключение при отсутствии валюты в БД"""


class CurrencyExistsError(CurrencyExchangeError):
    """Исключение возникает если в БД уже имеется код запрошенной валюты."""


class ExchangeRateNotExistsError(CurrencyExchangeError):
    """Исключение при отсутствии обменного курса в БД"""


class ExchangeRateExistsError(CurrencyExchangeError):
    """Исключение при наличии обменного курса в БД"""


class SameCurrencyConversionError(CurrencyExchangeError):
    """Исключение при конвертации валюты в саму себя"""
