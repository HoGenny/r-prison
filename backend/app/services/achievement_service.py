from sqlalchemy.ext.asyncio import AsyncSession


class AchievementService:
    async def list_achievements(self, db: AsyncSession) -> list[object]:
        _ = db
        return []


achievement_service = AchievementService()
