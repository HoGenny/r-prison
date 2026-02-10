from __future__ import annotations

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )


class SlimeRarity(str, enum.Enum):
    common = "common"
    uncommon = "uncommon"
    rare = "rare"
    epic = "epic"
    legendary = "legendary"


class IncubationStatus(str, enum.Enum):
    incubating = "incubating"
    ready = "ready"
    opened = "opened"
    canceled = "canceled"


class ItemType(str, enum.Enum):
    consumable = "consumable"
    cosmetic = "cosmetic"
    material = "material"


def slime_rarity_enum() -> SqlEnum:
    return SqlEnum(SlimeRarity, name="slime_rarity", native_enum=False, validate_strings=True)


def incubation_status_enum() -> SqlEnum:
    return SqlEnum(IncubationStatus, name="incubation_status", native_enum=False, validate_strings=True)


def item_type_enum() -> SqlEnum:
    return SqlEnum(ItemType, name="item_type", native_enum=False, validate_strings=True)
