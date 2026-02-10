from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.user import UserMeResponse
from app.services.auth_service import auth_service


router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def read_me(db: AsyncSession = Depends(get_db)) -> UserMeResponse:
    user = await auth_service.get_or_create_demo_user(db)
    return UserMeResponse.model_validate(user)
