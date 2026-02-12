from fastapi import APIRouter

from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.db import get_db
from app.deps.auth import get_current_user 

from app.schemas.todo import TodoRead
from app.schemas.calendar import CalendarDayResponse
from app.services.calendar_service import CalendarService


router = APIRouter(prefix="/calendar", tags=["calendar"])

@router.get("/day/{date}", response_model=CalendarDayResponse)
async def get_calendar_day(
    day: date,
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    data = await CalendarService.get_day(session, user_id=me.id, day=day)
    data["todos"] = [TodoRead.model_validate(t) for t in data["todos"]]
    return data