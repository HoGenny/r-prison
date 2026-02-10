from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TodoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    content: str
    description: str | None = None
    scheduled_for: date
    due_at: datetime | None = None
    completed_at: datetime | None = None
    deleted_at: datetime | None = None
    difficulty: int
    category: str
    reward_rp: int
    created_at: datetime
    updated_at: datetime
