from sqlalchemy.ext.asyncio import AsyncSession


class IncubationService:
    async def list_incubations(self, db: AsyncSession, user_id: int) -> list[object]:
        _ = db
        _ = user_id
        return []


incubation_service = IncubationService()
