import uuid
from collections.abc import Sequence

from app.application.dto.region import NewRegionDTO
from app.application.errors import EntityAlreadyExistsError
from app.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
    RegionSaver,
)
from app.application.interface.uuid_generator import UUIDGenerator
from app.domain.entities.region import RegionDM


class GetRegionsInteractor:
    def __init__(
        self,
        region_gateway: RegionReader
    ):
        self._region_gateway = region_gateway

    async def __call__(self) -> Sequence[RegionDM]:
        return await self._region_gateway.get_regions()


class GetRegionByIdInteractor:
    def __init__(
        self,
        region_gateway: RegionReader
    ):
        self._region_gateway = region_gateway

    async def __call__(self, region_id: uuid.UUID) -> RegionDM | None:
        return await self._region_gateway.get_by_uuid(region_id)


class CreateRegionInteractor:
    def __init__(
        self,
        region_gateway: RegionSaver,
        uuid_generator: UUIDGenerator
    ):
        self._region_gateway = region_gateway
        self._uuid_generator = uuid_generator

    async def __call__(self, region: NewRegionDTO) -> uuid:
        region_id = self._uuid_generator()
        region = RegionDM(
            id=region_id,
            name=region.name,
            capital=region.capital
        )
        if await self._region_gateway.exist_with_name(region_name=region.name):
            raise EntityAlreadyExistsError

        await self._region_gateway.save(region)
        return region_id


class DeleteRegionInteractor:
    def __init__(
            self,
        region_gateway: RegionDeleter
    ):
        self._region_gateway = region_gateway

    async def __call__(self, region_id: uuid.UUID) -> None:
        await self._region_gateway.delete_by_uuid(region_id)
