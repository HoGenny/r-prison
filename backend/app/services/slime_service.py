from sqlalchemy.ext.asyncio import AsyncSession


class SlimeService:
    async def list_slimes(self, db: AsyncSession) -> list[object]:
        _ = db
        return []


slime_service = SlimeService()
