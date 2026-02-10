from datetime import datetime

from pydantic import BaseModel


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expires_at: datetime
    refresh_token_expires_at: datetime
