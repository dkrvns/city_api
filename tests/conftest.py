import datetime
import os
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any
from unittest.mock import AsyncMock

import jwt
import pytest
from dishka import AnyOf, AsyncContainer, Provider, Scope, make_async_container, provide
from dishka.integrations import fastapi as fastapi_integration
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from city_api.config import AuthSettings, Config, PostgresConfig
from city_api.infrastructure.db.models import BaseModel
from city_api.ioc import AppProvider
from city_api.presentation.api.city import city_router
from city_api.presentation.api.district import district_router
from city_api.presentation.api.region import region_router
from city_api.presentation.auth.asgi_middleware import ASGIAuthMiddleware

pytestmark = pytest.mark.asyncio

load_dotenv()


@pytest.fixture(scope='session')
def postgres_config() -> PostgresConfig:
    return PostgresConfig(
        POSTGRES_USER=os.getenv('POSTGRES_USER'),
        POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD'),
        POSTGRES_HOST=os.getenv('POSTGRES_HOST'),
        POSTGRES_PORT=int(os.getenv('TEST_PORT')),
        POSTGRES_DB=os.getenv('TEST_DB'),
    )


@pytest.fixture(scope='session')
async def session_maker(
    postgres_config: PostgresConfig,
) -> async_sessionmaker[AsyncSession]:
    database_uri = f'postgresql+psycopg://{postgres_config.user}:{postgres_config.password}@{postgres_config.host}:{postgres_config.port}/{postgres_config.database}'
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


@pytest.fixture(scope='session')
def jwt_config() -> AuthSettings:
    return AuthSettings(
        JWT_SECRET=os.getenv('JWT_SECRET'),
        JWT_ALGORITHM=os.getenv('JWT_ALGORITHM'),
        SESSION_TTL_MIN=int(os.getenv('SESSION_TTL_MIN')),
        SESSION_REFRESH_EXPIRES=int(os.getenv('SESSION_REFRESH_EXPIRES')),
    )


@pytest.fixture
def valid_access_token(jwt_config: AuthSettings):
    payload = {
        'sub': 'test_user',
        'exp': datetime.datetime.now() + datetime.timedelta(minutes=15),
    }
    token = jwt.encode(
        payload, jwt_config.jwt_secret, algorithm=jwt_config.jwt_algorithm
    )
    return token


@pytest.fixture
async def http_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()

    app.add_middleware(ASGIAuthMiddleware)
    app.include_router(district_router)
    app.include_router(region_router)
    app.include_router(city_router)

    fastapi_integration.setup_dishka(container, app)
    return app


@pytest.fixture
async def http_client(
    http_app: FastAPI, valid_access_token: str
) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_app),
        base_url='http://test',
        cookies={'access_token': valid_access_token},
    ) as client:
        yield client
