import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from fastapi import FastAPI

from app.config import Config
from app.ioc import AppProvider
from app.presentation.api.city import city_router
from app.presentation.api.district import district_router
from app.presentation.api.region import region_router


def get_fastapi_app() -> FastAPI:
    config = Config()
    app = FastAPI()

    app.include_router(region_router)
    app.include_router(district_router)
    app.include_router(city_router)

    async_container = make_async_container(
        AppProvider(),
        FastapiProvider(),
        context={Config: config}
    )
    setup_dishka(container=async_container, app=app)

    return app


def get_app():
    app = get_fastapi_app()

    return app


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    app = get_app()
    await run_api(app)
