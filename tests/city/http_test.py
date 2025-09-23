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

from app.application.dto.city import NewCityDTO, UpdatedCityDTO
from app.infrastructure.db.models import City as CityModel
from app.infrastructure.db.models import District, Region
from app.presentation.api.city import city_router


@pytest.fixture
async def http_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI()
    app.include_router(city_router)

    fastapi_integration.setup_dishka(container, app)
    return app


@pytest.fixture
async def http_client(http_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=http_app), base_url='http://test'
    ) as client:
        yield client


async def test_get_cities(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
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
        insert(CityModel).values(
            id=city_id,
            district_id=district_id,
            name=name,
            obj_type=obj_type,
            population=population,
        )
    )
    await session.commit()

    result = await http_client.get('/cities/get_cities')
    assert result.status_code == 200

    assert len(result.json()) == 1
    assert result.json()[0]['id'] == str(city_id)
    assert result.json()[0]['district_id'] == str(district_id)
    assert result.json()[0]['name'] == name
    assert result.json()[0]['obj_type'] == obj_type
    assert result.json()[0]['population'] == population


async def test_empty_get_cities(
    http_client: AsyncClient,
) -> None:
    result = await http_client.get('/cities/get_cities')
    assert result.status_code == 404
    assert result.json()['detail'] == 'Cities not found'


async def test_get_cities_by_district_id(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
    city_id = uuid.uuid4()
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
        insert(CityModel).values(
            id=city_id,
            district_id=district_id,
            name=name,
            obj_type=obj_type,
            population=population,
        )
    )
    await session.commit()

    result = await http_client.get(
        f'/cities/get_cities_by_district?district_id={district_id}'
    )
    assert result.status_code == 200

    assert len(result.json()) == 1
    assert result.json()[0]['id'] == str(city_id)
    assert result.json()[0]['district_id'] == str(district_id)
    assert result.json()[0]['name'] == name
    assert result.json()[0]['obj_type'] == obj_type
    assert result.json()[0]['population'] == population


async def test_get_empty_cities_by_district_id(
    http_client: AsyncClient,
) -> None:
    district_id = uuid.uuid4()
    result = await http_client.get(
        f'/cities/get_cities_by_district?district_id={district_id}'
    )
    assert result.status_code == 404
    assert result.json()['detail'] == 'Cities not found for this district'


async def test_get_city_by_id(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
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
        insert(CityModel).values(
            id=city_id,
            district_id=district_id,
            name=name,
            obj_type=obj_type,
            population=population,
        )
    )
    await session.commit()

    result = await http_client.get(f'/cities/get_city_by_id?city_id={city_id}')
    assert result.status_code == 200

    assert result.json()['id'] == str(city_id)
    assert result.json()['district_id'] == str(district_id)
    assert result.json()['name'] == name
    assert result.json()['obj_type'] == obj_type
    assert result.json()['population'] == population


async def test_get_empty_city_by_id(
    http_client: AsyncClient,
) -> None:
    city_id = uuid.uuid4()
    result = await http_client.get(f'/cities/get_city_by_id?city_id={city_id}')
    assert result.status_code == 404
    assert result.json()['detail'] == 'City not found'


async def test_create_city(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
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
    await session.commit()

    dto = NewCityDTO(
        district_id=district_id,
        name=name,
        obj_type=obj_type,
        population=population,
    )

    result_uuid = await http_client.post(
        '/cities/create_city',
        json={
            'district_id': str(dto.district_id),
            'name': dto.name,
            'obj_type': dto.obj_type,
            'population': dto.population,
        },
    )

    assert result_uuid.status_code == 200
    created_id = result_uuid.json()

    result_obj = await http_client.get(f'/cities/get_city_by_id?city_id={created_id}')

    assert result_obj.status_code == 200
    assert result_obj.json()['name'] == name
    assert result_obj.json()['district_id'] == str(district_id)
    assert result_obj.json()['obj_type'] == obj_type
    assert result_obj.json()['population'] == population


async def test_create_city_with_nonexistent_district(
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    name = faker.pystr()
    obj_type = faker.pystr()
    population = faker.pyint()

    dto = NewCityDTO(
        district_id=district_id,
        name=name,
        obj_type=obj_type,
        population=population,
    )

    result = await http_client.post(
        '/cities/create_city',
        json={
            'district_id': str(dto.district_id),
            'name': dto.name,
            'obj_type': dto.obj_type,
            'population': dto.population,
        },
    )

    assert result.status_code == 404
    assert (
        result.json()['detail']
        == 'District not found. Please check if this district exists'
    )


async def test_delete_city(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
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
        insert(CityModel).values(
            id=city_id,
            district_id=district_id,
            name=name,
            obj_type=obj_type,
            population=population,
        )
    )
    await session.commit()

    result_del = await http_client.delete(f'/cities/delete_city?city_id={city_id}')
    result_get = await http_client.get(f'/cities/get_city_by_id?city_id={city_id}')

    assert result_del.status_code == 200
    assert result_get.status_code == 404
    assert result_get.json()['detail'] == 'City not found'


async def test_update_city(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()
    old_name = faker.pystr()
    old_obj_type = faker.pystr()
    old_population = faker.pyint()

    new_name = faker.pystr()
    new_obj_type = faker.pystr()
    new_population = faker.pyint()

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
        insert(CityModel).values(
            id=city_id,
            district_id=district_id,
            name=old_name,
            obj_type=old_obj_type,
            population=old_population,
        )
    )
    await session.commit()

    dto = UpdatedCityDTO(
        city_id=city_id,
        district_id=district_id,
        name=new_name,
        obj_type=new_obj_type,
        population=new_population,
    )

    result_uuid = await http_client.put(
        '/cities/update_city',
        json={
            'city_id': str(dto.city_id),
            'district_id': str(dto.district_id),
            'name': dto.name,
            'obj_type': dto.obj_type,
            'population': dto.population,
        },
    )

    result_obj = await http_client.get(f'/cities/get_city_by_id?city_id={city_id}')

    assert result_uuid.status_code == 200
    assert result_uuid.json() == str(city_id)

    assert result_obj.status_code == 200
    assert result_obj.json()['name'] == new_name
    assert result_obj.json()['obj_type'] == new_obj_type
    assert result_obj.json()['population'] == new_population


async def test_update_nonexistent_city(
    session: AsyncSession,
    http_client: AsyncClient,
    faker: Faker,
) -> None:
    district_id = uuid.uuid4()
    region_id = uuid.uuid4()

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

    city_id = uuid.uuid4()
    dto = UpdatedCityDTO(
        city_id=city_id,
        district_id=district_id,
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    result = await http_client.put(
        '/cities/update_city',
        json={
            'city_id': str(dto.city_id),
            'district_id': str(dto.district_id),
            'name': dto.name,
            'obj_type': dto.obj_type,
            'population': dto.population,
        },
    )

    assert result.status_code == 404
    assert result.json()['detail'] == 'City does not exist'
