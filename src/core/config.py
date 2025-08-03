import logging.config
from pathlib import Path

import yaml
from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv())

    postgres_db: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_port: int

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()

LOGGING_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "logging_config.yaml"


def setup_logging() -> None:
    """Загружает конфигурацию логгирования из YAML файла и применяет ее."""
    with LOGGING_CONFIG_PATH.open() as conf:
        logging_config = yaml.safe_load(conf)

    logging.config.dictConfig(logging_config)
    logging.getLogger().info("Логгирование успешно настроено из файла.")
