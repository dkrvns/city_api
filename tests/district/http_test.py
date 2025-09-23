import uuid
from collections.abc import AsyncIterator

import pytest
from dishka import AsyncContainer
from dishka.integrations import fastapi as fastapi_integration
from faker import Faker
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.district import NewDistrictDTO
from app.infrastructure.db.models import District as DistrictModel
from app.infrastructure.db.models import Region
from app.presentation.api.district import district_router


@pytest.fixture
async def http_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(district_router)

    fastapi_integration.setup_dishka(container, app)
    return app


@pytest.fixture
async def http_client(http_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_app), base_url='http://test'
    ) as client:
        yield client


async def test_get_districts(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
    name = faker.pystr()

    stmt = insert(DistrictModel).values(
        id=district_id,
        region_id=region_id,
        name=name,
    )

    await session.execute(stmt)
    await session.commit()

    result = await http_client.get('/districts/get_districts')
    assert result.status_code == 200

    assert len(result.json()) == 1
    assert result.json()[0]['id'] == str(district_id)
    assert result.json()[0]['region_id'] == str(region_id)
    assert result.json()[0]['name'] == name


async def test_empty_get_districts(
    http_client: AsyncClient,
) -> None:
    result = await http_client.get('/districts/get_districts')
    assert result.status_code == 404
    assert result.json()['detail'] == 'Districts not found'


async def test_get_districts_by_region_id(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    region_id = uuid.uuid4()
    district_id = uuid.uuid4()
    name = faker.pystr()

    stmt = insert(DistrictModel).values(
        id=district_id,
        region_id=region_id,
        name=name,
    )

    await session.execute(stmt)
    await session.commit()

    result = await http_client.get(
        f'/districts/get_districts_by_region?region_id={region_id}'
    )
    assert result.status_code == 200

    assert len(result.json()) == 1
    assert result.json()[0]['id'] == str(district_id)
    assert result.json()[0]['region_id'] == str(region_id)
    assert result.json()[0]['name'] == name


async def test_get_empty_districts_by_region_id(
    http_client: AsyncClient,
) -> None:
    region_id = uuid.uuid4()
    result = await http_client.get(
        f'/districts/get_districts_by_region?region_id={region_id}'
    )
    assert result.status_code == 404
    assert result.json()['detail'] == 'District not found'


async def test_get_district_by_id(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
    name = faker.pystr()

    stmt = insert(DistrictModel).values(
        id=district_id,
        region_id=region_id,
        name=name,
    )

    await session.execute(stmt)
    await session.commit()

    result = await http_client.get(
        f'/districts/get_district_by_id?district_id={district_id}'
    )
    assert result.status_code == 200

    assert result.json()['id'] == str(district_id)
    assert result.json()['region_id'] == str(region_id)
    assert result.json()['name'] == name


async def test_get_empty_district_by_id(
    http_client: AsyncClient,
) -> None:
    district_id = uuid.uuid4()
    result = await http_client.get(
        f'/districts/get_district_by_id?district_id={district_id}'
    )
    assert result.status_code == 404
    assert result.json()['detail'] == 'District not found'


async def test_create_district(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    region_id = uuid.uuid4()
    name = faker.pystr()

    dto = NewDistrictDTO(region_id=region_id, name=name)

    await session.execute(
        insert(Region).values(
            id=region_id,
            name=faker.pystr(),
            capital=faker.pystr(),
        )
    )
    await session.commit()

    result_uuid = await http_client.post(
        '/districts/create_district',
        json={
            'region_id': str(dto.region_id),
            'name': dto.name,
        },
    )

    assert result_uuid.status_code == 200
    created_id = result_uuid.json()

    result_obj = await http_client.get(
        f'/districts/get_district_by_id?district_id={created_id}'
    )

    assert result_obj.status_code == 200
    assert result_obj.json()['name'] == name
    assert result_obj.json()['region_id'] == str(region_id)


async def test_create_district_with_nonexistent_region(
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    region_id = uuid.uuid4()
    name = faker.pystr()

    dto = NewDistrictDTO(region_id=region_id, name=name)

    result = await http_client.post(
        '/districts/create_district',
        json={
            'region_id': str(dto.region_id),
            'name': dto.name,
        },
    )

    assert result.status_code == 404
    assert (
        result.json()['detail']
        == 'Region not found. Please check if this region exists or create it'
    )


async def test_delete_district(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
    name = faker.pystr()

    stmt = insert(DistrictModel).values(
        id=district_id,
        region_id=region_id,
        name=name,
    )

    await session.execute(stmt)
    await session.commit()

    result_del = await http_client.delete(
        f'/districts/delete_district?district_id={district_id}'
    )
    result_get = await http_client.get(
        f'/districts/get_district_by_id?district_id={district_id}'
    )

    assert result_del.status_code == 200
    assert result_get.status_code == 404
    assert result_get.json()['detail'] == 'District not found'
