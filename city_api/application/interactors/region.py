import uuid
from collections.abc import Sequence

from city_api.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
)
from city_api.application.interface.transaction_manager import TransactionManager
from city_api.domain.entities.region import RegionDM


class GetRegionsInteractor:
    def __init__(self, region_gateway: RegionReader):
        self._region_gateway = region_gateway

    async def __call__(self) -> Sequence[RegionDM]:
        return await self._region_gateway.get_regions()


class GetRegionByIdInteractor:
    def __init__(self, region_gateway: RegionReader):
        self._region_gateway = region_gateway

    async def __call__(self, region_id: uuid.UUID) -> RegionDM | None:
        return await self._region_gateway.get_by_uuid(region_id)


class DeleteRegionInteractor:
    def __init__(
        self,
        region_gateway: RegionDeleter,
        transaction_manager: TransactionManager,
    ):
        self._region_gateway = region_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, region_id: uuid.UUID) -> None:
        await self._region_gateway.delete_by_uuid(region_id)
        await self._transaction_manager.commit()
