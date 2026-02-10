from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.base import SlimeRarity


class GachaBoxRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    price_rp: int
    min_rarity: SlimeRarity | None = None
    is_active: bool
    created_at: datetime


class GachaBoxesResponse(BaseModel):
    boxes: list[GachaBoxRead]
    seed_guide: str | None = None
