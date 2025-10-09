import uuid

from city_api.application.dto.region import NewRegionDTO
from city_api.application.errors import EntityAlreadyExistsError
from city_api.application.interface.region.region import RegionSaver
from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.uuid_generator import UUIDGenerator
from city_api.domain.entities.region import RegionDM


class CreateRegionCommand:
    def __init__(
        self,
        region_gateway: RegionSaver,
        uuid_generator: UUIDGenerator,
        transaction_manager: TransactionManager,
    ):
        self._region_gateway = region_gateway
        self._uuid_generator = uuid_generator
        self._transaction_manager = transaction_manager

    async def __call__(self, region: NewRegionDTO) -> uuid:
        region_id = self._uuid_generator()
        region = RegionDM(id=region_id, name=region.name, capital=region.capital)
        if await self._region_gateway.exist_with_name(region_name=region.name):
            raise EntityAlreadyExistsError

        await self._region_gateway.save(region)
        await self._transaction_manager.commit()
        return region_id
