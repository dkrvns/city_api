from abc import abstractmethod
from collections.abc import Sequence
from typing import Protocol
from uuid import UUID

from app.domain.entities.city import CityDM


class CitySaver(Protocol):
    @abstractmethod
    async def save(self, city: CityDM) -> None:
        ...


class CityReader(Protocol):
    @abstractmethod
    async def get_cities(self) -> Sequence[CityDM]:
        ...

    @abstractmethod
    async def get_cities_by_district_uuid(self, district_id: UUID) -> Sequence[CityDM]:
        ...

    @abstractmethod
    async def get_by_uuid(self, city_id: UUID) -> CityDM | None:
        ...


class CityDeleter(Protocol):
    @abstractmethod
    async def delete_by_uuid(self, city_id: UUID) -> None:
        ...


class CityUpdater(Protocol):
    @abstractmethod
    async def update_by_uuid(self, city: CityDM) -> None:
        ...
