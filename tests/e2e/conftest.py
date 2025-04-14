import os
from datetime import timedelta
from typing import Generator

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from diagnosix_auth.api import handlers
from diagnosix_auth.api.providers import (
    session_provider,
    jwt_token_processor_provider,
    user_gateway_provider,
    user_gateway,
    db_session,
)
from diagnosix_auth.infrastructure.auth import JwtTokenProcessor


@pytest.fixture(scope="session")
def postgres_url() -> Generator[str, None, None]:
    postgres = PostgresContainer("postgres:15-alpine")
    if (
        os.name == "nt"
    ):  # TODO: workaround from testcontainers/testcontainers-python#108
        postgres.get_container_host_ip = lambda: "localhost"
    try:
        postgres.start()
        postgres_url_ = postgres.get_connection_url(driver="psycopg")
        yield postgres_url_
    finally:
        postgres.stop()


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="session", autouse=True)
def upgrade_schema_db(alembic_config: AlembicConfig):
    upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def client(postgres_url):
    app = FastAPI()

    app.dependency_overrides[session_provider] = db_session(postgres_url)
    app.dependency_overrides[user_gateway_provider] = user_gateway
    app.dependency_overrides[jwt_token_processor_provider] = lambda: JwtTokenProcessor(
        "some-secret", timedelta(minutes=5), "HS256"
    )

    app.include_router(handlers.router)

    return TestClient(app)
