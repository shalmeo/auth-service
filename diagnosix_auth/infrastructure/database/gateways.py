from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from diagnosix_auth.infrastructure.database.models import User


class UserGateway:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self._session.scalar(select(User).where(User.email == email))
        return user

    async def create_user(self, user: User) -> None:
        self._session.add(user)
        await self._session.flush()
