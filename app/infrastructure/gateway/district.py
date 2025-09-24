import uuid

from sqlalchemy import Sequence, and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
    DistrictSaver,
)
from app.domain.entities.district import DistrictDM
from app.infrastructure.db.models import District


class DistrictGateway(DistrictSaver, DistrictReader, DistrictDeleter):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_districts(self) -> Sequence[DistrictDM] | None:
        query = select(District).where(and_(District.is_deleted == False))
        result = await self._session.execute(query)

        return [self._map_row_to_read_model(row) for row in result.scalars()]

    async def get_districts_by_region_uuid(
        self, region_id: uuid.UUID
    ) -> Sequence[DistrictDM]:
        query = select(District).where(
            and_(District.region_id == region_id, District.is_deleted == False)
        )
        result = await self._session.execute(query)

        return [self._map_row_to_read_model(row) for row in result.scalars()]

    async def get_by_uuid(self, district_id: uuid.UUID) -> DistrictDM | None:
        query = select(District).where(
            and_(District.id == district_id, District.is_deleted == False)
        )
        result = await self._session.execute(query)

        row = result.scalar_one_or_none()
        if not row:
            return None

        return self._map_row_to_read_model(row)

    async def save(self, district: DistrictDM) -> None:
        query = insert(District).values(
            id=district.id, region_id=district.region_id, name=district.name
        )

        await self._session.execute(query)
        await self._session.commit()

    async def delete_by_uuid(self, district_id: uuid.UUID) -> None:
        stmt = (
            update(District)
            .where(
                and_(District.id == district_id),
            )
            .values(is_deleted=True)
        )

        await self._session.execute(stmt)
        await self._session.commit()

    @staticmethod
    def _map_row_to_read_model(row: District) -> DistrictDM:
        return DistrictDM(
            id=row.id,
            region_id=row.region_id,
            name=row.name,
        )
