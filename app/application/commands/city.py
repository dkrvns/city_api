from uuid import UUID

from app.application.dto.city import NewCityDTO, UpdatedCityDTO
from app.application.errors import EntityNotExistsError
from app.application.interface.city.city import CityReader, CitySaver, CityUpdater
from app.application.interface.district.district import DistrictReader
from app.application.interface.uuid_generator import UUIDGenerator
from app.domain.entities.city import CityDM


class CreateCityCommand:
    def __init__(
        self,
        city_gateway: CitySaver,
        district_gateway: DistrictReader,
        uuid_generator: UUIDGenerator,
    ):
        self._city_gateway = city_gateway
        self._district_gateway = district_gateway
        self._uuid_generator = uuid_generator

    async def __call__(self, city_dto: NewCityDTO) -> UUID:
        if await self._district_gateway.get_by_uuid(city_dto.district_id) is None:
            raise EntityNotExistsError

        city_id = self._uuid_generator()
        city = CityDM(
            id=city_id,
            district_id=city_dto.district_id,
            name=city_dto.name,
            obj_type=city_dto.obj_type,
            population=city_dto.population,
        )

        await self._city_gateway.save(city)
        return city_id


class UpdateCityCommand:
    def __init__(
        self,
        city_read_gateway: CityReader,
        city_update_gateway: CityUpdater,
        district_gateway: DistrictReader,
    ):
        self._city_read_gateway = city_read_gateway
        self._city_update_gateway = city_update_gateway
        self._district_gateway = district_gateway

    async def __call__(self, city_dto: UpdatedCityDTO):
        if await self._district_gateway.get_by_uuid(city_dto.district_id) is None:
            raise EntityNotExistsError('District does not exist')

        if await self._city_read_gateway.get_by_uuid(city_dto.city_id) is None:
            raise EntityNotExistsError('City does not exist')

        city = CityDM(
            id=city_dto.city_id,
            district_id=city_dto.district_id,
            name=city_dto.name,
            obj_type=city_dto.obj_type,
            population=city_dto.population,
        )
        await self._city_update_gateway.update_by_uuid(city)

        return city.id
