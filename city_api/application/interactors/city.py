from collections.abc import Sequence
from uuid import UUID

from city_api.application.interface.city.city import (
    CityDeleter,
    CityReader,
)
from city_api.application.interface.transaction_manager import TransactionManager
from city_api.domain.entities.city import CityDM


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


class DeleteCityInteractor:
    def __init__(
        self, city_gateway: CityDeleter, transaction_manager: TransactionManager
    ):
        self._city_gateway = city_gateway
        self._transaction_manager = transaction_manager

    async def __call__(self, city_id: UUID) -> None:
        await self._city_gateway.delete_by_uuid(city_id)
        await self._transaction_manager.commit()
