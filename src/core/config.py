import logging
from pathlib import Path

import yaml
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    @property
    def ASYNC_DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()

LOGGING_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "logging_config.yaml"


def setup_logging() -> None:
    """Загружает конфигурацию логгирования из YAML файла и применяет ее."""
    with open(LOGGING_CONFIG_PATH) as conf:
        logging_config = yaml.safe_load(conf)

    logging.config.dictConfig(logging_config)
    logging.getLogger().info("Логгирование успешно настроено из файла.")
