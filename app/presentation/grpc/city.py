import uuid

import grpc
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty
from grpc.aio import ServicerContext

from app.application.dto.city import NewCityDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.city import (
    CreateCityInteractor,
    DeleteCityInteractor,
    GetCitiesByDistrictIdInteractor,
    GetCitiesInteractor,
    GetCityByIdInteractor,
)
from app.infrastructure.grpc.city import city_pb2
from app.infrastructure.grpc.city.city_pb2_grpc import CityServiceServicer


class CityGRPCService(CityServiceServicer):
    @inject
    async def GetCities(
        self,
        request: Empty,
        context: ServicerContext,
        interactor: FromDishka[GetCitiesInteractor]
    ) -> city_pb2.CityList:
        city_dms = await interactor()
        cities = [
            city_pb2.City(
                id=str(city_dm.id),
                district_id=str(city_dm.district_id),
                name=city_dm.name,
                obj_type=city_dm.obj_type,
                population=city_dm.population,
            )
            for city_dm in city_dms
        ]
        return city_pb2.CityList(cities=cities)

    @inject
    async def GetCitiesByDistrictId(
        self,
        request: city_pb2.DistrictIdRequest,
        context: ServicerContext,
        interactor: FromDishka[GetCitiesByDistrictIdInteractor]
    ) -> city_pb2.CityList:
        city_dms = await interactor(district_id=uuid.UUID(request.district_id))
        cities = [
            city_pb2.City(
                id=str(city_dm.id),
                district_id=str(city_dm.district_id),
                name=city_dm.name,
                obj_type=city_dm.obj_type,
                population=city_dm.population,
            )
            for city_dm in city_dms
        ]
        return city_pb2.CityList(cities=cities)

    @inject
    async def GetCityById(
        self,
        request: city_pb2.CityIdRequest,
        context: ServicerContext,
        interactor: FromDishka[GetCityByIdInteractor]
    ) -> city_pb2.City:
        city_dm = await interactor(city_id=uuid.UUID(request.city_id))
        if not city_dm:
            await context.abort(grpc.StatusCode.NOT_FOUND, "City not found")

        return city_pb2.City(
            id=str(city_dm.id),
            district_id=str(city_dm.district_id),
            name=city_dm.name,
            obj_type=city_dm.obj_type,
            population=city_dm.population,
        )

    @inject
    async def CreateCity(
        self,
        request: city_pb2.NewCityDTO,
        context: ServicerContext,
        interactor: FromDishka[CreateCityInteractor]
    ) -> city_pb2.CityIdResponse:
        try:
            city_uuid = await interactor(NewCityDTO(
                district_id=uuid.UUID(request.district_id),
                name=request.name,
                obj_type=request.obj_type,
                population=request.population
            ))

            return city_pb2.CityIdResponse(
                city_id=str(city_uuid),
            )
        except EntityNotExistsError:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                "District not found. Please check if this district exists"
            )

    @inject
    async def DeleteCity(
        self,
        request: city_pb2.CityIdRequest,
        context: ServicerContext,
        interactor: FromDishka[DeleteCityInteractor],
    ) -> Empty:
        await interactor(city_id=uuid.UUID(request.city_id))
        return Empty()
