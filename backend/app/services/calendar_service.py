from datetime import date

from app.schemas.calendar import DailyCalendarSummary


class CalendarService:
    async def daily_summary(self, user_id: int, target_date: date) -> DailyCalendarSummary:
        _ = user_id
        return DailyCalendarSummary(
            date=target_date,
            todos_completed=0,
            rp_earned=0,
            streak_day=0,
        )


calendar_service = CalendarService()
