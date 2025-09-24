import uuid
from unittest.mock import AsyncMock, MagicMock, create_autospec
from uuid import uuid4

import pytest
from faker import Faker

from app.application.dto.region import NewRegionDTO
from app.application.interactors.region import (
    CreateRegionInteractor,
    DeleteRegionInteractor,
    GetRegionByIdInteractor,
    GetRegionsInteractor,
)
from app.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
    RegionSaver,
)
from app.domain.entities.region import RegionDM

pytestmark = pytest.mark.asyncio


@pytest.fixture
def get_regions_interactor() -> GetRegionsInteractor:
    region_gateway = create_autospec(RegionReader)
    return GetRegionsInteractor(region_gateway)


async def test_get_regions(get_regions_interactor: GetRegionsInteractor) -> None:
    result = await get_regions_interactor()
    get_regions_interactor._region_gateway.get_regions.assert_awaited_once_with()
    assert result == get_regions_interactor._region_gateway.get_regions.return_value


@pytest.fixture
def get_region_by_uuid() -> GetRegionByIdInteractor:
    region_gateway = create_autospec(RegionReader)
    return GetRegionByIdInteractor(region_gateway)


@pytest.mark.parametrize('region_id', [uuid.uuid4(), uuid.uuid4()])
async def test_get_region_by_uuid(
    get_region_by_uuid: GetRegionByIdInteractor, region_id: uuid.UUID
):
    result = await get_region_by_uuid(region_id=region_id)
    get_region_by_uuid._region_gateway.get_by_uuid.assert_awaited_once_with(
        region_id=region_id
    )
    assert result == get_region_by_uuid._region_gateway.get_by_uuid.return_value


@pytest.fixture
def create_region(faker: Faker) -> CreateRegionInteractor:
    region_gateway = create_autospec(RegionSaver)
    uuid_generator = MagicMock(return_value=faker.uuid4())
    return CreateRegionInteractor(region_gateway, uuid_generator)


async def test_create_region(
    create_region: CreateRegionInteractor, faker: Faker
) -> None:
    dto = NewRegionDTO(name=f'test_{uuid4()}', capital=faker.pystr())

    create_region._region_gateway.exist_with_name = AsyncMock(return_value=False)

    result = await create_region(dto)

    uuid = create_region._uuid_generator()

    create_region._region_gateway.save.assert_awaited_with(
        RegionDM(id=uuid, name=dto.name, capital=dto.capital)
    )

    assert result == uuid


async def test_create_same_regions(
    create_region: CreateRegionInteractor, faker: Faker
) -> None:
    dto = NewRegionDTO(name=faker.pystr(), capital=faker.pystr())

    create_region._region_gateway.exist_with_name = AsyncMock(return_value=False)

    result = await create_region(dto)

    uuid = create_region._uuid_generator()

    create_region._region_gateway.save.assert_awaited_with(
        RegionDM(id=uuid, name=dto.name, capital=dto.capital)
    )

    assert result == uuid


@pytest.fixture
def delete_region() -> DeleteRegionInteractor:
    region_gateway = create_autospec(RegionDeleter)
    return DeleteRegionInteractor(region_gateway)


@pytest.mark.parametrize('region_id', [uuid.uuid4(), uuid.uuid4()])
async def test_delete_region(
    delete_region: DeleteRegionInteractor, region_id: uuid.UUID
):
    result = await delete_region(region_id=region_id)
    delete_region._region_gateway.delete_by_uuid.assert_awaited_once_with(
        region_id=region_id
    )
    assert result is None
