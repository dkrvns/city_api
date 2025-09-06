import uuid
from collections.abc import Sequence
from uuid import UUID

from app.application.dto.city import NewCityDTO
from app.application.errors import EntityNotExistsError
from app.application.interface.city.city import (
    CityDeleter,
    CityReader,
    CitySaver,
)
from app.application.interface.district.district import DistrictReader
from app.domain.entities.city import CityDM


class GetCitiesInteractor:
    def __init__(self, city_gateway: CityReader):
        self._city_gateway = city_gateway

    async def __call__(self) -> Sequence[CityDM]:
        return await self._city_gateway.get_cities()


class GetCitiesByDistrictIdInteractor:
    def __init__(self, city_gateway: CityReader):
        self._city_gateway = city_gateway

    async def __call__(self, district_id: UUID) -> Sequence[CityDM]:
        return await self._city_gateway.get_cities_by_district_uuid(district_id)


class GetCityByIdInteractor:
    def __init__(self, city_gateway: CityReader):
        self._city_gateway = city_gateway

    async def __call__(self, city_id: UUID) -> CityDM | None:
        return await self._city_gateway.get_by_uuid(city_id)


class CreateCityInteractor:
    def __init__(self, city_gateway: CitySaver, district_gateway: DistrictReader):
        self._city_gateway = city_gateway
        self._district_gateway = district_gateway

    async def __call__(self, city_dto: NewCityDTO) -> UUID:
        if await self._district_gateway.get_by_uuid(city_dto.district_id) is None:
            raise EntityNotExistsError

        city_id = uuid.uuid4()
        city = CityDM(
            id=city_id,
            district_id=city_dto.district_id,
            name=city_dto.name,
            obj_type=city_dto.obj_type,
            population=city_dto.population,
        )

        await self._city_gateway.save(city)
        return city_id


class DeleteCityInteractor:
    def __init__(self, city_gateway: CityDeleter):
        self._city_gateway = city_gateway

    async def __call__(self, city_id: UUID) -> None:
        await self._city_gateway.delete_by_uuid(city_id)
