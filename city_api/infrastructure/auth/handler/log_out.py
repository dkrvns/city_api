from city_api.application.interface.user.user import UserReader
from city_api.domain.services.user import UserService
from city_api.infrastructure.auth.exception import UserLoggedOutError
from city_api.infrastructure.auth.session.auth_session_transport import AuthTransport


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

    async def __call__(self):  # -> TokenPair
        if not await self._jwt_auth_transport.get_current_user_token_info():
            raise UserLoggedOutError('User already logged out')

        await self._jwt_auth_transport.remove_current()
