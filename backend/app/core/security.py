from datetime import datetime, timedelta, timezone
import hashlib
import secrets

from app.core.config import settings


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_refresh_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def access_token_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)


def refresh_token_expires_at() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
