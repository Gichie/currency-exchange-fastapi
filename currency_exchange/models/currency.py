from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from currency_exchange.core.db.base import Base


class Currency(Base):
    __tablename__ = "currency"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    sign: Mapped[str] = mapped_column(String(8), nullable=False)
