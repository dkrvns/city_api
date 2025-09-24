import uuid
from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest
from faker import Faker

from app.application.commands.city import CreateCityCommand, UpdateCityCommand
from app.application.dto.city import NewCityDTO, UpdatedCityDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.city import (
    DeleteCityInteractor,
    GetCitiesByDistrictIdInteractor,
    GetCitiesInteractor,
    GetCityByIdInteractor,
)
from app.application.interface.city.city import (
    CityDeleter,
    CityReader,
    CitySaver,
    CityUpdater,
)
from app.application.interface.district.district import DistrictReader
from app.domain.entities.city import CityDM


@pytest.fixture
def get_cities_interactor() -> GetCitiesInteractor:
    city_gateway = create_autospec(CityReader)
    return GetCitiesInteractor(city_gateway)


async def test_get_cities(get_cities_interactor: GetCitiesInteractor) -> None:
    result = await get_cities_interactor()
    get_cities_interactor._city_gateway.get_cities.assert_awaited_once_with()
    assert result == get_cities_interactor._city_gateway.get_cities.return_value


@pytest.fixture
def get_cities_by_district_id() -> GetCitiesByDistrictIdInteractor:
    city_gateway = create_autospec(CityReader)
    return GetCitiesByDistrictIdInteractor(city_gateway)


@pytest.mark.parametrize('district_id', [uuid.uuid4(), uuid.uuid4()])
async def test_get_cities_by_district_id(
    get_cities_by_district_id: GetCitiesByDistrictIdInteractor, district_id: uuid.UUID
):
    result = await get_cities_by_district_id(district_id=district_id)
    get_cities_by_district_id._city_gateway.get_cities_by_district_uuid.assert_awaited_once_with(
        district_id=district_id
    )
    assert (
        result
        == get_cities_by_district_id._city_gateway.get_cities_by_district_uuid.return_value
    )


@pytest.fixture
def get_city_by_uuid() -> GetCityByIdInteractor:
    city_gateway = create_autospec(CityReader)
    return GetCityByIdInteractor(city_gateway)


@pytest.mark.parametrize('city_id', [uuid.uuid4(), uuid.uuid4()])
async def test_get_city_by_uuid(
    get_city_by_uuid: GetCityByIdInteractor, city_id: uuid.UUID
):
    result = await get_city_by_uuid(city_id=city_id)
    get_city_by_uuid._city_gateway.get_by_uuid.assert_awaited_once_with(city_id=city_id)
    assert result == get_city_by_uuid._city_gateway.get_by_uuid.return_value


@pytest.fixture
def create_city(faker: Faker) -> CreateCityCommand:
    city_gateway = create_autospec(CitySaver)
    district_gateway = create_autospec(DistrictReader)
    uuid_generator = MagicMock()
    return CreateCityCommand(city_gateway, district_gateway, uuid_generator)


async def test_create_city_success(
    create_city: CreateCityCommand, faker: Faker
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    dto = NewCityDTO(
        district_id=district_id,
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    create_city._uuid_generator.return_value = city_id
    create_city._district_gateway.get_by_uuid = AsyncMock(return_value=MagicMock())

    result = await create_city(dto)

    expected_city = CityDM(
        id=city_id,
        district_id=dto.district_id,
        name=dto.name,
        obj_type=dto.obj_type,
        population=dto.population,
    )
    create_city._city_gateway.save.assert_awaited_once_with(expected_city)
    create_city._district_gateway.get_by_uuid.assert_awaited_once_with(district_id)
    create_city._uuid_generator.assert_called_once()

    assert result == city_id


async def test_create_city_district_not_exists(
    create_city: CreateCityCommand, faker: Faker
) -> None:
    dto = NewCityDTO(
        district_id=uuid.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    create_city._district_gateway.get_by_uuid = AsyncMock(return_value=None)

    with pytest.raises(EntityNotExistsError):
        await create_city(dto)

    create_city._city_gateway.save.assert_not_awaited()
    create_city._uuid_generator.assert_not_called()


@pytest.fixture
def delete_city() -> DeleteCityInteractor:
    city_gateway = create_autospec(CityDeleter)
    return DeleteCityInteractor(city_gateway)


@pytest.mark.parametrize('city_id', [uuid.uuid4(), uuid.uuid4()])
async def test_delete_city(delete_city: DeleteCityInteractor, city_id: uuid.UUID):
    result = await delete_city(city_id=city_id)
    delete_city._city_gateway.delete_by_uuid.assert_awaited_once_with(city_id=city_id)
    assert result is None


@pytest.fixture
def update_city(faker: Faker) -> UpdateCityCommand:
    city_read_gateway = create_autospec(CityReader)
    city_update_gateway = create_autospec(CityUpdater)
    district_gateway = create_autospec(DistrictReader)
    return UpdateCityCommand(city_read_gateway, city_update_gateway, district_gateway)


async def test_update_city_success(
    update_city: UpdateCityCommand, faker: Faker
) -> None:
    city_id = uuid.uuid4()
    district_id = uuid.uuid4()
    dto = UpdatedCityDTO(
        city_id=city_id,
        district_id=district_id,
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    update_city._district_gateway.get_by_uuid = AsyncMock(return_value=MagicMock())
    update_city._city_read_gateway.get_by_uuid = AsyncMock(return_value=MagicMock())

    result = await update_city(dto)

    expected_city = CityDM(
        id=dto.city_id,
        district_id=dto.district_id,
        name=dto.name,
        obj_type=dto.obj_type,
        population=dto.population,
    )
    update_city._city_update_gateway.update_by_uuid.assert_awaited_once_with(
        expected_city
    )
    update_city._district_gateway.get_by_uuid.assert_awaited_once_with(district_id)
    update_city._city_read_gateway.get_by_uuid.assert_awaited_once_with(city_id)

    assert result == city_id


async def test_update_city_district_not_exists(
    update_city: UpdateCityCommand, faker: Faker
) -> None:
    dto = UpdatedCityDTO(
        city_id=uuid.uuid4(),
        district_id=uuid.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    update_city._district_gateway.get_by_uuid = AsyncMock(return_value=None)

    with pytest.raises(EntityNotExistsError, match='District does not exist'):
        await update_city(dto)

    update_city._city_update_gateway.update_by_uuid.assert_not_awaited()


async def test_update_city_not_exists(
    update_city: UpdateCityCommand, faker: Faker
) -> None:
    dto = UpdatedCityDTO(
        city_id=uuid.uuid4(),
        district_id=uuid.uuid4(),
        name=faker.pystr(),
        obj_type=faker.pystr(),
        population=faker.pyint(),
    )

    update_city._district_gateway.get_by_uuid = AsyncMock(return_value=MagicMock())
    update_city._city_read_gateway.get_by_uuid = AsyncMock(return_value=None)

    with pytest.raises(EntityNotExistsError, match='City does not exist'):
        await update_city(dto)

    update_city._city_update_gateway.update_by_uuid.assert_not_awaited()
