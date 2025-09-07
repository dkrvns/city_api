from concurrent.futures import ThreadPoolExecutor

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider, setup_dishka
from dishka.integrations.grpcio import DishkaAioInterceptor, GrpcioProvider
from fastapi import FastAPI
from grpc.aio import server as make_server

from app.config import Config
from app.infrastructure.grpc.city.city_pb2_grpc import add_CityServiceServicer_to_server
from app.infrastructure.grpc.district.district_pb2_grpc import (
    add_DistrictServiceServicer_to_server,
)
from app.infrastructure.grpc.region.region_pb2_grpc import (
    add_RegionServiceServicer_to_server,
)
from app.ioc import AppProvider
from app.presentation.api.city import city_router
from app.presentation.api.district import district_router
from app.presentation.api.region import region_router
from app.presentation.grpc.city import CityGRPCService
from app.presentation.grpc.district import DistrictGRPCService
from app.presentation.grpc.region import RegionGRPCService


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


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
    )
    server = uvicorn.Server(config)
    await server.serve()


async def run_http_app():
    app = get_fastapi_app()
    await run_api(app)


async def run_grpc_app():
    config = Config()
    container = make_async_container(
        AppProvider(),
        GrpcioProvider(),
        context={Config: config}
    )

    server = make_server(
        ThreadPoolExecutor(max_workers=10),
        interceptors=[DishkaAioInterceptor(container)]
    )

    add_RegionServiceServicer_to_server(RegionGRPCService(), server)
    add_DistrictServiceServicer_to_server(DistrictGRPCService(), server)
    add_CityServiceServicer_to_server(CityGRPCService(), server)

    server.add_insecure_port("[::]:50051")

    await server.start()
    await server.wait_for_termination()


async def main(server_type: str) -> None:
    if server_type == 'HTTP':
        await run_http_app()
    elif server_type == 'GRPC':
        await run_grpc_app()
