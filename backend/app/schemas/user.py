from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserMeResponse(BaseModel):
    """GET /me, POST /auth/setup-nickname 등에서 반환하는 유저 정보."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str | None
    rp: int             
    rp_balance: int     
    ticket_balance: int
    premium_balance: int
    created_at: datetime
    updated_at: datetime


class UserUpdateRequest(BaseModel):
    """PATCH /me 요청. 변경할 필드만 전달 (현재는 nickname만 지원)."""
    nickname: str | None = Field(default=None, min_length=2, max_length=16)
