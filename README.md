# Exchange Currency - Обменник валют

[![Python Version](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![Linter](https://img.shields.io/badge/linting-ruff-brightgreen)](https://github.com/astral-sh/ruff)

REST API для обмена валют. Учебный проект в рамках roadmap'а [Python Backend Developer](https://zhukovsd.github.io/python-backend-learning-course/projects/currency-exchange/).
Проект позволяет управлять списком валют, задавать обменные курсы и выполнять конвертацию между валютными парами. 
Основная цель — отработка навыков работы с FastAPI, SQLAlchemy 2.0, Pydantic 2, Docker


## Стек технологий

| Категория       | Технология                                      |
|-----------------|-------------------------------------------------|
| **Backend**     | Python 3.13, FastAPI 0.116.1, Pydantic 2.11.7   |
| **Базы данных** | PostgreSQL                                      |
| **ORM**         | SQLAlchemy 2.0 (Async), Alembic (для миграций)  |
| **Инструменты** | Docker, Docker Compose, Poetry, Mypy, Ruff      |

## Установка и запуск

Проект полностью контейнеризирован, для запуска требуется только git, Docker и Docker Compose.

1.  **Клонируйте репозиторий:**
    ```bash
    git clone https://github.com/Gichie/currency-exchange-fastapi.git
    cd currency-exchange-fastapi
    ```

2.  **Создайте файл `.env`:** и заполните своими данными.

    Для linux:
    ```bash
    nano .env
    ```
    Для windows powershell:
    ```
    notepad .env
    ```
    Примерное содержимое файла .env.

```env
POSTGRES_HOST=db
POSTGRES_DB=currency_exchanger_db
POSTGRES_USER=currency_exchanger_user
POSTGRES_PASSWORD=1234
POSTGRES_PORT=5432
```

3.  **Соберите и запустите контейнеры:**
    ```bash
    docker compose up --build -d
    ```
4.  Фронтенд будет доступен по адресу: `http://localhost`.
5.  Интерактивная документация (Swagger UI) доступна по адресу `http://localhost/docs`.