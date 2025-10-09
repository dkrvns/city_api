from uuid import UUID

from city_api.application.dto.district import NewDistrictDTO
from city_api.application.errors import EntityNotExistsError
from city_api.application.interface.district.district import DistrictSaver
from city_api.application.interface.region.region import RegionReader
from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.uuid_generator import UUIDGenerator
from city_api.domain.entities.district import DistrictDM


class CreateDistrictCommand:
    def __init__(
        self,
        district_gateway: DistrictSaver,
        region_gateway: RegionReader,
        uuid_generator: UUIDGenerator,
        transaction_manager: TransactionManager,
    ):
        self._district_gateway = district_gateway
        self._region_gateway = region_gateway
        self._uuid_generator = uuid_generator
        self._transaction_manager = transaction_manager

    async def __call__(self, district_dto: NewDistrictDTO) -> UUID:
        if await self._region_gateway.get_by_uuid(district_dto.region_id) is None:
            raise EntityNotExistsError

        district_id = self._uuid_generator()
        district = DistrictDM(
            id=district_id, region_id=district_dto.region_id, name=district_dto.name
        )

        await self._district_gateway.save(district)
        await self._transaction_manager.commit()

        return district_id
