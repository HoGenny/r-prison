from sqlalchemy import BigInteger, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    rp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    rp_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    ticket_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    premium_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
