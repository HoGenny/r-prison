from datetime import datetime, timedelta, timezone

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.errors import AppError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_token,
)
from app.models.session import UserSession
from app.models.user import User
from app.schemas.auth import KakaoLoginResponse, TokenPair
from app.services.kakao_service import kakao_service


class AuthService:
    # ── 카카오 로그인 ──

    async def kakao_login(
        self,
        db: AsyncSession,
        *,
        kakao_access_token: str,
        device_id: str,
        user_agent: str | None,
    ) -> KakaoLoginResponse:
        """
        카카오 소셜 로그인 처리.

        1) RN에서 받은 카카오 access_token으로 kakao_id 조회
        2) kakao_id로 기존 유저 검색 → 없으면 신규 생성 (nickname=NULL)
        3) 같은 device_id의 기존 세션을 revoke
        4) 자체 JWT(access + refresh) 발급 + DB 세션 생성

        Returns:
            KakaoLoginResponse: 토큰 쌍 + is_new (닉네임 설정 필요 여부)
        """
        # 1) RN에서 받은 카카오 access_token → 사용자 정보 조회
        kakao_user = await kakao_service.get_kakao_user(kakao_access_token)
        kakao_id: int = kakao_user["kakao_id"]

        # 2) 기존 유저 조회
        result = await db.execute(select(User).where(User.kakao_id == kakao_id))
        user = result.scalar_one_or_none()

        is_new = False
        if user is None:
            user = User(kakao_id=kakao_id)
            db.add(user)
            await db.flush()
            is_new = True

        # 3) 같은 device 기존 세션 revoke
        await self._revoke_device_sessions(db, user_id=user.id, device_id=device_id)

        # 4) 자체 JWT 발급 + 세션 생성
        tokens = self._issue_tokens(user)
        self._create_session(
            db,
            user_id=user.id,
            refresh_token=tokens.refresh_token,
            device_id=device_id,
            user_agent=user_agent,
        )

        await db.commit()
        await db.refresh(user)

        return KakaoLoginResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            is_new=is_new,
        )

    # ── 닉네임 설정 (신규 유저) ──

    async def setup_nickname(
        self, db: AsyncSession, *, user: User, nickname: str
    ) -> User:
        """
        신규 유저의 닉네임을 설정한다.

        - 이미 닉네임이 있으면 400 에러 (PATCH /me를 사용해야 함)
        - 닉네임 중복 시 409 에러

        Raises:
            AppError(400): 이미 닉네임이 설정된 유저
            AppError(409): 닉네임 중복
        """
        if user.nickname is not None:
            raise AppError(
                "Nickname already set", status_code=400, code="nickname_already_set"
            )

        exists = await db.execute(select(User.id).where(User.nickname == nickname))
        if exists.scalar_one_or_none() is not None:
            raise AppError(
                "Nickname already taken", status_code=409, code="nickname_duplicate"
            )

        user.nickname = nickname
        await db.commit()
        await db.refresh(user)
        return user

    # ── refresh ──

    async def refresh(
        self,
        db: AsyncSession,
        *,
        refresh_token: str,
        device_id: str,
        user_agent: str | None,
    ) -> TokenPair:
        """
        리프레시 토큰으로 새 토큰 쌍을 발급한다 (토큰 로테이션 방식).

        1) refresh_token JWT 디코딩 → user_id 추출
        2) DB에서 해당 세션 조회 (hash 비교, revoke 여부 확인)
        3) 기존 세션 revoke → 새 세션 + 토큰 생성

        Raises:
            AppError(401): 유효하지 않은 토큰, 세션 없음, 만료
        """
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = int(payload["sub"])

        token_hash = hash_token(refresh_token)
        result = await db.execute(
            select(UserSession).where(
                UserSession.user_id == user_id,
                UserSession.refresh_token_hash == token_hash,
                UserSession.revoked_at.is_(None),
            )
        )
        session = result.scalar_one_or_none()

        if session is None:
            raise AppError(
                "Session not found or already revoked",
                status_code=401,
                code="session_invalid",
            )

        now = datetime.now(timezone.utc)
        if session.expires_at < now:
            raise AppError(
                "Refresh token expired", status_code=401, code="token_expired"
            )

        # 기존 세션 revoke → 새 세션 (토큰 로테이션)
        session.revoked_at = now

        new_tokens = self._issue_tokens_by_id(user_id)
        self._create_session(
            db,
            user_id=user_id,
            refresh_token=new_tokens.refresh_token,
            device_id=device_id,
            user_agent=user_agent,
        )

        await db.commit()
        return new_tokens

    # ── logout ──

    async def logout(
        self, db: AsyncSession, *, user_id: int, refresh_token: str
    ) -> None:
        """
        로그아웃 처리. 해당 refresh_token에 연결된 세션을 revoke한다.
        이미 revoke된 세션이면 아무 일도 일어나지 않음 (멱등).
        """
        token_hash = hash_token(refresh_token)
        now = datetime.now(timezone.utc)

        await db.execute(
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.refresh_token_hash == token_hash,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )
        await db.commit()

    # ── private helpers ──

    def _issue_tokens(self, user: User) -> TokenPair:
        return self._issue_tokens_by_id(user.id)

    def _issue_tokens_by_id(self, user_id: int) -> TokenPair:
        subject = str(user_id)
        return TokenPair(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )

    def _create_session(
        self,
        db: AsyncSession,
        *,
        user_id: int,
        refresh_token: str,
        device_id: str,
        user_agent: str | None,
    ) -> None:
        """DB에 새 세션 레코드를 추가한다. refresh_token은 해시로 저장."""
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        session = UserSession(
            user_id=user_id,
            refresh_token_hash=hash_token(refresh_token),
            device_id=device_id,
            user_agent=user_agent,
            expires_at=expires_at,
        )
        db.add(session)

    async def _revoke_device_sessions(
        self, db: AsyncSession, *, user_id: int, device_id: str
    ) -> None:
        """같은 유저 + 같은 device_id의 활성 세션을 모두 revoke한다."""
        now = datetime.now(timezone.utc)
        await db.execute(
            update(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.device_id == device_id,
                UserSession.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )


auth_service = AuthService()
