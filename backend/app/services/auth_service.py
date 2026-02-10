from app.core.security import (
    access_token_expires_at,
    generate_refresh_token,
    hash_refresh_token,
    refresh_token_expires_at,
)
from app.schemas.auth import TokenPair


class AuthService:
    def issue_demo_tokens(self) -> TokenPair:
        refresh = generate_refresh_token()
        access = hash_refresh_token(refresh)
        return TokenPair(
            access_token=access,
            refresh_token=refresh,
            access_token_expires_at=access_token_expires_at(),
            refresh_token_expires_at=refresh_token_expires_at(),
        )
