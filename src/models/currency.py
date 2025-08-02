from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import Base

if TYPE_CHECKING:
    from .exchange_rate import ExchangeRate


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    sign: Mapped[str] = mapped_column(String(8), nullable=False)

    base: Mapped[list["ExchangeRate"]] = relationship(
        back_populates="base_currency",
        foreign_keys="ExchangeRate.base_currency_id"
    )

    target: Mapped[list["ExchangeRate"]] = relationship(
        back_populates="target_currency",
        foreign_keys="ExchangeRate.target_currency_id"
    )
