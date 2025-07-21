import logging

from asyncpg import PostgresError
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

log = logging.getLogger(__name__)


async def database_connection_exception_handler(request: Request, exc: PostgresError):
    log.exception("Ошибка уровня DBAPI-драйвера (psycopg2).", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Сервис временно недоступен. База данных недоступна."}
    )


async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    log.exception("Ошибка в ORM SQLAlchemy", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Сервис временно недоступен. Ошибка в базе данных."}
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики исключений для FastAPI приложения."""
    app.add_exception_handler(PostgresError, database_connection_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
