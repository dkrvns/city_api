import datetime
from collections.abc import AsyncIterator

import jwt
import pytest
from dishka import AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from city_api.config import AuthSettings
from city_api.presentation.api.auth.change_password import change_password_router
from city_api.presentation.api.auth.log_in import log_in_router
from city_api.presentation.api.auth.log_out import log_out_router
from city_api.presentation.api.auth.sign_up import sign_up_router
from city_api.presentation.auth.asgi_middleware import ASGIAuthMiddleware
from tests.auth.http.endpoint import test_router


@pytest.fixture
async def http_auth_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.add_middleware(ASGIAuthMiddleware)

    app.include_router(sign_up_router)
    app.include_router(log_in_router)
    app.include_router(log_out_router)
    app.include_router(change_password_router)
    app.include_router(test_router)

    fastapi_integration.setup_dishka(container, app)
    return app


@pytest.fixture
def valid_access_token(jwt_config: AuthSettings):
    payload = {
        'sub': 'test_user',
        'exp': (datetime.datetime.now() + datetime.timedelta(minutes=5)).timestamp(),
    }
    token = jwt.encode(
        payload, jwt_config.jwt_secret, algorithm=jwt_config.jwt_algorithm
    )
    return token


@pytest.fixture
def invalid_access_token(jwt_config: AuthSettings):
    payload = {
        'sub': 'test_user',
        'exp': (datetime.datetime.now() - datetime.timedelta(seconds=1)).timestamp(),
    }
    token = jwt.encode(
        payload, jwt_config.jwt_secret, algorithm=jwt_config.jwt_algorithm
    )
    return token


@pytest.fixture
async def clean_http_client(
    http_auth_app: FastAPI, valid_access_token: str
) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_auth_app),
        base_url='http://test',
    ) as client:
        yield client
