from collections.abc import Sequence
from uuid import UUID

from app.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
)
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


class DeleteDistrictInteractor:
    def __init__(self, district_gateway: DistrictDeleter):
        self._district_gateway = district_gateway

    async def __call__(self, district_id: UUID) -> None:
        await self._district_gateway.delete_by_uuid(district_id)
