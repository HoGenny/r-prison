from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.base import ItemType


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    type: ItemType
    description: str | None = None
    created_at: datetime
