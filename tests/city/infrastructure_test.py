import pytest
from faker import Faker
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.city import CityDM
from app.infrastructure.db.models import City, District, Region
from app.infrastructure.gateway.city import CityGateway

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def city_gateway(session: AsyncSession) -> CityGateway:
    return CityGateway(session=session)


async def test_create_city(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    district_id = faker.uuid4()
    city_id = faker.uuid4()
    name = faker.pystr()
    obj_type = faker.pystr()
    population = faker.pyint()

    stmt = insert(City).values(
        id=city_id,
        district_id=district_id,
        name=name,
        obj_type=obj_type,
        population=population,
        is_deleted=False,
    )
    await session.execute(stmt)
    await session.commit()

    result = await city_gateway.get_by_uuid(city_id)

    assert str(result.id) == city_id
    assert str(result.district_id) == district_id
    assert result.name == name
    assert result.obj_type == obj_type
    assert result.population == population


async def test_save_city(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    city = CityDM(
        id=faker.uuid4(),
        district_id=faker.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    await city_gateway.save(city)
    result = await city_gateway.get_by_uuid(city.id)

    assert str(result.id) == city.id
    assert str(result.district_id) == city.district_id
    assert result.name == city.name
    assert result.obj_type == city.obj_type
    assert result.population == city.population


async def test_create_few_cities(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    city_first = CityDM(
        id=faker.uuid4(),
        district_id=faker.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    city_second = CityDM(
        id=faker.uuid4(),
        district_id=faker.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    await city_gateway.save(city_first)
    await city_gateway.save(city_second)
    result = await city_gateway.get_cities()

    assert len(result) == 2
    assert str(result[0].id) == city_first.id
    assert str(result[1].id) == city_second.id


async def test_get_cities_by_district_id(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    region_id = faker.uuid4()
    district_id = faker.uuid4()
    city_id = faker.uuid4()
    name = faker.pystr()
    obj_type = faker.pystr()
    population = faker.pyint()

    await session.execute(
        insert(Region).values(
            id=region_id,
            name=faker.pystr(),
            capital=faker.pystr(),
        )
    )
    await session.execute(
        insert(District).values(
            id=district_id,
            region_id=region_id,
            name=faker.pystr(),
        )
    )
    await session.execute(
        insert(City).values(
            id=city_id,
            district_id=district_id,
            name=name,
            obj_type=obj_type,
            population=population,
            is_deleted=False,
        )
    )
    await session.commit()

    result = await city_gateway.get_cities_by_district_uuid(district_id)

    assert len(result) == 1
    assert str(result[0].id) == city_id
    assert str(result[0].district_id) == district_id
    assert result[0].name == name
    assert result[0].obj_type == obj_type
    assert result[0].population == population


async def test_delete_city(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    city_id = faker.uuid4()
    district_id = faker.uuid4()
    name = faker.pystr()
    obj_type = faker.pystr()
    population = faker.pyint()

    stmt = insert(City).values(
        id=city_id,
        district_id=district_id,
        name=name,
        obj_type=obj_type,
        population=population,
        is_deleted=False,
    )
    await session.execute(stmt)
    await session.commit()

    await city_gateway.delete_by_uuid(city_id)

    result = await city_gateway.get_by_uuid(city_id)
    assert result is None

    query = select(City).where(City.id == city_id)
    row = (await session.execute(query)).scalar_one_or_none()
    assert row is not None
    assert row.is_deleted is True


async def test_update_city(
    session: AsyncSession, city_gateway: CityGateway, faker: Faker
) -> None:
    city_id = faker.uuid4()
    district_id = faker.uuid4()
    old_name = faker.pystr()
    old_obj_type = faker.pystr()
    old_population = faker.pyint()

    new_name = faker.pystr()
    new_obj_type = faker.pystr()
    new_population = faker.pyint()

    stmt = insert(City).values(
        id=city_id,
        district_id=district_id,
        name=old_name,
        obj_type=old_obj_type,
        population=old_population,
        is_deleted=False,
    )
    await session.execute(stmt)
    await session.commit()

    updated_city = CityDM(
        id=city_id,
        district_id=district_id,
        name=new_name,
        obj_type=new_obj_type,
        population=new_population,
    )

    await city_gateway.update_by_uuid(updated_city)
    result = await city_gateway.get_by_uuid(city_id)

    assert str(result.id) == city_id
    assert result.name == new_name
    assert result.obj_type == new_obj_type
    assert result.population == new_population
