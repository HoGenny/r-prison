from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from app.schemas.todo import TodoRead


class DailyCalendarSummary(BaseModel):
    date: date
    todos_completed: int
    rp_earned: int
    streak_day: int


class CalendarDayResponse(BaseModel):
    summary: DailyCalendarSummary
    note: str | None = None
    todos: list[TodoRead]


class CalendarNoteUpdate(BaseModel):
    note: str | None = None
