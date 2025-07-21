import logging
from pathlib import Path

import yaml
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def ASYNC_DATABASE_URL(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:"
                f"{self.DB_PORT}/{self.DB_NAME}")


settings = Settings()

LOGGING_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "logging_config.yaml"


def setup_logging():
    """Загружает конфигурацию логгирования из YAML файла и применяет ее."""
    with open(LOGGING_CONFIG_PATH) as conf:
        logging_config = yaml.safe_load(conf)

    logging.config.dictConfig(logging_config)
    logging.getLogger().info("Логгирование успешно настроено из файла.")
