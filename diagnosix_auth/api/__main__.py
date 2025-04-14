import asyncio
import logging
import os
from datetime import timedelta

import uvicorn
from fastapi import FastAPI

from diagnosix_auth.api import handlers
from diagnosix_auth.api.providers import (
    session_provider,
    db_session,
    jwt_token_processor_provider,
    user_gateway,
    user_gateway_provider,
)
from diagnosix_auth.infrastructure.auth import JwtTokenProcessor


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] #%(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s",
    )

    app = FastAPI(version="1.0.0")

    app.dependency_overrides[session_provider] = db_session(
        uri=os.getenv("DATABASE_URI")
    )
    app.dependency_overrides[user_gateway_provider] = user_gateway
    app.dependency_overrides[jwt_token_processor_provider] = lambda: JwtTokenProcessor(
        "some-secret", timedelta(minutes=5), "HS256"
    )

    app.include_router(handlers.router)

    server = uvicorn.Server(
        uvicorn.Config(
            app, host="0.0.0.0", port=9898, log_level=logging.INFO, log_config=None
        )
    )
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
