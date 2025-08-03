from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy.

    Предоставляет функциональность ORM через наследование от DeclarativeBase.
    Все модели должны наследоваться от этого класса.
    """
    pass
