# application/city.py
from dishka import AnyOf, Provider, Scope, provide

from city_api.application.commands.city import CreateCityCommand, UpdateCityCommand
from city_api.application.commands.district import CreateDistrictCommand
from city_api.application.commands.region import CreateRegionCommand
from city_api.application.interactors.city import (
    DeleteCityInteractor,
    GetCitiesByDistrictIdInteractor,
    GetCitiesInteractor,
    GetCityByIdInteractor,
)
from city_api.application.interactors.district import (
    DeleteDistrictInteractor,
    GetDistrictByIdInteractor,
    GetDistrictsByRegionIdInteractor,
    GetDistrictsInteractor,
)
from city_api.application.interactors.region import (
    DeleteRegionInteractor,
    GetRegionByIdInteractor,
    GetRegionsInteractor,
)
from city_api.application.interface.city.city import (
    CityDeleter,
    CityReader,
    CitySaver,
    CityUpdater,
)
from city_api.application.interface.district.district import (
    DistrictDeleter,
    DistrictReader,
    DistrictSaver,
)
from city_api.application.interface.region.region import (
    RegionDeleter,
    RegionReader,
    RegionSaver,
)
from city_api.infrastructure.db.gateway.city import CityGateway
from city_api.infrastructure.db.gateway.district import DistrictGateway
from city_api.infrastructure.db.gateway.region import RegionGateway


class CityProvider(Provider):
    city_gateway = provide(
        CityGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[CitySaver, CityReader, CityDeleter, CityUpdater],
    )
    get_cities_interactor = provide(GetCitiesInteractor, scope=Scope.REQUEST)
    get_cities_by_district_id_interactor = provide(
        GetCitiesByDistrictIdInteractor, scope=Scope.REQUEST
    )
    get_city_by_id_interactor = provide(GetCityByIdInteractor, scope=Scope.REQUEST)
    create_city_interactor = provide(CreateCityCommand, scope=Scope.REQUEST)
    delete_city_interactor = provide(DeleteCityInteractor, scope=Scope.REQUEST)
    update_city_interactor = provide(UpdateCityCommand, scope=Scope.REQUEST)


class DistrictProvider(Provider):
    district_gateway = provide(
        DistrictGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[DistrictSaver, DistrictReader, DistrictDeleter],
    )

    get_districts_interactor = provide(GetDistrictsInteractor, scope=Scope.REQUEST)
    get_districts_by_region_id_interactor = provide(
        GetDistrictsByRegionIdInteractor, scope=Scope.REQUEST
    )
    get_district_by_id_interactor = provide(
        GetDistrictByIdInteractor, scope=Scope.REQUEST
    )
    create_district_interactor = provide(CreateDistrictCommand, scope=Scope.REQUEST)
    delete_district_interactor = provide(DeleteDistrictInteractor, scope=Scope.REQUEST)


class RegionProvider(Provider):
    region_gateway = provide(
        RegionGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RegionSaver, RegionReader, RegionDeleter],
    )

    get_region_interactor = provide(GetRegionByIdInteractor, scope=Scope.REQUEST)
    get_regions_interactor = provide(GetRegionsInteractor, scope=Scope.REQUEST)
    create_region_interactor = provide(CreateRegionCommand, scope=Scope.REQUEST)
    delete_region_interactor = provide(DeleteRegionInteractor, scope=Scope.REQUEST)
