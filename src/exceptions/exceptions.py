class CurrencyExchangeError(Exception):
    """Базовое исключение."""
    pass


class CurrencyNotExistError(CurrencyExchangeError):
    """Исключение при отсутствии валюты в БД"""
    pass
