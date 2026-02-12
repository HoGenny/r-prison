from datetime import date

from __future__ import annotations

from typing import Optional
from pydantic import BaseModel
from app.schemas.todo import TodoRead

class DailyCalendarSummary(BaseModel):
    date: date
    todos_completed: int
    rp_earned: int
    streak_day: int

class CalendarDayResponse(BaseModel):
    summary: DailyCalendarSummary
    note: Optional[str] = None
    todos: list[TodoRead]