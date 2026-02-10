from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.gacha import GachaBox


class GachaService:
    async def list_active_boxes(self, db: AsyncSession) -> list[GachaBox]:
        result = await db.execute(
            select(GachaBox)
            .where(GachaBox.is_active.is_(True))
            .order_by(GachaBox.id.asc())
        )
        return list(result.scalars().all())


gacha_service = GachaService()
