from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class GachaBox(Base):
    __tablename__ = "gacha_boxes"
    __table_args__ = (UniqueConstraint("code", name="uq_gacha_boxes_code"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price_rp: Mapped[int] = mapped_column(Integer, nullable=False)
    min_rarity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class GachaBoxRate(Base):
    __tablename__ = "gacha_box_rates"
    __table_args__ = (UniqueConstraint("box_id", "rarity", name="uq_gacha_box_rates_box_rarity"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    box_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("gacha_boxes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rarity: Mapped[str] = mapped_column(String(20), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
