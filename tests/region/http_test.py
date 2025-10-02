import uuid

from faker import Faker
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.region import NewRegionDTO
from app.infrastructure.db.models import Region


async def test_get_regions(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    uuid = faker.uuid4()
    name = faker.pystr()
    capital = faker.pystr()

    stmt = insert(Region).values(id=uuid, name=name, capital=capital)

    await session.execute(stmt)
    await session.commit()

    result = await http_client.get('/region/get_regions')
    assert result.status_code == 200

    assert len(result.json()) == 1
    assert result.json()[0]['id'] == uuid
    assert result.json()[0]['name'] == name
    assert result.json()[0]['capital'] == capital


async def test_empty_get_regions(
    http_client: AsyncClient,
) -> None:
    result = await http_client.get('/region/get_regions')
    assert result.status_code == 404
    assert result.json()['detail'] == 'Regions not found'


async def test_get_region_by_id(
    session: AsyncSession, http_client: AsyncClient, faker: Faker
) -> None:
    uuid = faker.uuid4()
    name = faker.pystr()
    capital = faker.pystr()

    stmt = insert(Region).values(id=uuid, name=name, capital=capital)

    await session.execute(stmt)
    await session.commit()

    result = await http_client.get(f'/region/get_by_id?region_id={uuid}')
    assert result.status_code == 200

    assert result.json()['id'] == uuid
    assert result.json()['name'] == name
    assert result.json()['capital'] == capital


async def test_get_empty_region_by_id(
    http_client: AsyncClient,
) -> None:
    result = await http_client.get(f'/region/get_by_id?region_id={uuid.uuid4()}')
    assert result.status_code == 404
    assert result.json()['detail'] == 'Region not found'


async def test_create_region(
    session: AsyncSession, http_client: AsyncClient, faker: Faker
) -> None:
    dto = NewRegionDTO(name=faker.pystr(), capital=faker.pystr())
    result_uuid = await http_client.post(
        '/region/create_region',
        json={
            'name': dto.name,
            'capital': dto.capital,
        },
    )

    result_obj = await http_client.get(
        f'/region/get_by_id?region_id={result_uuid.json()}'
    )

    assert result_uuid.status_code == 200

    assert result_obj.json()['name'] == dto.name
    assert result_obj.json()['capital'] == dto.capital


async def test_create_regions_with_same_name(
    session: AsyncSession, http_client: AsyncClient, faker: Faker
) -> None:
    dto = NewRegionDTO(name=faker.pystr(), capital=faker.pystr())
    result_first = await http_client.post(
        '/region/create_region',
        json={
            'name': dto.name,
            'capital': dto.capital,
        },
    )

    result_second = await http_client.post(
        '/region/create_region',
        json={
            'name': dto.name,
            'capital': dto.capital,
        },
    )

    assert result_first.status_code == 200

    assert result_second.status_code == 409
    assert (
        result_second.json()['detail'] == f'Region with name {dto.name} already exists'
    )


async def test_delete_region(
    session: AsyncSession, http_client: AsyncClient, faker: Faker
) -> None:
    uuid = faker.uuid4()
    name = faker.pystr()
    capital = faker.pystr()

    stmt = insert(Region).values(id=uuid, name=name, capital=capital)

    await session.execute(stmt)
    await session.commit()

    result_del = await http_client.delete(f'/region/delete_region?region_id={uuid}')
    result_get = await http_client.get(f'/region/get_by_id?region_id={uuid}')

    assert result_del.status_code == 200

    assert result_get.status_code == 404
    assert result_get.json()['detail'] == 'Region not found'
