import logging

from asyncpg import PostgresError
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.exceptions.exceptions import CurrencyNotExistsError, CurrencyExistsError, \
    ExchangeRateNotExistsError, ExchangeRateExistsError, SameCurrencyConversionError

log = logging.getLogger(__name__)

PYDANTIC_ERROR_MESSAGES = {
    "string_pattern_mismatch": "Код валюты должен состоять из 3 букв латинского алфавита.",
    "greater_than": "Поле '{field_name}' должно быть больше {limit_value}.",
    "value_error": "{original_msg}",
    "missing": "Поле '{field_name}' является обязательным.",
    "decimal_parsing": "Поле '{field_name}' должно быть числом. Для десятичной части используй точку",
    "string_too_short": "Поле '{field_name}' должно быть больше одного символа."
}


async def database_connection_exception_handler(request: Request, exc: PostgresError):
    log.exception("Ошибка уровня DBAPI-драйвера (psycopg2).", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Сервис временно недоступен. База данных недоступна."}
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    log.error("Ошибка базы данных при запросе: %s %s", request.method, request.url.path, exc_info=exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Сервис временно недоступен. Ошибка в базе данных."}
    )


async def currency_not_found_handler(request: Request, exc: CurrencyNotExistsError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Валюта не найдена"}
    )


async def currency_exists_handler(request: Request, exc: CurrencyExistsError):
    log.warning(f"Валюта уже есть в БД, {request.method}, {request.url.path}, {exc}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "Такая валюта уже существует."}
    )


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """
    Кастомный обработчик ошибок валидации Pydantic.

    Формирует понятный для пользователя ответ со всеми ошибками.
    """
    field_name = str(exc.errors()[0]["loc"][-1])
    error_type = exc.errors()[0]["type"]

    template = PYDANTIC_ERROR_MESSAGES.get(error_type, exc.errors()[0]['msg'])

    message = template.format(
        field_name=field_name,
        limit_value=exc.errors()[0].get('ctx', {}).get("gt"),
        original_msg=exc.errors()[0].get("msg")
    )

    log.warning(f"Ошибка валидации данных: {message}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": message}
    )


async def exchange_rate_not_found_handler(request: Request, exc: ExchangeRateNotExistsError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": "Обменного курса данных валют нет в БД"}
    )


async def exchange_rate_exists_handler(request: Request, exc: ExchangeRateExistsError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"message": "Такая валютная пара уже существует"}
    )


async def same_currency_exception_handler(request: Request, exc: SameCurrencyConversionError):
    log.warning(f"Конвертация валюты в саму себя, {request.method}, {request.url.path}, {exc}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Нельзя конвертировать валюту в саму себя"}
    )


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={"message": "Запрашиваемый ресурс не найден. Проверьте URL."},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики исключений для FastAPI приложения."""
    app.add_exception_handler(PostgresError, database_connection_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(CurrencyNotExistsError, currency_not_found_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(CurrencyExistsError, currency_exists_handler)
    app.add_exception_handler(ExchangeRateNotExistsError, exchange_rate_not_found_handler)
    app.add_exception_handler(ExchangeRateExistsError, exchange_rate_exists_handler)
    app.add_exception_handler(SameCurrencyConversionError, same_currency_exception_handler)
    app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
