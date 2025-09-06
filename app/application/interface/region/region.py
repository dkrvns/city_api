import uuid
from abc import abstractmethod
from typing import Protocol

from sqlalchemy import Sequence

from app.domain.entities.region import RegionDM


class RegionSaver(Protocol):
    @abstractmethod
    async def save(self, region: RegionDM) -> None:
        ...

    @abstractmethod
    async def exist_with_name(self, region_name: str) -> bool:
        ...


class RegionReader(Protocol):
    @abstractmethod
    async def get_regions(self) -> Sequence[RegionDM] | None:
        ...

    @abstractmethod
    async def get_by_uuid(self, region_id: uuid.UUID) -> RegionDM | None:
        ...


class RegionDeleter(Protocol):
    @abstractmethod
    async def delete_by_uuid(self, region_id: uuid.UUID) -> None:
        ...
