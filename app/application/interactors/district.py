from collections.abc import Sequence
from uuid import UUID

from app.application.dto.district import NewDistrictDTO
from app.application.errors import EntityNotExistsError
from app.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
    DistrictSaver,
)
from app.application.interface.region.region import RegionReader
from app.application.interface.uuid_generator import UUIDGenerator
from app.domain.entities.district import DistrictDM


class GetDistrictsInteractor:
    def __init__(self, district_gateway: DistrictReader):
        self._district_gateway = district_gateway

    async def __call__(self) -> Sequence[DistrictDM]:
        return await self._district_gateway.get_districts()


class GetDistrictsByRegionIdInteractor:
    def __init__(self, district_gateway: DistrictReader):
        self._district_gateway = district_gateway

    async def __call__(self, region_id: UUID) -> Sequence[DistrictDM]:
        return await self._district_gateway.get_districts_by_region_uuid(region_id)


class GetDistrictByIdInteractor:
    def __init__(self, district_gateway: DistrictReader):
        self._district_gateway = district_gateway

    async def __call__(self, district_id: UUID) -> DistrictDM | None:
        return await self._district_gateway.get_by_uuid(district_id)


class CreateDistrictInteractor:
    def __init__(
        self,
        district_gateway: DistrictSaver,
        region_gateway: RegionReader,
        uuid_generator: UUIDGenerator,
    ):
        self._district_gateway = district_gateway
        self._region_gateway = region_gateway
        self._uuid_generator = uuid_generator

    async def __call__(self, district_dto: NewDistrictDTO) -> UUID:
        if await self._region_gateway.get_by_uuid(district_dto.region_id) is None:
            raise EntityNotExistsError

        district_id = self._uuid_generator()
        district = DistrictDM(
            id=district_id, region_id=district_dto.region_id, name=district_dto.name
        )

        await self._district_gateway.save(district)
        return district_id


class DeleteDistrictInteractor:
    def __init__(self, district_gateway: DistrictDeleter):
        self._district_gateway = district_gateway

    async def __call__(self, district_id: UUID) -> None:
        await self._district_gateway.delete_by_uuid(district_id)
