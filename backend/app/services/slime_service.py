from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.slime import Slime


class SlimeService:
    async def list_slimes(
        self,
        db: AsyncSession,
        rarity: str | None = None,
        element: str | None = None,
    ) -> list[Slime]:
        stmt: Select[tuple[Slime]] = select(Slime).order_by(Slime.id.asc())
        if rarity is not None:
            stmt = stmt.where(Slime.rarity == rarity)
        if element is not None:
            stmt = stmt.where(Slime.element == element)

        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_slime(self, db: AsyncSession, slime_id: int) -> Slime | None:
        result = await db.execute(select(Slime).where(Slime.id == slime_id))
        return result.scalar_one_or_none()


slime_service = SlimeService()
