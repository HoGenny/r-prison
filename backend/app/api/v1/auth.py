from typing import Annotated

from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.schemas.auth import (
    KakaoLoginRequest,
    KakaoLoginResponse,
    RefreshRequest,
    SetupNicknameRequest,
    TokenPair,
)
from app.schemas.common import MessageResponse
from app.schemas.user import UserMeResponse
from app.services.auth_service import auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/kakao", response_model=KakaoLoginResponse)
async def kakao_login(
    body: KakaoLoginRequest,
    db: AsyncSession = Depends(get_db),
    user_agent: Annotated[str | None, Header()] = None,
    x_device_id: Annotated[str, Header()] = "default",
) -> KakaoLoginResponse:
    """
    카카오 소셜 로그인.

    RN 앱에서 카카오 SDK로 발급받은 access_token을 전달하면,
    백엔드가 카카오 API로 유저 정보를 확인하고 자체 JWT를 발급한다.

    - 기존 유저: is_new=False, 바로 서비스 이용 가능
    - 신규 유저: is_new=True, POST /auth/setup-nickname 으로 닉네임 설정 필요
    """
    return await auth_service.kakao_login(
        db,
        kakao_access_token=body.kakao_access_token,
        device_id=x_device_id,
        user_agent=user_agent,
    )


@router.post("/setup-nickname", response_model=UserMeResponse)
async def setup_nickname(
    body: SetupNicknameRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserMeResponse:
    """
    신규 유저 닉네임 설정 (최초 1회).

    - 이미 닉네임이 있으면 400 에러 → PATCH /me 를 사용해야 함
    - 닉네임 중복 시 409 에러
    """
    user = await auth_service.setup_nickname(
        db, user=current_user, nickname=body.nickname
    )
    return UserMeResponse.model_validate(user)


@router.post("/refresh", response_model=TokenPair)
async def refresh(
    body: RefreshRequest,
    db: AsyncSession = Depends(get_db),
    user_agent: Annotated[str | None, Header()] = None,
    x_device_id: Annotated[str, Header()] = "default",
) -> TokenPair:
    """
    리프레시 토큰으로 새 토큰 쌍 발급 (토큰 로테이션).

    기존 refresh_token은 즉시 무효화되고 새 토큰 쌍이 반환된다.
    """
    return await auth_service.refresh(
        db,
        refresh_token=body.refresh_token,
        device_id=x_device_id,
        user_agent=user_agent,
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    body: RefreshRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """
    로그아웃. 전달된 refresh_token에 연결된 세션을 revoke한다.

    - Authorization 헤더(access_token) + body(refresh_token) 모두 필요
    """
    await auth_service.logout(
        db, user_id=current_user.id, refresh_token=body.refresh_token
    )
    return MessageResponse(message="Logged out successfully")
