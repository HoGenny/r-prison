from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.errors import AppError
from app.schemas.slime import SlimeDetailData, SlimeDetailResponse, SlimeListData, SlimeListResponse, SlimeRead
from app.services.slime_service import slime_service


router = APIRouter(prefix="/slimes", tags=["slimes"])


@router.get("", response_model=SlimeListResponse)
async def list_slimes(
    rarity: str | None = Query(default=None),
    element: str | None = Query(default=None),
    db: AsyncSession = Depends(get_db),
) -> SlimeListResponse:
    slimes = await slime_service.list_slimes(db=db, rarity=rarity, element=element)
    items = [SlimeRead.model_validate(slime) for slime in slimes]
    return SlimeListResponse(data=SlimeListData(items=items))


@router.get("/{slimeId}", response_model=SlimeDetailResponse)
async def get_slime(slimeId: int, db: AsyncSession = Depends(get_db)) -> SlimeDetailResponse:
    slime = await slime_service.get_slime(db=db, slime_id=slimeId)
    if slime is None:
        raise AppError("Slime not found", status_code=404, code="not_found")

    return SlimeDetailResponse(data=SlimeDetailData(item=SlimeRead.model_validate(slime)))
