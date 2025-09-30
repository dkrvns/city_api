from dataclasses import dataclass

from app.application.errors import EntityNotExistsError
from app.application.interface.user.user import UserReader
from app.domain.services.user import UserService
from app.infrastructure.auth.session.auth_session_transport import AuthTransport


@dataclass(frozen=True, slots=True, kw_only=True)
class LogOutRequest:
    email: str


class LogOutHandler:
    def __init__(
        self,
        user_service: UserService,
        user_reader: UserReader,
        jwt_auth_transport: AuthTransport,
    ) -> None:
        self._user_service = user_service
        self._user_reader = user_reader
        self._jwt_auth_transport = jwt_auth_transport

    async def __call__(self, request_data: LogOutRequest):  # -> TokenPair
        user = await self._user_reader.read_by_email(request_data.email)

        if not self._user_reader.user_exist(user):
            raise EntityNotExistsError("User with this login or email doesn't exist")

        await self._jwt_auth_transport.remove_current()

        # if not await self._refresh_token_reader.get_by_username(user.email):
        #     raise UserAlreadyLoggedOutError("You're already logged out")
        #
        # await self._refresh_token_deleter.delete(request_data.refresh_token)

        """
        TODO
        продолжение туду из логина
        """
