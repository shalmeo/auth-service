from typing import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from diagnosix_auth.infrastructure.auth import JwtTokenProcessor
from diagnosix_auth.infrastructure.database.gateways import UserGateway


def session_provider() -> AsyncSession: ...


def db_session(uri: str) -> Callable[[], AsyncSession]:
    engine = create_async_engine(url=uri)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def session_wrapper() -> AsyncSession:
        session: AsyncSession = session_factory()
        try:
            yield session
        finally:
            await session.close()

    return session_wrapper


def user_gateway_provider() -> UserGateway: ...


def user_gateway(session: AsyncSession = Depends(session_provider)) -> UserGateway:
    return UserGateway(session=session)


def jwt_token_processor_provider() -> JwtTokenProcessor: ...
