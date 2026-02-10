from pydantic import BaseModel, ConfigDict

from app.models.base import SlimeRarity


class SlimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    rarity: SlimeRarity
    element: str | None = None
    description: str | None = None
    base_hatch_days: int
