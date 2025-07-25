class CurrencyExchangeError(Exception):
    """Базовое исключение."""
    pass


class CurrencyNotExistsError(CurrencyExchangeError):
    """Исключение при отсутствии валюты в БД"""
    pass


class CurrencyExistsError(CurrencyExchangeError):
    """Исключение возникает если в БД уже имеется код запрошенной валюты."""


class ExchangeRateNotExistsError(CurrencyExchangeError):
    """Исключение при отсутствии обменного курса в БД"""
    pass


class ExchangeRateExistsError(CurrencyExchangeError):
    """Исключение при наличии обменного курса в БД"""
    pass
