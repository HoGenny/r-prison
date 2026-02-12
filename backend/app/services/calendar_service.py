from datetime import date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo
from app.models.stats import DailyStat

class CalendarService:
    @staticmethod
    async def get_day(session: AsyncSession, *, user_id: int, day: date):
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



calendar_service = CalendarService()
