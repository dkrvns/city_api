from collections.abc import Sequence
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from app.application.dto.district import NewDistrictDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.district import (
    CreateDistrictInteractor,
    DeleteDistrictInteractor,
    GetDistrictByIdInteractor,
    GetDistrictsByRegionIdInteractor,
    GetDistrictsInteractor,
)
from app.presentation.schemas.district import District

district_router = APIRouter(prefix="/districts", tags=["districts"])


@district_router.get("/get_districts")
@inject
async def get_districts(
    interactor: FromDishka[GetDistrictsInteractor],
) -> Sequence[District]:
    district_dms = await interactor()
    if not district_dms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Districts not found"
        )

    return [
        District(
            id=district_dm.id,
            region_id=district_dm.region_id,
            name=district_dm.name,
        )
        for district_dm in district_dms
    ]


@district_router.get("/get_districts_by_region")
@inject
async def get_districts_by_region_id(
    interactor: FromDishka[GetDistrictsByRegionIdInteractor],
    region_id: UUID,
) -> Sequence[District]:
    district_dms = await interactor(region_id=region_id)
    if not district_dms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )

    return [
        District(
            id=district_dm.id,
            region_id=district_dm.region_id,
            name=district_dm.name,
        )
        for district_dm in district_dms
    ]


@district_router.get("/get_district_by_id")
@inject
async def get_district_by_id(
    interactor: FromDishka[GetDistrictByIdInteractor],
    district_id: UUID,
) -> District:
    district_dm = await interactor(district_id=district_id)
    if not district_dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found"
        )

    return District(
        id=district_dm.id,
        region_id=district_dm.region_id,
        name=district_dm.name,
    )


@district_router.post("/create_district")
@inject
async def create_district(
    interactor: FromDishka[CreateDistrictInteractor],
    district_schema: NewDistrictDTO,
) -> UUID:
    try:
        district_id = await interactor(district_schema)
    except EntityNotExistsError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Region not found. Please check if this region exists or create it"
        )
    return district_id


@district_router.delete("/delete_district")
@inject
async def delete_district(
    interactor: FromDishka[DeleteDistrictInteractor],
    district_id: UUID,
):
    await interactor(district_id=district_id)
