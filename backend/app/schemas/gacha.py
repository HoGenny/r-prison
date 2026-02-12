from pydantic import BaseModel, ConfigDict


class GachaBoxRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    price_rp: int
    min_rarity: str | None = None


class GachaRateRead(BaseModel):
    rarity: str
    weight: int


class GachaBoxListData(BaseModel):
    items: list[GachaBoxRead]


class GachaBoxRatesData(BaseModel):
    box_id: int
    rates: list[GachaRateRead]


class GachaBoxListResponse(BaseModel):
    ok: bool = True
    data: GachaBoxListData


class GachaBoxRatesResponse(BaseModel):
    ok: bool = True
    data: GachaBoxRatesData
