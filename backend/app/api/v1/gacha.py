from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.gacha import GachaBoxesResponse, GachaBoxRead
from app.services.gacha_service import gacha_service

router = APIRouter(prefix="/gacha", tags=["gacha"])


@router.get("/boxes", response_model=GachaBoxesResponse)
async def list_gacha_boxes(db: AsyncSession = Depends(get_db)) -> GachaBoxesResponse:
    boxes = await gacha_service.list_active_boxes(db)
    if not boxes:
        return GachaBoxesResponse(
            boxes=[],
            seed_guide="No active boxes found. Seed `gacha_boxes` and `gacha_box_rates` first.",
        )

    return GachaBoxesResponse(
        boxes=[GachaBoxRead.model_validate(box) for box in boxes],
    )
