from sqlalchemy.ext.asyncio import AsyncSession


class ItemService:
    async def list_items(self, db: AsyncSession) -> list[object]:
        _ = db
        return []


item_service = ItemService()
