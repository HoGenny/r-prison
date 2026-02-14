from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.errors import AppError
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserMeResponse, UserUpdateRequest


router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserMeResponse)
async def read_me(
    current_user: User = Depends(get_current_user),
) -> UserMeResponse:
    """현재 로그인한 유저의 정보를 반환한다."""
    return UserMeResponse.model_validate(current_user)


@router.patch("/me", response_model=UserMeResponse)
async def update_me(
    body: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserMeResponse:
    """
    유저 정보 수정. 현재는 닉네임만 변경 가능.

    - 닉네임 중복 시 409 에러
    - body에 nickname이 없으면 아무것도 변경하지 않음
    """
    if body.nickname is not None:
        exists = await db.execute(
            select(User.id).where(User.nickname == body.nickname, User.id != current_user.id)
        )
        if exists.scalar_one_or_none() is not None:
            raise AppError("Nickname already taken", status_code=409, code="nickname_duplicate")

        current_user.nickname = body.nickname

    try:
        await db.commit()
    except IntegrityError as exc:
        await db.rollback()
        raise AppError("Nickname already taken", status_code=409, code="nickname_duplicate") from exc

    await db.refresh(current_user)
    return UserMeResponse.model_validate(current_user)