import uuid
from collections.abc import Sequence

from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
    RegionSaver,
)
from app.domain.entities.region import RegionDM
from app.infrastructure.db.models import Region


class RegionGateway(RegionSaver, RegionReader, RegionDeleter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_regions(self) -> Sequence[RegionDM]:
        query = select(Region).where(and_(Region.is_deleted == False))
        result = await self._session.execute(query)

        return [self._map_row_to_read_model(row) for row in result.scalars()]

    async def get_by_uuid(self, region_id: uuid.UUID) -> RegionDM | None:
        query = select(Region).where(
            and_(Region.id == region_id, Region.is_deleted == False)
        )
        result = await self._session.execute(query)

        row = result.scalar_one_or_none()
        if not row:
            return None

        return self._map_row_to_read_model(row)

    async def save(self, region: RegionDM) -> None:
        query = insert(Region).values(
            id=region.id, name=region.name, capital=region.capital
        )

        await self._session.execute(query)
        await self._session.commit()

    async def exist_with_name(self, region_name: str) -> bool:
        query = select(Region).where(
            and_(Region.name == region_name, Region.is_deleted == False)
        )

        result = await self._session.execute(query)
        return bool(result.scalar())

    async def delete_by_uuid(self, region_id: uuid.UUID) -> None:
        stmt = (
            update(Region)
            .where(
                and_(Region.id == region_id),
            )
            .values(is_deleted=True)
        )

        await self._session.execute(stmt)
        await self._session.commit()

    @staticmethod
    def _map_row_to_read_model(row: Region) -> RegionDM:
        return RegionDM(id=row.id, name=row.name, capital=row.capital)
