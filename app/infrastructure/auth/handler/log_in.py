from dataclasses import dataclass

from app.application.errors import EntityNotExistsError
from app.application.interface.user.user import UserReader
from app.domain.entities.auth.raw_password import RawPassword
from app.domain.services.user import UserService
from app.infrastructure.auth.error import WrongPasswordError
from app.infrastructure.auth.session.auth_session_transport import AuthTransport


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginInRequest:
    email: str
    password: str


class LogInHandler:
    def __init__(
        self,
        user_service: UserService,
        user_reader: UserReader,
        jwt_auth_transport: AuthTransport,
    ) -> None:
        self._user_service = user_service
        self._user_reader = user_reader
        self._jwt_auth_transport = jwt_auth_transport

    async def __call__(self, request_data: LoginInRequest) -> None:
        password = RawPassword(request_data.password)

        current_user = await self._user_service.create(request_data.email, password)

        if not await self._user_reader.user_exist(current_user):
            raise EntityNotExistsError("User with this login or email doesn't exist")

        # if await self._refresh_token_reader.get_by_username(current_user.email):
        #     raise UserAlreadyLoggedInError("You're already logged in")

        user = await self._user_reader.read_by_email(current_user.email)

        if not await self._user_service.is_password_valid(user, password):
            raise WrongPasswordError('Wrong password')

        await self._jwt_auth_transport.deliver(current_user)

        """
        TODO
        положить рефреш токен в редис и проверять его наличие есть access истек
        """
