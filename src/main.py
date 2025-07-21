from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.api import main_router
from src.core.config import setup_logging
from src.exceptions.handlers import register_exception_handlers

setup_logging()
app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

register_exception_handlers(app)
app.include_router(main_router)
