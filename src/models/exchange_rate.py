from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db.base import Base


class ExchangeRate(Base):
    __tablename__ = "exchange_rate"

    id: Mapped[int] = mapped_column(primary_key=True)
    base_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    target_currency_id: Mapped[int] = mapped_column(ForeignKey("currency.id"), nullable=False)
    rate: Mapped[Decimal] = mapped_column(Numeric(precision=17, scale=6), nullable=False)

    base_currency: Mapped["Currency"] = relationship(
        foreign_keys=[base_currency_id],
        back_populates="base"
    )
    target_currency: Mapped["Currency"] = relationship(
        foreign_keys=[target_currency_id],
        back_populates="target"
    )

    __table_args__ = (
        UniqueConstraint("base_currency_id", "target_currency_id", name="uq_base_target_currencies"),
    )
