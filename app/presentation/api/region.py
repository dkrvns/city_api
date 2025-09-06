import uuid
from collections.abc import Sequence
from http import HTTPStatus

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from app.application.dto.region import NewRegionDTO
from app.application.errors import EntityAlreadyExistsError
from app.application.interactors.region import (
    CreateRegionInteractor,
    DeleteRegionInteractor,
    GetRegionByIdInteractor,
    GetRegionsInteractor,
)
from app.presentation.schemas.region import Region

region_router = APIRouter(
    prefix="/region",
)


@region_router.get('/get_regions')
@inject
async def get_regions(
    interactor: FromDishka[GetRegionsInteractor],
) -> Sequence[Region]:
    region_dms = await interactor()
    if not region_dms:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Regions not found"
        )

    return [Region(
        id=region_dm.id,
        name=region_dm.name,
        capital=region_dm.capital,
    ) for region_dm in region_dms]


@region_router.get('/get_by_id')
@inject
async def get_by_id(
    interactor: FromDishka[GetRegionByIdInteractor],
    region_id: uuid.UUID
) -> Region:
    region_dm = await interactor(region_id=region_id)
    if not region_dm:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Region not found"
        )

    return Region(
        id=region_dm.id,
        name=region_dm.name,
        capital=region_dm.capital,
    )


@region_router.post('/create_region')
@inject
async def create_region(
    interactor: FromDishka[CreateRegionInteractor],
    region_schema: NewRegionDTO
) -> uuid.UUID:
    try:
        region_uuid = await interactor(region_schema)
    except EntityAlreadyExistsError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=f"Region with name {region_schema.name} already exists"
        )
    return region_uuid


@region_router.delete('/delete_region')
@inject
async def delete_region(
        interactor: FromDishka[DeleteRegionInteractor],
        region_id: uuid.UUID
):
    await interactor(region_id=region_id)
