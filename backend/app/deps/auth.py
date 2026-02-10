from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.errors import AppError
from app.models.user import User


async def get_current_user_demo(db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).order_by(User.id).limit(1))
    user = result.scalar_one_or_none()
    if user is None:
        raise AppError(status_code=401, code="unauthorized", detail="No demo user available")
    return user
