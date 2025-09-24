from uuid import UUID

from app.application.dto.district import NewDistrictDTO
from app.application.errors import EntityNotExistsError
from app.application.interface.district.district import DistrictSaver
from app.application.interface.region.region import RegionReader
from app.application.interface.uuid_generator import UUIDGenerator
from app.domain.entities.district import DistrictDM


class CreateDistrictCommand:
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
