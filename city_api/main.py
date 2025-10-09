import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from city_api.config import Config
from city_api.di.main import ioc_factory
from city_api.presentation.api.auth.change_password import change_password_router
from city_api.presentation.api.auth.log_in import log_in_router
from city_api.presentation.api.auth.log_out import log_out_router
from city_api.presentation.api.auth.sign_up import sign_up_router
from city_api.presentation.api.city import city_router
from city_api.presentation.api.district import district_router
from city_api.presentation.api.region import region_router
from city_api.presentation.auth.asgi_middleware import ASGIAuthMiddleware


def get_fastapi_app() -> FastAPI:
    config = Config()
    app = FastAPI()

    app.include_router(log_in_router)
    app.include_router(sign_up_router)
    app.include_router(log_out_router)
    app.include_router(change_password_router)
    app.include_router(region_router)
    app.include_router(district_router)
    app.include_router(city_router)
    app.add_middleware(ASGIAuthMiddleware)

    async_container = make_async_container(
        *ioc_factory(), FastapiProvider(), context={Config: config}
    )
    setup_dishka(container=async_container, app=app)

    return app


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host='127.0.0.1',
        port=8000,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_http_app():
    app = get_fastapi_app()
    await run_api(app)


async def main() -> None:
    await run_http_app()
