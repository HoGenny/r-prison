from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import Todo

class TodoService:
    async def list_todos(self, db: AsyncSession, user_id: int) -> list[object]: # 유저의 todo list 목록 조회
        stmt = (
          select(Todo)
          .where(
            Todo.user_id == user_id,
            Todo.deleted_at.is_(None),
          )
          .order_by(Todo.scheduled_for.asc())
        )

        result = await db.execute(stmt)
        return list(result.scalars().all())

    


todo_service = TodoService()
