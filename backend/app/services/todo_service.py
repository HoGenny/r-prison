from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.todo import TodoCreate, TodoUpdate
from app.models.todo import Todo
from app.core.errors import AppError

class TodoService:
    async def list_todos(self, session: AsyncSession, user_id: int) -> list[Todo]: # 유저의 todo list 목록 조회
        stmt = (
          select(Todo)
          .where(
            Todo.user_id == user_id,
            Todo.deleted_at.is_(None),
          )
          .order_by(Todo.scheduled_for.asc())
        )

        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def get_todo(self, session: AsyncSession, user_id: int, todo_id: int) -> Todo: # todo 1건 상세 검색
        stmt = (
            select(Todo)
            .where(
                Todo.id == todo_id,
                Todo.user_id == user_id,
                Todo.deleted_at.is_(None),
            )
        )

        result = await session.execute(stmt)
        todo = result.scalar_one_or_none()

        if todo is None :
            raise AppError("Todo not found", status_code=404, code="not found")
        
        return todo
      

    async def create_todo(self, session: AsyncSession, user_id: int, data: TodoCreate) -> Todo: # todo 생성 
        content = data.content.strip()
        if not content:
            raise AppError("content is required", status_code=422, code="invalid_request")

        async with session.begin():
            todo = Todo(
                user_id=user_id,
                content=content,
                description=data.description,
                scheduled_for=data.scheduled_for,
                due_at=data.due_at,
                difficulty=data.difficulty if data.difficulty is not None else 1,
                category=data.category if data.category is not None else "general",
                reward_rp=data.reward_rp if data.reward_rp is not None else 0,
            )

            session.add(todo)
            await session.flush() 

            return todo
    
    async def update_todo(self, session: AsyncSession, user_id: int, todo_id: int, data: TodoUpdate) -> Todo: # todo 수정
        todo = await self.get_todo(session, user_id, todo_id)

        async with session.begin():
            if data.content is not None:
                todo.content = data.content.strip()
            
            if data.description is not None:
                todo.description = data.description

            if data.scheduled_for is not None:
                todo.scheduled_for = data.scheduled_for

            if data.due_at is not None:
                todo.due_at = data.due_at
            
            if data.category is not None:
                todo.category = data.category
            
            await session.flush()
        
        return todo


todo_service = TodoService()
