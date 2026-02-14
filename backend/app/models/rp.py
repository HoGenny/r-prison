from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# rp_transactions 테이블

# 목적:
# - RP(Reward Point) 증감 내역을 "원장(ledger)"처럼 기록한다.
# - 유저의 현재 RP(users.rp)는 별도 누적값으로 존재할 수 있지만,
#   이 테이블은 "왜/어떤 근거로 RP가 변했는지"를 추적/감사(audit)하기 위한 로그다.

# 공통 규칙(팀 전체):
# - RP 증감은 무조건 RpService.apply_rp_delta() 로만 처리한다. (직접 update 금지)
# - 트랜잭션이 필요한 작업(예: 투두 complete)은 async with session.begin(): 으로 묶는다.

# 인덱스:
# - ix_rp_transactions_user_id_created_at (user_id, created_at)
#   -> 유저별 RP 이력 조회(최신순/기간 필터) 최적화

# 속성:
#  - 식별/소유: id(PK), user_id(FK)
#  - 변화량: delta (양수=지급, 음수=회수)
#  - 사유: reason (사람이 읽는 설명/메모. 로직 판단 금지)
#  - 참조(근거): ref_type(어떤 이벤트/도메인인지), ref_id(해당 도메인 id)
#  - 생성시각: created_at (서버 기본값 now)

# ref_type 문자열 규칙(고정):
# - 서비스 레벨에서 허용값을 관리한다(실수 방지).
# - 아래 상수들을 "권장"으로 사용한다.

# B 담당(투두 기반 루프)에서 주로 쓰는 ref_type:
# - TODO_COMPLETE: 투두 완료 보상 지급
# - TODO_UNCOMPLETE: 투두 완료 취소로 인한 보상 회수

# 기본 조회 패턴:
# - 유저 RP 이력(최신순): WHERE user_id=:userId ORDER BY created_at DESC
# - 기간 조회: WHERE user_id=:userId AND created_at BETWEEN :from AND :to
# - 특정 이벤트 중복 검증(필요 시): WHERE user_id=:userId AND ref_type=:type AND ref_id=:refId

# 운영/정책(권장):
# - delta == 0 인 트랜잭션은 생성하지 않는다(의미 없음).
# - "중복 지급 방지"는 서비스 레벨에서 처리한다.
#   (예: complete가 이미 완료면 409, 미완료면 409)
# - 동일 ref에 대해 여러 번 발생할 수 있는 정책이라면 유니크 제약을 걸지 않는다.
#   반대로, ref 단위로 단 1회만 허용하면 (user_id, ref_type, ref_id) 유니크 제약을 고려.

# 주의:
# - reason은 UI/로그용 텍스트이므로 비즈니스 로직 판단 근거로 쓰지 않는다.
# - ref_type 오타는 운영 장애로 직결되므로 상수 사용을 권장한다.


class RPTransaction(Base):
    __tablename__ = "rp_transactions"
    __table_args__ = (Index("ix_rp_transactions_user_id_created_at", "user_id", "created_at"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    delta: Mapped[int] = mapped_column(BigInteger, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    ref_type: Mapped[str] = mapped_column(String(50), nullable=False)
    ref_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
