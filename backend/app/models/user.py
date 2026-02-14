from sqlalchemy import BigInteger, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

"""
User 모델
- 카카오 소셜 로그인 기반 유저 테이블
- kakao_id: 카카오 API에서 반환하는 고유 회원번호 (Signed int 64)
- nickname: 카카오 로그인 후 별도로 입력받음 (최초 가입 시 NULL)
- rp, rp_balance, ticket_balance, premium_balance: 게임 내 재화
"""
class User(TimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("nickname", name="uq_users_nickname"),
        UniqueConstraint("kakao_id", name="uq_users_kakao_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    kakao_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rp: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    rp_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    ticket_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    premium_balance: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))