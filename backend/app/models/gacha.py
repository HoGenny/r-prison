from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, SlimeRarity, slime_rarity_enum


class GachaBox(Base):
    __tablename__ = "gacha_boxes"
    __table_args__ = (UniqueConstraint("code", name="uq_gacha_boxes_code"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    price_rp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    min_rarity: Mapped[SlimeRarity | None] = mapped_column(slime_rarity_enum(), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class GachaBoxRate(Base):
    __tablename__ = "gacha_box_rates"
    __table_args__ = (
        UniqueConstraint("box_id", "rarity", name="uq_gacha_box_rates_box_rarity"),
        Index("ix_gacha_box_rates_box_id", "box_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    box_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("gacha_boxes.id", ondelete="CASCADE"),
        nullable=False,
    )
    rarity: Mapped[SlimeRarity] = mapped_column(slime_rarity_enum(), nullable=False)
    weight: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class GachaDraw(Base):
    __tablename__ = "gacha_draws"
    __table_args__ = (
        Index("ix_gacha_draws_user_id_created_at", "user_id", "created_at"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    box_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("gacha_boxes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    result_rarity: Mapped[SlimeRarity] = mapped_column(slime_rarity_enum(), nullable=False)
    result_slime_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("slimes.id", ondelete="RESTRICT"),
        nullable=False,
    )
    spent_rp: Mapped[int] = mapped_column(BigInteger, nullable=False)
    incubation_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("incubations.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class GachaPityState(Base):
    __tablename__ = "gacha_pity_state"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    box_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("gacha_boxes.id", ondelete="CASCADE"),
        primary_key=True,
    )
    since_last_epic: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    since_last_legendary: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
