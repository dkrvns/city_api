from collections.abc import AsyncGenerator

from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.interactors.city import (
    CreateCityInteractor,
    DeleteCityInteractor,
    GetCitiesByDistrictIdInteractor,
    GetCitiesInteractor,
    GetCityByIdInteractor,
    UpdateCityInteractor,
)
from app.application.interactors.district import (
    CreateDistrictInteractor,
    DeleteDistrictInteractor,
    GetDistrictByIdInteractor,
    GetDistrictsByRegionIdInteractor,
    GetDistrictsInteractor,
)
from app.application.interactors.region import (
    CreateRegionInteractor,
    DeleteRegionInteractor,
    GetRegionByIdInteractor,
    GetRegionsInteractor,
)
from app.application.interface.city.city import (
    CityDeleter,
    CityReader,
    CitySaver,
    CityUpdater,
)
from app.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
    DistrictSaver,
)
from app.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
    RegionSaver,
)
from app.config import Config
from app.infrastructure.db.main import new_session_maker
from app.infrastructure.gateway.city import CityGateway
from app.infrastructure.gateway.district import DistrictGateway
from app.infrastructure.gateway.region import RegionGateway
from app.infrastructure.grpc.region.region_pb2_grpc import RegionService


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    # region
    region_gateway = provide(
        RegionGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RegionSaver, RegionReader, RegionDeleter],
    )

    get_region_interactor = provide(GetRegionByIdInteractor, scope=Scope.REQUEST)
    get_regions_interactor = provide(GetRegionsInteractor, scope=Scope.REQUEST)
    create_region_interactor = provide(CreateRegionInteractor, scope=Scope.REQUEST)
    delete_region_interactor = provide(DeleteRegionInteractor, scope=Scope.REQUEST)

    region_grpc_service = provide(
        RegionService,
        scope=Scope.REQUEST
    )

    #district
    district_gateway = provide(
        DistrictGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DistrictSaver, DistrictReader, DistrictDeleter],
    )

    get_districts_interactor = provide(GetDistrictsInteractor, scope=Scope.REQUEST)
    get_districts_by_region_id_interactor = provide(GetDistrictsByRegionIdInteractor, scope=Scope.REQUEST)
    get_district_by_id_interactor = provide(GetDistrictByIdInteractor, scope=Scope.REQUEST)
    create_district_interactor = provide(CreateDistrictInteractor, scope=Scope.REQUEST)
    delete_district_interactor = provide(DeleteDistrictInteractor, scope=Scope.REQUEST)

    #city
    city_gateway = provide(
        CityGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[CitySaver, CityReader, CityDeleter, CityUpdater],
    )
    get_cities_interactor = provide(GetCitiesInteractor, scope=Scope.REQUEST)
    get_cities_by_district_id_interactor = provide(GetCitiesByDistrictIdInteractor, scope=Scope.REQUEST)
    get_city_by_id_interactor = provide(GetCityByIdInteractor, scope=Scope.REQUEST)
    create_city_interactor = provide(CreateCityInteractor, scope=Scope.REQUEST)
    delete_city_interactor = provide(DeleteCityInteractor, scope=Scope.REQUEST)
    update_city_interactor = provide(UpdateCityInteractor, scope=Scope.REQUEST)
