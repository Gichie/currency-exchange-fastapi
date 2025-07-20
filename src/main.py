from pathlib import Path

import yaml
from asyncpg import PostgresError
from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
import logging
from src.api import main_router


CONFIG_PATH = Path(__file__).resolve().parent.parent / "logging_config.yaml"

with open(CONFIG_PATH) as f:
    logging_config = yaml.safe_load(f)

logging.config.dictConfig(logging_config)


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(main_router)


@app.exception_handler(PostgresError)
async def database_connection_exception_handler(request: Request, exc: PostgresError):
    # todo logging
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"message": "Сервис временно недоступен. База данных недоступна."}
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    # todo logging
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Сервис временно недоступен. Ошибка в базе данных."}
    )
