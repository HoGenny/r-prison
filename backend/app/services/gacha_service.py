from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.gacha import GachaBox, GachaBoxRate


class GachaService:
    async def list_active_boxes(self, db: AsyncSession) -> list[GachaBox]:
        result = await db.execute(
            select(GachaBox)
            .where(GachaBox.is_active.is_(True))
            .order_by(GachaBox.id.asc())
        )
        return list(result.scalars().all())

    async def get_box_rates(self, db: AsyncSession, box_id: int) -> list[GachaBoxRate]:
        box_result = await db.execute(select(GachaBox.id).where(GachaBox.id == box_id))
        if box_result.scalar_one_or_none() is None:
            raise AppError("Gacha box not found", status_code=404, code="not_found")

        rate_result = await db.execute(
            select(GachaBoxRate)
            .where(GachaBoxRate.box_id == box_id)
            .order_by(GachaBoxRate.id.asc())
        )
        return list(rate_result.scalars().all())


gacha_service = GachaService()
