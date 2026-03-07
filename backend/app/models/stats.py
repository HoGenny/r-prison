from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Integer, Text, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# daily_stats 테이블

# 목적:
# - 유저의 "하루 단위 활동 결과"를 빠르게 조회하기 위한 집계(summary) 테이블.
# - todos, rp_transactions 같은 원본 데이터를 매번 계산하지 않고
#   화면(캘린더/홈)에서 즉시 보여주기 위한 캐시 역할을 한다.

# 단위:
# - user 1명 + 날짜 1일 = 1행
# - 따라서 PK = (user_id, date)

# B 담당(투두 기반 루프)에서 책임지는 핵심 집계 데이터:
# - 투두 완료 수
# - 해당 날짜에 획득한 RP

# 속성:
#  - 식별/소유: user_id, date
#  - 완료 통계: todos_completed
#  - 보상 통계: rp_earned
#  - 연속 기록: streak_day
#  - 메모: note
#  - 수정 시각: updated_at

# 언제 갱신되나?
# - todo complete / uncomplete 시점에 서비스 레벨에서 upsert 한다.

# complete 예:
#   todos_completed += 1
#   rp_earned += reward_rp

# uncomplete 예:
#   todos_completed -= 1
#   rp_earned -= reward_rp

# 기본 조회 패턴:
# - 특정 날짜:
#   WHERE user_id=:userId AND date=:date

# - 기간 조회(캘린더 범위):
#   WHERE user_id=:userId AND date BETWEEN :from AND :to

# 운영/정책(권장):
# - 집계 테이블이므로, 원본 데이터와 불일치하지 않도록
#   반드시 트랜잭션 안에서 함께 처리한다.

# - 최초 데이터가 없으면 insert,
#   이미 존재하면 update 하는 방식(upsert)을 사용한다.

# 주의:
# - 이 테이블의 값은 "계산 결과"이므로,
#   신뢰 기준(source of truth)은 todos / rp_transactions 이다.
# - 데이터가 이상하면 집계 재계산으로 복구 가능해야 한다.


class DailyStat(Base):
    __tablename__ = "daily_stats"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    date: Mapped[date] = mapped_column(Date, primary_key=True)
    todos_completed: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    rp_earned: Mapped[int] = mapped_column(BigInteger, nullable=False, server_default=text("0"))
    streak_day: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
