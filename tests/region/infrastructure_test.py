import pytest
from faker import Faker
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.region import RegionDM
from app.infrastructure.db.models import Region
from app.infrastructure.gateway.region import RegionGateway

pytestmark = pytest.mark.asyncio


@pytest.fixture
async def region_gateway(session: AsyncSession) -> RegionGateway:
    return RegionGateway(session=session)


async def test_create_region(
    session: AsyncSession, region_gateway: RegionGateway, faker: Faker
) -> None:
    uuid = faker.uuid4()
    name = faker.pystr()
    capital = faker.pystr()

    stmt = insert(Region).values(id=uuid, name=name, capital=capital)

    await session.execute(stmt)

    result = await region_gateway.get_by_uuid(uuid)
    assert result.name == name
    assert result.capital == capital


async def test_save_region(
    session: AsyncSession, region_gateway: RegionGateway, faker: Faker
) -> None:
    region = RegionDM(
        id=faker.uuid4(),
        name=faker.pystr(),
        capital=faker.pystr(),
    )
    await region_gateway.save(region)

    result = await region_gateway.get_by_uuid(region.id)
    assert str(result.id) == region.id
    assert result.name == region.name
    assert result.capital == region.capital


async def test_create_few_regions(
    session: AsyncSession, region_gateway: RegionGateway, faker: Faker
) -> None:
    region_first = RegionDM(
        id=faker.uuid4(),
        name=faker.pystr(),
        capital=faker.pystr(),
    )
    region_second = RegionDM(
        id=faker.uuid4(),
        name=faker.pystr(),
        capital=faker.pystr(),
    )
    await region_gateway.save(region_first)
    await region_gateway.save(region_second)

    result = await region_gateway.get_regions()
    assert len(result) == 2
    assert str(result[0].id) == region_first.id
    assert str(result[1].id) == region_second.id


async def test_delete_region(
    session: AsyncSession, region_gateway: RegionGateway, faker: Faker
) -> None:
    uuid = faker.uuid4()
    name = faker.pystr()
    capital = faker.pystr()

    stmt = insert(Region).values(id=uuid, name=name, capital=capital)

    await session.execute(stmt)

    await region_gateway.delete_by_uuid(uuid)
    result = await region_gateway.get_by_uuid(uuid)

    assert result is None
