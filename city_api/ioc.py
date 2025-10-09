from collections.abc import AsyncGenerator
from uuid import uuid4

from dishka import AnyOf, Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.requests import Request

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
from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.user.user import (
    UserDeleter,
    UserReader,
    UserSaver,
    UserUpdater,
)
from city_api.application.interface.uuid_generator import UUIDGenerator
from city_api.config import AuthSettings, Config
from city_api.domain.ports.jwt_encoder import JwtAccessTokenEncoder
from city_api.domain.ports.password_hasher import PasswordHasher
from city_api.domain.services.user import UserService
from city_api.infrastructure.auth.adapter.jwt_access_token_jose import (
    JWTAccessTokenJose,
)
from city_api.infrastructure.auth.adapter.password_hasher_bcrypt import (
    BcryptPasswordHasher,
)
from city_api.infrastructure.auth.gateway.refresh_token import RefreshTokenGateway
from city_api.infrastructure.auth.handler.change_password import ChangePasswordHandler
from city_api.infrastructure.auth.handler.log_in import LogInHandler
from city_api.infrastructure.auth.handler.log_out import LogOutHandler
from city_api.infrastructure.auth.handler.sign_up import SignUpHandler
from city_api.infrastructure.auth.handler.token_handler import TokenHandler
from city_api.infrastructure.auth.interface.auth_gateway import (
    RefreshTokenDeleter,
    RefreshTokenReader,
    RefreshTokenSaver,
)
from city_api.infrastructure.auth.session.auth_session_transport import AuthTransport
from city_api.infrastructure.db.gateway.city import CityGateway
from city_api.infrastructure.db.gateway.district import DistrictGateway
from city_api.infrastructure.db.gateway.region import RegionGateway
from city_api.infrastructure.db.gateway.user import UserGateway
from city_api.infrastructure.db.main import new_session_maker
from city_api.infrastructure.db.transaction_manager import SqlAlchemyTransactionManager
from city_api.infrastructure.grpc.region.region_pb2_grpc import RegionService
from city_api.presentation.auth.adapters.jwt_cookie_auth_transport import (
    JWTCookieAuthTransport,
)
from city_api.presentation.auth.cookie import CookieParams


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return uuid4

    @provide(scope=Scope.APP)
    def get_session_maker(self, config: Config) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(config.postgres)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_maker: async_sessionmaker[AsyncSession]
    ) -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    transaction_manager = provide(
        SqlAlchemyTransactionManager, scope=Scope.REQUEST, provides=TransactionManager
    )

    # region
    region_gateway = provide(
        RegionGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RegionSaver, RegionReader, RegionDeleter],
    )

    get_region_interactor = provide(GetRegionByIdInteractor, scope=Scope.REQUEST)
    get_regions_interactor = provide(GetRegionsInteractor, scope=Scope.REQUEST)
    create_region_interactor = provide(CreateRegionCommand, scope=Scope.REQUEST)
    delete_region_interactor = provide(DeleteRegionInteractor, scope=Scope.REQUEST)

    region_grpc_service = provide(RegionService, scope=Scope.REQUEST)

    # district
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

    # city
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

    # auth
    @provide(scope=Scope.APP)
    def provide_jwt_config(self, config: Config) -> AuthSettings:
        return config.auth_settings

    @provide(scope=Scope.APP)
    def provide_cookie_config(self) -> CookieParams:
        return CookieParams(secure=False)

    user_gateway = provide(
        UserGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[UserSaver, UserReader, UserDeleter, UserUpdater],
    )

    refresh_token_gateway = provide(
        RefreshTokenGateway,
        scope=Scope.REQUEST,
        provides=AnyOf[RefreshTokenReader, RefreshTokenSaver, RefreshTokenDeleter],
    )

    jwt_access_token_encoder = provide(
        JWTAccessTokenJose, scope=Scope.APP, provides=JwtAccessTokenEncoder
    )

    jwt_cookie_auth_transport = provide(
        JWTCookieAuthTransport, scope=Scope.REQUEST, provides=AuthTransport
    )

    password_hasher = provide(
        BcryptPasswordHasher, scope=Scope.REQUEST, provides=PasswordHasher
    )

    user_service = provide(UserService, scope=Scope.REQUEST)

    request = from_context(scope=Scope.REQUEST, provides=Request)

    log_in_handler = provide(LogInHandler, scope=Scope.REQUEST)
    log_out_handler = provide(LogOutHandler, scope=Scope.REQUEST)
    sign_up_handler = provide(SignUpHandler, scope=Scope.REQUEST)
    change_password_handler = provide(ChangePasswordHandler, scope=Scope.REQUEST)
    token_handler = provide(TokenHandler, scope=Scope.REQUEST)
