import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import settings
from app.core.errors import AppError


ALGORITHM = "HS256"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_access_token(subject: str) -> str:
    """
    자체 access_token(JWT) 생성.
    - subject: 유저 ID (문자열)
    - 만료: settings.access_token_expire_minutes (기본 60분)
    """
    expires_at = _utc_now() + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "type": "access", "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def create_refresh_token(subject: str) -> str:
    """
    자체 refresh_token(JWT) 생성.
    - subject: 유저 ID (문자열)
    - 만료: settings.refresh_token_expire_days (기본 30일)
    """
    expires_at = _utc_now() + timedelta(days=settings.refresh_token_expire_days)
    payload: dict[str, Any] = {"sub": subject, "type": "refresh", "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_token(token: str, *, expected_type: str | None = None) -> dict[str, Any]:
    """
    JWT 디코딩 및 검증.

    Args:
        token: JWT 문자열
        expected_type: "access" 또는 "refresh" — 지정 시 토큰 타입 불일치하면 에러

    Returns:
        디코딩된 payload dict

    Raises:
        AppError(401): 만료, 유효하지 않은 토큰, sub 누락, 타입 불일치
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError as exc:
        raise AppError(
            "Token has expired", status_code=401, code="token_expired"
        ) from exc
    except jwt.PyJWTError as exc:
        raise AppError("Invalid token", status_code=401, code="invalid_token") from exc

    if "sub" not in payload:
        raise AppError(
            "Token subject is missing", status_code=401, code="invalid_token"
        )

    if expected_type and payload.get("type") != expected_type:
        raise AppError(
            f"Expected {expected_type} token",
            status_code=401,
            code="invalid_token_type",
        )

    return payload
