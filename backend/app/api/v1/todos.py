from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.deps.auth import get_current_user 
from app.models.user import User
from app.schemas.todo import TodoCreate, TodoUpdate
from app.services.todo_service import todo_service

router = APIRouter(prefix="/todos", tags=["todos"])

# 각 user todo list 조회 (삭제한 항목 제외 모든 리스트 조회)
@router.get("") 
async def list_todos(
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return await todo_service.list_todos(session, me.id)

# todo 1건 상세 조회
@router.get("/{todo_id}")
async def get_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_db),
    me: User = Depends(get_current_user),
):
    return await todo_service.get_todo(session, me.id, todo_id)

# todo list 생성(body에 content, scheduled_for, category, diffculty, reward_rp, due_at 포함)
@router.post("") 
async def create_todo(
  body: TodoCreate,
  session: AsyncSession = Depends(get_db),
  me: User = Depends(get_current_user),
):
	return await todo_service.create_todo(session, me.id, body)

# todo 수정(content, description, scheduled_for, due_at, category만 가능)
@router.patch("/{todo_id}")
async def update_todo(
	todo_id: int,
	body: TodoUpdate,
	session: AsyncSession = Depends(get_db),
	me: User = Depends(get_current_user),
):
	return await todo_service.update_todo(session, me.id, todo_id, body)

@router.delete("/{todo_id}")
async def update_todo(
	todo_id: int,
	session: AsyncSession = Depends(get_db),
	me: User = Depends(get_current_user),
):
	return await todo_service.delete_todo(session, me.id, todo_id)





