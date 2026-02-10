from sqlalchemy.ext.asyncio import AsyncSession


class TodoService:
    async def list_todos(self, db: AsyncSession, user_id: int) -> list[object]:
        _ = db
        _ = user_id
        return []


todo_service = TodoService()
