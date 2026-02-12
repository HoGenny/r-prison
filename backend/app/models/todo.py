from datetime import date, datetime

from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin

# todos 테이블
# index : ix_todos_user_id_scheduled_for (user_id, scheduled_for) -> 유저의 특정 날짜 투두 조회(캘린더)
# 속성 : 
#  - 식별, 소유 : id(PK), user_id(FK) 
#  - 내용 : content(todo 제목), description(설명)
#  - 날짜, 시간(캘린더) : scheduled_for(해당 날짜), due_at(마감기한)
#  - 완료, 삭제 상태 : completed_at(완료 시간), deleted_at(소프트 삭제 플래그)
#  - 게임용 메타데이터 : difficulty(난이도), category(분류), reward_rp(성공 시 보상 rp)
# 기본 WHERE 절
# - 유저 투두 1건 접근 : WHERE id=:todoId AND user_id=:userId AND deleted_at IS NULL
# - 특정 날짜 투두 목록(캘린더 용) : WHERE user_id=:userId AND scheduled_for=:date AND deleted_at IS NULL
# - 완료 / 미완료 필터 : completed_at IS NOT NULL / completed_at IS NULL
# 공통 규칙 적용 사항
# - complete 요청 시 : 이미 완료(completed_at is not null) -> 409, 아니면 RP지급
# - uncomplete 요청 시 : 이미 미완료(completed_at is null) -> 409, 아니면 comleted_at = null + RP 회수
class Todo(TimestampMixin, Base): 
    __tablename__ = "todos"
    __table_args__ = (
        Index("ix_todos_user_id_scheduled_for", "user_id", "scheduled_for"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True) # 기본키 id
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
