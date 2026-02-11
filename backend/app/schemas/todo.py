from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


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

    
class TodoCreate(BaseModel):
    content: str = Field(min_length=1, max_length=255)
    description: str | None = None
    scheduled_for: date
    due_at: datetime | None = None
    difficulty: int | None = Field(default=None, ge=1, le=5)
    category: str | None = Field(default=None, max_length=50)
    reward_rp: int | None = Field(default=None, ge=0)
