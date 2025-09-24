import pytest
from faker import Faker
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.district import DistrictDM
from app.infrastructure.db.models import District, Region
from app.infrastructure.gateway.district import DistrictGateway
from app.infrastructure.gateway.region import RegionGateway

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def district_gateway(session: AsyncSession) -> DistrictGateway:
    return DistrictGateway(session=session)


@pytest.fixture
async def region_gateway(session: AsyncSession) -> RegionGateway:
    return RegionGateway(session=session)


async def test_create_district(
    session: AsyncSession, district_gateway: DistrictGateway, faker: Faker
) -> None:
    rg_uuid = faker.uuid4()

    ds_uuid = faker.uuid4()
    ds_name = faker.pystr()

    stmt = insert(District).values(id=ds_uuid, region_id=rg_uuid, name=ds_name)
    await session.execute(stmt)
    await session.commit()

    result = await district_gateway.get_by_uuid(ds_uuid)

    assert str(result.region_id) == rg_uuid
    assert result.name == ds_name


async def test_save_district(
    session: AsyncSession, district_gateway: DistrictGateway, faker: Faker
) -> None:
    district = DistrictDM(
        id=faker.uuid4(),
        region_id=faker.uuid4(),
        name=faker.pystr(),
    )

    await district_gateway.save(district)
    result = await district_gateway.get_by_uuid(district.id)

    assert str(result.id) == district.id
    assert str(result.region_id) == district.region_id
    assert result.name == district.name


async def test_create_few_districts(
    session: AsyncSession, district_gateway: DistrictGateway, faker: Faker
) -> None:
    district_first = DistrictDM(
        id=faker.uuid4(),
        region_id=faker.uuid4(),
        name=faker.pystr(),
    )

    district_second = DistrictDM(
        id=faker.uuid4(),
        region_id=faker.uuid4(),
        name=faker.pystr(),
    )

    await district_gateway.save(district_first)
    await district_gateway.save(district_second)
    result = await district_gateway.get_districts()

    assert len(result) == 2
    assert str(result[0].id) == district_first.id
    assert str(result[1].id) == district_second.id


async def test_get_districts_by_region_id(
    session: AsyncSession, district_gateway: DistrictGateway, faker: Faker
) -> None:
    rg_uuid = faker.uuid4()
    rg_name = faker.pystr()
    rg_capital = faker.pystr()

    stmt = insert(Region).values(id=rg_uuid, name=rg_name, capital=rg_capital)
    await session.execute(stmt)

    ds_uuid = faker.uuid4()
    ds_name = faker.pystr()

    stmt = insert(District).values(id=ds_uuid, region_id=rg_uuid, name=ds_name)
    await session.execute(stmt)
    await session.commit()

    result = await district_gateway.get_districts_by_region_uuid(rg_uuid)

    assert len(result) == 1
    assert str(result[0].id) == ds_uuid
    assert str(result[0].region_id) == rg_uuid
    assert result[0].name == ds_name


async def test_delete_district(
    session: AsyncSession, district_gateway: DistrictGateway, faker: Faker
) -> None:
    uuid = faker.uuid4()
    rg_uuid = faker.uuid4()
    name = faker.pystr()

    stmt = insert(District).values(id=uuid, region_id=rg_uuid, name=name)

    await session.execute(stmt)

    await district_gateway.delete_by_uuid(uuid)
    result = await district_gateway.get_by_uuid(uuid)

    query = select(District).where(District.id == uuid)
    row = (await session.execute(query)).scalar_one_or_none()

    assert result is None
    assert row is not None
    assert row.is_deleted is True
