from dataclasses import dataclass

from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.user.user import UserReader, UserUpdater
from city_api.domain.entities.auth.raw_password import RawPassword
from city_api.domain.services.user import UserService
from city_api.infrastructure.auth.exception import (
    AuthenticationChangeError,
    UserLoggedOutError,
    WrongPasswordError,
)
from city_api.infrastructure.auth.session.auth_session_transport import AuthTransport


@dataclass
class ChangePasswordRequest:
    email: str
    current_password: str
    new_password: str


class ChangePasswordHandler:
    def __init__(
        self,
        user_service: UserService,
        transaction_manager: TransactionManager,
        user_reader: UserReader,
        user_updater: UserUpdater,
        jwt_auth_transport: AuthTransport,
    ):
        self._user_service = user_service
        self._transaction_manager = transaction_manager
        self._user_reader = user_reader
        self._user_updater = user_updater
        self._jwt_auth_transport = jwt_auth_transport

    async def __call__(self, request_data: ChangePasswordRequest) -> None:
        current_password = RawPassword(request_data.current_password)
        new_password = RawPassword(request_data.new_password)

        current_user_token_info = (
            await self._jwt_auth_transport.get_current_user_token_info()
        )

        if not current_user_token_info:
            raise UserLoggedOutError("You're logged out")

        if current_password == new_password:
            raise AuthenticationChangeError(
                'New password must differ from current password'
            )

        current_user = await self._user_reader.read_by_email(
            current_user_token_info.get('token')
        )

        if not await self._user_service.is_password_valid(
            current_user, current_password
        ):
            raise WrongPasswordError('Wrong password')

        new_user = await self._user_service.change_password(current_user, new_password)

        await self._user_updater.update(new_user)
        await self._transaction_manager.commit()
