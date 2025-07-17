from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from currency_exchange.core.db import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rate"

    id: Mapped[int] = mapped_column(primary_key=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    rate: Mapped[Decimal] = mapped_column(Numeric(precision=7, scale=6), nullable=False)

    __table_args__ = (
        UniqueConstraint("base_currency_id", "target_currency_id", name="uq_base_target_currencies")
    )

