from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.deps.auth import get_current_user 
from app.models.user import User
from app.schemas.todo import TodoCreate
from app.services.todo_service import todo_service

router = APIRouter(prefix="/todos", tags=["todos"])

# 각 user todo list 조회 (삭제한 항목 제외 모든 리스트 조회)
@router.get("") 
async def list_todos(
    db: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return await todo_service.list_todos(db, me.id)

# todo list 생성(body에 content, scheduled_for, due_at, category, diffculty, reward_rp, due_at 포함)
@router.post("") 
async def create_todo(
  body: TodoCreate,
  db: AsyncSession = Depends(get_db),
  me: User = Depends(get_current_user),
):
  return await todo_service.create_todo(db, me.id, body)





