from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Todo(TimestampMixin, Base):
    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_user_id_scheduled_for", "user_id", "scheduled_for"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_for: Mapped[date] = mapped_column(Date, nullable=False)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("1"))
    category: Mapped[str] = mapped_column(String(50), nullable=False, server_default=text("'general'"))
    reward_rp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
