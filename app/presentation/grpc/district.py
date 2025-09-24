import uuid

import grpc
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty
from grpc.aio import ServicerContext

from app.application.dto.district import NewDistrictDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.district import (
    CreateDistrictInteractor,
    DeleteDistrictInteractor,
    GetDistrictByIdInteractor,
    GetDistrictsByRegionIdInteractor,
    GetDistrictsInteractor,
)
from app.infrastructure.grpc.district import district_pb2
from app.infrastructure.grpc.district.district_pb2_grpc import DistrictServiceServicer


class DistrictGRPCService(DistrictServiceServicer):
    @inject
    async def GetDistricts(
        self,
        request: Empty,
        context: ServicerContext,
        interactor: FromDishka[GetDistrictsInteractor],
    ) -> district_pb2.DistrictList:
        district_dms = await interactor()
        districts = [
            district_pb2.District(
                id=str(district_dm.id),
                region_id=str(district_dm.region_id),
                name=district_dm.name,
            )
            for district_dm in district_dms
        ]
        return district_pb2.DistrictList(districts=districts)

    @inject
    async def GetDistrictsByRegionId(
        self,
        request: district_pb2.RegionIdRequest,
        context: ServicerContext,
        interactor: FromDishka[GetDistrictsByRegionIdInteractor],
    ) -> district_pb2.DistrictList:
        district_dms = await interactor(region_id=uuid.UUID(request.region_id))
        districts = [
            district_pb2.District(
                id=str(district_dm.id),
                region_id=str(district_dm.region_id),
                name=district_dm.name,
            )
            for district_dm in district_dms
        ]
        return district_pb2.DistrictList(districts=districts)

    @inject
    async def GetDistrictById(
        self,
        request: district_pb2.DistrictIdRequest,
        context: ServicerContext,
        interactor: FromDishka[GetDistrictByIdInteractor],
    ) -> district_pb2.District:
        district_dm = await interactor(district_id=uuid.UUID(request.district_id))
        if not district_dm:
            await context.abort(grpc.StatusCode.NOT_FOUND, 'District not found')

        return district_pb2.District(
            id=str(district_dm.id),
            region_id=str(district_dm.region_id),
            name=district_dm.name,
        )

    @inject
    async def CreateDistrict(
        self,
        request: district_pb2.NewDistrictDTO,
        context: ServicerContext,
        interactor: FromDishka[CreateDistrictInteractor],
    ) -> district_pb2.DistrictIdResponse | None:
        try:
            district_uuid = await interactor(
                NewDistrictDTO(uuid.UUID(request.region_id), request.name)
            )

            return district_pb2.DistrictIdResponse(
                district_id=str(district_uuid),
            )
        except EntityNotExistsError:
            await context.abort(
                grpc.StatusCode.NOT_FOUND,
                'Region not found. Please check if this region exists or create it',
            )

    @inject
    async def DeleteDistrict(
        self,
        request: district_pb2.DistrictIdRequest,
        context: ServicerContext,
        interactor: FromDishka[DeleteDistrictInteractor],
    ) -> Empty:
        await interactor(district_id=uuid.UUID(request.district_id))
        return Empty()
