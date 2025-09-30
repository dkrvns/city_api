import uuid
from collections.abc import Sequence

from sqlalchemy import and_, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.interface.city.city import (
    CityDeleter,
    CityReader,
    CitySaver,
    CityUpdater,
)
from app.domain.entities.city import CityDM
from app.infrastructure.db.models import City


class CityGateway(CitySaver, CityReader, CityDeleter, CityUpdater):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_cities(self) -> Sequence[CityDM]:
        query = select(City).where(and_(City.is_deleted == False))
        result = await self._session.execute(query)

        return [self._map_row_to_read_model(row) for row in result.scalars()]

    async def get_cities_by_district_uuid(
        self, district_id: uuid.UUID
    ) -> Sequence[CityDM]:
        query = select(City).where(
            and_(City.district_id == district_id, City.is_deleted == False)
        )
        result = await self._session.execute(query)

        return [self._map_row_to_read_model(row) for row in result.scalars()]

    async def get_by_uuid(self, city_id: uuid.UUID) -> CityDM | None:
        query = select(City).where(and_(City.id == city_id, City.is_deleted == False))
        result = await self._session.execute(query)

        row = result.scalar_one_or_none()
        if not row:
            return None

        return self._map_row_to_read_model(row)

    async def save(self, city: CityDM) -> None:
        query = insert(City).values(
            id=city.id,
            district_id=city.district_id,
            name=city.name,
            obj_type=city.obj_type,
            population=city.population,
        )

        await self._session.execute(query)
        await self._session.commit()

    async def delete_by_uuid(self, city_id: uuid.UUID) -> None:
        stmt = (
            update(City)
            .where(
                and_(City.id == city_id),
            )
            .values(is_deleted=True)
        )

        await self._session.execute(stmt)
        await self._session.commit()

    async def update_by_uuid(self, city: CityDM) -> None:
        stmt = update(City).where(and_(City.id == city.id)).values(**city.__dict__)
        await self._session.execute(stmt)
        await self._session.commit()

    @staticmethod
    def _map_row_to_read_model(row: City) -> CityDM:
        return CityDM(
            id=row.id,
            district_id=row.district_id,
            name=row.name,
            obj_type=row.obj_type,
            population=row.population,
        )
