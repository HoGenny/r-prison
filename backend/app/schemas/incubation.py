from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.base import IncubationStatus, SlimeRarity


class IncubationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    target_slime_id: int
    rarity: SlimeRarity
    started_at: datetime
    ends_at: datetime
    opened_at: datetime | None = None
    status: IncubationStatus
