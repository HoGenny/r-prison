from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.errors import AppError
from app.core.security import decode_token
from app.models.user import User


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    """
    Authorization 헤더에서 현재 로그인 유저를 추출한다.

    헤더 형식: "Bearer {access_token}"

    Raises:
        AppError(401): 헤더 누락, 형식 오류, 토큰 무효, 유저 미존재
    """
    if not authorization:
        raise AppError("Authentication required", status_code=401, code="unauthorized")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AppError(
            "Invalid authorization header", status_code=401, code="unauthorized"
        )

    payload = decode_token(token, expected_type="access")
    sub = payload.get("sub")

    if not isinstance(sub, str) or not sub.isdigit():
        raise AppError("Invalid token subject", status_code=401, code="invalid_token")

    result = await db.execute(select(User).where(User.id == int(sub)))
    user = result.scalar_one_or_none()

    if user is None:
        raise AppError("User not found", status_code=401, code="user_not_found")

    return user
