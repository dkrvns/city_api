import uuid
from abc import abstractmethod
from typing import Protocol

from sqlalchemy import Sequence

from app.domain.entities.district import DistrictDM


class DistrictSaver(Protocol):
    @abstractmethod
    async def save(self, district: DistrictDM) -> None:
        ...


class DistrictReader(Protocol):
    @abstractmethod
    async def get_districts(self) -> Sequence[DistrictDM] | None:
        ...

    @abstractmethod
    async def get_districts_by_region_uuid(self, region_id: uuid.UUID) -> Sequence[DistrictDM]:
        ...

    @abstractmethod
    async def get_by_uuid(self, district_id: uuid.UUID) -> DistrictDM | None:
        ...


class DistrictDeleter(Protocol):
    @abstractmethod
    async def delete_by_uuid(self, district_id: uuid.UUID) -> None:
        ...
