from collections.abc import Sequence
from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from starlette import status

from app.application.dto.city import NewCityDTO
from app.application.errors import EntityNotExistsError
from app.application.interactors.city import (
    CreateCityInteractor,
    DeleteCityInteractor,
    GetCitiesByDistrictIdInteractor,
    GetCitiesInteractor,
    GetCityByIdInteractor,
)
from app.presentation.schemas.city import City

city_router = APIRouter(prefix="/cities", tags=["cities"])


@city_router.get("/get_cities")
@inject
async def get_cities(
    interactor: FromDishka[GetCitiesInteractor],
) -> Sequence[City]:
    city_dms = await interactor()
    if not city_dms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cities not found"
        )

    return [
        City(
            id=city_dm.id,
            district_id=city_dm.district_id,
            name=city_dm.name,
            obj_type=city_dm.obj_type,
            population=city_dm.population,
        )
        for city_dm in city_dms
    ]


@city_router.get("/get_cities_by_district")
@inject
async def get_cities_by_district_id(
    interactor: FromDishka[GetCitiesByDistrictIdInteractor],
    district_id: UUID,
) -> Sequence[City]:
    city_dms = await interactor(district_id=district_id)
    if not city_dms:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cities not found for this district"
        )

    return [
        City(
            id=city_dm.id,
            district_id=city_dm.district_id,
            name=city_dm.name,
            obj_type=city_dm.obj_type,
            population=city_dm.population,
        )
        for city_dm in city_dms
    ]


@city_router.get("/get_city_by_id")
@inject
async def get_city_by_id(
    interactor: FromDishka[GetCityByIdInteractor],
    city_id: UUID,
) -> City:
    city_dm = await interactor(city_id=city_id)
    if not city_dm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return City(
        id=city_dm.id,
        district_id=city_dm.district_id,
        name=city_dm.name,
        obj_type=city_dm.obj_type,
        population=city_dm.population,
    )


@city_router.post("/create_city")
@inject
async def create_city(
    interactor: FromDishka[CreateCityInteractor],
    city_schema: NewCityDTO,
) -> UUID:
    try:
        city_id = await interactor(city_schema)
    except EntityNotExistsError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="District not found. Please check if this district exists"
        )
    return city_id


@city_router.delete("/delete_city")
@inject
async def delete_city(
    interactor: FromDishka[DeleteCityInteractor],
    city_id: UUID,
):
    await interactor(city_id=city_id)
