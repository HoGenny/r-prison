from datetime import date

from pydantic import BaseModel


class DailyCalendarSummary(BaseModel):
    date: date
    todos_completed: int
    rp_earned: int
    streak_day: int
