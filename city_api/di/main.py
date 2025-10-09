from dishka import Provider

from city_api.di.application.main import CityProvider, DistrictProvider, RegionProvider
from city_api.di.auth.main import AuthProvider
from city_api.di.infrastructure.main import CoreProvider, DatabaseProvider


def ioc_factory() -> list:
    containers = [
        CoreProvider(),
        DatabaseProvider(),
        AuthProvider(),
        CityProvider(),
        RegionProvider(),
        DistrictProvider(),
    ]
    return containers


# for testing
AppProvider: list[type[Provider]] = [
    CoreProvider,
    DatabaseProvider,
    AuthProvider,
    CityProvider,
    RegionProvider,
    DistrictProvider,
]
