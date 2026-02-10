from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.auth import TokenPair


class AuthService:
    async def get_or_create_demo_user(self, db: AsyncSession) -> User:
        result = await db.execute(select(User).order_by(User.id).limit(1))
        user = result.scalar_one_or_none()
        if user is not None:
            return user

        user = User(nickname="demo-user")
        db.add(user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            retry = await db.execute(select(User).order_by(User.id).limit(1))
            user = retry.scalar_one_or_none()
            if user is None:
                raise
            return user

        await db.refresh(user)
        return user

    def issue_token_pair(self, user: User) -> TokenPair:
        subject = str(user.id)
        return TokenPair(
            access_token=create_access_token(subject),
            refresh_token=create_refresh_token(subject),
        )


auth_service = AuthService()
