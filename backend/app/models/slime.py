from sqlalchemy import BigInteger, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Slime(Base):
    __tablename__ = "slimes"
    __table_args__ = (
        Index("ix_slimes_rarity", "rarity"),
        Index("ix_slimes_element", "element"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    rarity: Mapped[str] = mapped_column(String(20), nullable=False)
    element: Mapped[str | None] = mapped_column(String(50), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    base_hatch_days: Mapped[int] = mapped_column(Integer, nullable=False)
