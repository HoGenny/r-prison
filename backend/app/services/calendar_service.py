from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.stats import DailyStat
from app.models.todo import Todo


class CalendarService:
    @staticmethod
    async def get_day(
        session: AsyncSession, *, user_id: int, day: date
    ):  # 달력에서 해당 날 todo 및 하루 활동량 가져오기
        todos_q = (
            select(Todo)
            .where(
                Todo.user_id == user_id,
                Todo.deleted_at.is_(None),
                Todo.scheduled_for == day,
            )
            .order_by(Todo.completed_at.is_(None).desc(), Todo.created_at.desc())
        )
        todos_res = await session.execute(todos_q)
        todos = todos_res.scalars().all()

        stat_q = select(DailyStat).where(DailyStat.user_id == user_id, DailyStat.date == day)
        stat_res = await session.execute(stat_q)
        stat = stat_res.scalar_one_or_none()

        if stat:
            summary = {
                "date": day,
                "todos_completed": int(stat.todos_completed or 0),
                "rp_earned": int(stat.rp_earned or 0),
                "streak_day": int(stat.streak_day or 0),
            }
            note = stat.note
        else:
            completed = [t for t in todos if t.completed_at is not None]
            summary = {
                "date": day,
                "todos_completed": len(completed),
                "rp_earned": sum(int(t.reward_rp or 0) for t in completed),
                "streak_day": 0,
            }
            note = None

        return {"summary": summary, "note": note, "todos": todos}

    async def upsert_note(self, session: AsyncSession, user_id: int, day: date, note: str | None):
        async with session.begin():
            stmt = select(DailyStat).where(
                DailyStat.user_id == user_id,
                DailyStat.date == day,
            )
            result = await session.execute(stmt)
            stat = result.scalar_one_or_none()

            if stat is None:
                stat = DailyStat(
                    user_id=user_id,
                    date=day,
                    todos_completed=0,
                    rp_earned=0,
                    streak_day=0,
                    note=note,
                )
                session.add(stat)
                await session.flush()
            else:
                stat.note = note
                await session.flush()

        return {
            "date": stat.date,
            "note": stat.note,
        }

    async def get_summary(self, session: AsyncSession, user_id: int, from_: date, to_: date):
        if from_ > to_:
            from app.core.errors import AppError

            raise AppError("날짜 범위에 문제가 있습니다.", status_code=422, code="invalid_request")

        stmt = (
            select(DailyStat)
            .where(
                DailyStat.user_id == user_id,
                DailyStat.date >= from_,
                DailyStat.date <= to_,
            )
            .order_by(DailyStat.date.asc())
        )

        result = await session.execute(stmt)
        rows = result.scalars().all()

        return [
            {
                "date": r.date,
                "todos_completed": int(r.todos_completed or 0),
                "rp_earned": int(r.rp_earned or 0),
                "streak_day": int(r.streak_day or 0),
            }
            for r in rows
        ]


calendar_service = CalendarService()
