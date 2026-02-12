from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.todo import TodoRead
from app.schemas.calendar import DailyCalendarSummary, CalendarDayResponse, CalendarNoteUpdate
from app.services.calendar_service import calendar_service

router = APIRouter(prefix="/calendar", tags=["calendar"])


# 특정 날짜 캘린더 상세 조회 (todos + daily_stats 요약 + note)
@router.get("/day/{day}")
async def get_calendar_day(
    day: date,
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    data = await calendar_service.get_day(session, me.id, day)
    data["todos"] = [TodoRead.model_validate(t) for t in data["todos"]]

    return data

@router.patch("/day/{day}/note")
async def patch_calendar_note(
    day: date,
    body: CalendarNoteUpdate,
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return await calendar_service.upsert_note(session, me.id, day, body.note)

@router.get("/summary")
async def get_calendar_summary(
    from_: date = Query(..., alias="from"),
    to_: date = Query(..., alias="to"),
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return await calendar_service.get_summary(session, me.id, from_, to_)
