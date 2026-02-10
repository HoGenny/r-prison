from sqlalchemy.ext.asyncio import AsyncSession


class RPService:
    async def add_rp(self, db: AsyncSession, user_id: int, delta: int, ref_type: str) -> None:
        _ = db
        _ = user_id
        _ = delta
        _ = ref_type
        raise NotImplementedError("RPService.add_rp is not implemented yet")


rp_service = RPService()
