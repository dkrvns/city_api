from dishka import AnyOf, Provider, Scope, from_context, provide
from starlette.requests import Request

from city_api.application.interface.user.user import (
    UserDeleter,
    UserReader,
    UserSaver,
    UserUpdater,
)
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
from city_api.infrastructure.db.gateway.user import UserGateway
from city_api.presentation.auth.adapters.jwt_cookie_auth_transport import (
    JWTCookieAuthTransport,
)
from city_api.presentation.auth.cookie import CookieParams


class AuthProvider(Provider):
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
