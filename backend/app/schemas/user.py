from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    rp: int
    rp_balance: int
    ticket_balance: int
    premium_balance: int
    created_at: datetime
    updated_at: datetime
