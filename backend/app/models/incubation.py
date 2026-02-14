from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import (
    Base,
    IncubationStatus,
    SlimeRarity,
    incubation_status_enum,
    slime_rarity_enum,
)


class Incubation(Base):
    __tablename__ = "incubations"
    __table_args__ = (Index("ix_incubations_user_id_status", "user_id", "status"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    target_slime_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("slimes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    rarity: Mapped[SlimeRarity] = mapped_column(slime_rarity_enum(), nullable=False)
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    opened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[IncubationStatus] = mapped_column(
        incubation_status_enum(),
        nullable=False,
        server_default=text("'incubating'"),
    )
