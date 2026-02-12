from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.gacha import (
    GachaBoxListData,
    GachaBoxListResponse,
    GachaBoxRatesData,
    GachaBoxRatesResponse,
    GachaBoxRead,
    GachaRateRead,
)
from app.services.gacha_service import gacha_service


router = APIRouter(prefix="/gacha", tags=["gacha"])


@router.get("/boxes", response_model=GachaBoxListResponse)
async def list_gacha_boxes(db: AsyncSession = Depends(get_db)) -> GachaBoxListResponse:
    boxes = await gacha_service.list_active_boxes(db)
    items = [GachaBoxRead.model_validate(box) for box in boxes]
    return GachaBoxListResponse(data=GachaBoxListData(items=items))


@router.get("/boxes/{boxId}/rates", response_model=GachaBoxRatesResponse)
async def list_gacha_box_rates(boxId: int, db: AsyncSession = Depends(get_db)) -> GachaBoxRatesResponse:
    rates = await gacha_service.get_box_rates(db=db, box_id=boxId)
    data = GachaBoxRatesData(
        box_id=boxId,
        rates=[GachaRateRead(rarity=rate.rarity, weight=rate.weight) for rate in rates],
    )
    return GachaBoxRatesResponse(data=data)
