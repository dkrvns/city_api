import uuid

import grpc
from dishka import FromDishka
from dishka.integrations.grpcio import inject
from google.protobuf.empty_pb2 import Empty
from grpc.aio import ServicerContext

from app.application.dto.region import NewRegionDTO
from app.application.errors import EntityAlreadyExistsError
from app.application.interactors.region import (
    CreateRegionInteractor,
    DeleteRegionInteractor,
    GetRegionByIdInteractor,
    GetRegionsInteractor,
)
from app.infrastructure.grpc.region import region_pb2
from app.infrastructure.grpc.region.region_pb2_grpc import (
    RegionServiceServicer,
)


class RegionGRPCService(RegionServiceServicer):
    @inject
    async def GetRegions(
        self,
        request: Empty,
        context: ServicerContext,
        interactor: FromDishka[GetRegionsInteractor],
    ) -> region_pb2.RegionList:
        region_dms = await interactor()
        regions = [
            region_pb2.Region(
                id=str(region_dm.id),
                name=region_dm.name,
                capital=region_dm.capital,
            )
            for region_dm in region_dms
        ]
        return region_pb2.RegionList(regions=regions)

    @inject
    async def GetRegionById(
        self,
        request: region_pb2.RegionIdRequest,
        context: ServicerContext,
        interactor: FromDishka[GetRegionByIdInteractor],
    ) -> region_pb2.Region:
        region_dm = await interactor(region_id=uuid.UUID(request.region_id))
        if not region_dm:
            await context.abort(grpc.StatusCode.NOT_FOUND, 'Region not found')

        return region_pb2.Region(
            id=str(region_dm.id),
            name=region_dm.name,
            capital=region_dm.capital,
        )

    @inject
    async def CreateRegion(
        self,
        request: region_pb2.NewRegionDTO,
        context: ServicerContext,
        interactor: FromDishka[CreateRegionInteractor],
    ) -> region_pb2.RegionIdResponse | None:
        try:
            region_uuid = await interactor(NewRegionDTO(request.name, request.capital))

            return region_pb2.RegionIdResponse(region_id=str(region_uuid))
        except EntityAlreadyExistsError:
            await context.abort(
                grpc.StatusCode.ALREADY_EXISTS,
                f'Region with name {request.name} already exists',
            )

    @inject
    async def DeleteRegion(
        self,
        request: region_pb2.RegionIdRequest,
        context: ServicerContext,
        interactor: FromDishka[DeleteRegionInteractor],
    ) -> Empty:
        await interactor(region_id=uuid.UUID(request.region_id))
        return Empty()
