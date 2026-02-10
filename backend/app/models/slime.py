from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, Integer, String, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, SlimeRarity, slime_rarity_enum


class Slime(Base):
    __tablename__ = "slimes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    rarity: Mapped[SlimeRarity] = mapped_column(slime_rarity_enum(), nullable=False)
    element: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_hatch_days: Mapped[int] = mapped_column(Integer, nullable=False)


class UserSlime(Base):
    __tablename__ = "user_slimes"
    __table_args__ = (
        Index("ix_user_slimes_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    slime_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("slimes.id", ondelete="CASCADE"),
        nullable=False,
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    exp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    affection: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    obtained_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    hatched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))


class UserSlimeShard(Base):
    __tablename__ = "user_slime_shards"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    slime_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("slimes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    qty: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
