from sqlalchemy import BigInteger, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("nickname", name="uq_users_nickname"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    rp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    rp_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    ticket_balance: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("0")
    )
    premium_balance: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default=text("0")
    )
