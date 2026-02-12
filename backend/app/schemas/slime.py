from pydantic import BaseModel, ConfigDict


class SlimeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    rarity: str
    element: str | None = None
    description: str | None = None
    base_hatch_days: int


class SlimeListData(BaseModel):
    items: list[SlimeRead]


class SlimeDetailData(BaseModel):
    item: SlimeRead


class SlimeListResponse(BaseModel):
    ok: bool = True
    data: SlimeListData


class SlimeDetailResponse(BaseModel):
    ok: bool = True
    data: SlimeDetailData
