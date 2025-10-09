from dataclasses import dataclass

from city_api.application.interface.transaction_manager import TransactionManager
from city_api.application.interface.user.user import UserReader, UserSaver
from city_api.domain.entities.auth.raw_password import RawPassword
from city_api.domain.exception import UserAlreadyExistError
from city_api.domain.services.user import UserService


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpRequest:
    email: str
    password: str


class SignUpHandler:
    def __init__(
        self,
        user_service: UserService,
        user_reader: UserReader,
        user_saver: UserSaver,
        transaction_manager: TransactionManager,
    ) -> None:
        self._user_service = user_service
        self._user_reader = user_reader
        self._user_saver = user_saver
        self._transaction_manager = transaction_manager

    async def __call__(self, request_data: SignUpRequest) -> None:
        password = RawPassword(request_data.password)

        user = await self._user_service.create(request_data.email, password)

        if await self._user_reader.user_exist(user):
            raise UserAlreadyExistError('User with this login or email already exist')

        await self._user_saver.save(user)
        await self._transaction_manager.commit()
