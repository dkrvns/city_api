import os
from collections.abc import AsyncGenerator
from typing import Any
from unittest.mock import AsyncMock

import pytest
from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container, provide
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import Config, PostgresConfig
from app.infrastructure.db.models import BaseModel
from app.ioc import AppProvider

pytestmark = pytest.mark.asyncio

load_dotenv()

@pytest.fixture(scope="session")
def postgres_config() -> PostgresConfig:
    return PostgresConfig(
        POSTGRES_USER=os.getenv("POSTGRES_USER"),
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD"),
        POSTGRES_HOST=os.getenv("POSTGRES_HOST"),
        POSTGRES_PORT=int(os.getenv("TEST_PORT")),
        POSTGRES_DB=os.getenv("TEST_DB"),
    )


@pytest.fixture(scope="session")
async def session_maker(
    postgres_config: PostgresConfig,
) -> async_sessionmaker[AsyncSession]:
    database_uri = (
        f"postgresql+psycopg://{postgres_config.user}:{postgres_config.password}@{postgres_config.host}:{postgres_config.port}/{postgres_config.database}"
    )
    engine = create_async_engine(database_uri)

    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

    return async_sessionmaker(
        bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )


@pytest.fixture
async def session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as session:
        session.commit = AsyncMock()
        yield session
        await session.rollback()


@pytest.fixture
def mock_provider(session: AsyncSession) -> Provider:
    class MockProvider(AppProvider):
        @provide(scope=Scope.REQUEST)
        async def get_session(
            self, session_maker: async_sessionmaker[AsyncSession]
        ) -> AnyOf[AsyncSession]:
            return session


    return MockProvider()


@pytest.fixture
def test_config(postgres_config: PostgresConfig) -> Config:
    return Config(postgres=postgres_config)


@pytest.fixture
def container(mock_provider: Provider, test_config) -> AsyncContainer:
    return make_async_container(mock_provider, context={Config: test_config})
