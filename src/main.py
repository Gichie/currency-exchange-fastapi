from asyncpg import PostgresError
from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from src.api import main_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")
app.include_router(main_router)


@app.exception_handler(PostgresError)
async def database_connection_exception_handler(request: Request, exc: PostgresError):
    # todo logging
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Сервис временно недоступен. База данных недоступна."}
    )


