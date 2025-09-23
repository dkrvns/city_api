import uuid
from unittest.mock import AsyncMock, MagicMock, create_autospec

import pytest
from faker import Faker

from app.application.dto.district import NewDistrictDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.district import (
    CreateDistrictInteractor,
    DeleteDistrictInteractor,
    GetDistrictByIdInteractor,
    GetDistrictsByRegionIdInteractor,
    GetDistrictsInteractor,
)
from app.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
    DistrictSaver,
)
from app.application.interface.region.region import RegionReader
from app.domain.entities.district import DistrictDM


@pytest.fixture
def get_districts_interactor() -> GetDistrictsInteractor:
    ds_gateway = create_autospec(DistrictReader)
    return GetDistrictsInteractor(ds_gateway)


async def test_get_districts(get_districts_interactor: GetDistrictsInteractor) -> None:
    result = await get_districts_interactor()
    get_districts_interactor._district_gateway.get_districts.assert_awaited_once_with()
    assert (
        result == get_districts_interactor._district_gateway.get_districts.return_value
    )


@pytest.fixture
def get_district_by_region_id() -> GetDistrictsByRegionIdInteractor:
    ds_gateway = create_autospec(DistrictReader)
    return GetDistrictsByRegionIdInteractor(ds_gateway)


@pytest.mark.parametrize('region_id', [uuid.uuid4(), uuid.uuid4()])
async def test_get_district_by_region_id(
    get_district_by_region_id: GetDistrictsByRegionIdInteractor, region_id: uuid.UUID
):
    result = await get_district_by_region_id(region_id=region_id)
    get_district_by_region_id._district_gateway.get_districts_by_region_uuid.assert_awaited_once_with(
        region_id=region_id
    )
    assert (
        result
        == get_district_by_region_id._district_gateway.get_districts_by_region_uuid.return_value
    )


@pytest.fixture
def get_district_by_uuid() -> GetDistrictByIdInteractor:
    district_gateway = create_autospec(DistrictReader)
    return GetDistrictByIdInteractor(district_gateway)


@pytest.mark.parametrize('district_id', [uuid.uuid4(), uuid.uuid4()])
async def test_get_district_by_uuid(
    get_district_by_uuid: GetDistrictByIdInteractor, district_id: uuid.UUID
):
    result = await get_district_by_uuid(district_id=district_id)
    get_district_by_uuid._district_gateway.get_by_uuid.assert_awaited_once_with(
        district_id=district_id
    )
    assert result == get_district_by_uuid._district_gateway.get_by_uuid.return_value


@pytest.fixture
def create_district(faker: Faker) -> CreateDistrictInteractor:
    district_gateway = create_autospec(DistrictSaver)
    region_gateway = create_autospec(RegionReader)
    uuid_generator = MagicMock(return_value=faker.uuid4())
    return CreateDistrictInteractor(district_gateway, region_gateway, uuid_generator)


async def test_create_district_success(
    create_district: CreateDistrictInteractor, faker: Faker
) -> None:
    region_id = create_district._uuid_generator()
    dto = NewDistrictDTO(name=f'test_district_{uuid.uuid4()}', region_id=region_id)

    create_district._region_gateway.get_by_uuid = AsyncMock(return_value=MagicMock())

    result = await create_district(dto)

    expected_district = DistrictDM(id=result, region_id=dto.region_id, name=dto.name)
    create_district._district_gateway.save.assert_awaited_once_with(expected_district)
    create_district._region_gateway.get_by_uuid.assert_awaited_once_with(region_id)

    assert isinstance(result, str)
    assert result == region_id


async def test_create_district_region_not_exists(
    create_district: CreateDistrictInteractor, faker: Faker
) -> None:
    dto = NewDistrictDTO(name=f'test_district_{uuid.uuid4()}', region_id=uuid.uuid4())

    create_district._region_gateway.get_by_uuid = AsyncMock(return_value=None)

    with pytest.raises(EntityNotExistsError):
        await create_district(dto)

    create_district._district_gateway.save.assert_not_awaited()


@pytest.fixture
def delete_district() -> DeleteDistrictInteractor:
    district_gateway = create_autospec(DistrictDeleter)
    return DeleteDistrictInteractor(district_gateway)


@pytest.mark.parametrize('district_id', [uuid.uuid4(), uuid.uuid4()])
async def test_delete_district(
    delete_district: DeleteDistrictInteractor, district_id: uuid.UUID
):
    result = await delete_district(district_id=district_id)
    delete_district._district_gateway.delete_by_uuid.assert_awaited_once_with(
        district_id=district_id
    )
    assert result is None
