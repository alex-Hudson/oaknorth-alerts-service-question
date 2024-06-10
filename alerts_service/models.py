from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Alert(Base):
    __tablename__ = "alerts"
    alert_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    data_item: Mapped[str]
    operator: Mapped[str]
    value: Mapped[float]
    last_modified: Mapped[datetime] = mapped_column(
        server_default=sa.text("(now() at time zone 'utc')")
    )

    def __repr__(self) -> str:
        return f"Alert(alert_id={self.alert_id!r}, data_item={self.data_item!r}, operator={self.operator!r}, value={self.value!r}, last_modified={self.last_modified!r})"


class Borrower(Base):
    __tablename__ = "borrowers"

    borrower_id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str]
    total_revenue: Mapped[Optional[float]]
    ebitda: Mapped[Optional[float]]
    dscr: Mapped[Optional[float]]
    debt_to_ebitda: Mapped[Optional[float]]
    last_modified: Mapped[datetime] = mapped_column(
        server_default=sa.text("(now() at time zone 'utc')")
    )

    def __repr__(self) -> str:
        return (
            f"Borrower(borrower_id={self.borrower_id!r}, "
            f"name={self.name!r}, "
            f"total_revenue={self.total_revenue!r}), "
            f"ebitda={self.ebitda!r}, "
            f"dscr={self.dscr!r}, "
            f"debt_to_ebitda={self.debt_to_ebitda!r}, "
            f"last_modified={self.last_modified!r})"
        )
