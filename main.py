from typing import Annotated

from fastapi import FastAPI, Form
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from currency_exchange.schemas.currency import CurrencySchema

app = FastAPI()

app.mount("/static", StaticFiles(directory="currency_exchange/static"), name="static")

fake_db = [{"code": "QQQ", "name": "fsdfdsffds", "sign": "x"}]


@app.get("/")
async def root():
    return FileResponse("currency_exchange/static/templates/index.html")


@app.get("/currencies")
async def get_currencies():
    return fake_db


@app.post("/currencies")
async def add_currency(currency: Annotated[CurrencySchema, Form()]):
    return currency


@app.get("/exchangeRates")
async def get_exchange_rates():
    return
