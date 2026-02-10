from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserMeResponse


router = APIRouter()


@router.get("/me", response_model=UserMeResponse)
async def me(db: AsyncSession = Depends(get_db)) -> UserMeResponse:
    result = await db.execute(select(User).order_by(User.id).limit(1))
    user = result.scalar_one_or_none()

    if user is None:
        user = User(nickname="demo-user")
        db.add(user)
        await db.commit()
        await db.refresh(user)

    return UserMeResponse.model_validate(user)
