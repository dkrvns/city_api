from dataclasses import dataclass

from app.application.interface.user.user import UserReader, UserSaver
from app.domain.entities.auth.raw_password import RawPassword
from app.domain.exception import UserAlreadyExistError
from app.domain.services.user import UserService


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
    ) -> None:
        self._user_service = user_service
        self._user_reader = user_reader
        self._user_saver = user_saver

    async def __call__(self, request_data: SignUpRequest) -> None:
        password = RawPassword(request_data.password)

        user = await self._user_service.create(request_data.email, password)

        if await self._user_reader.user_exist(user):
            raise UserAlreadyExistError('User with this login or email already exist')

        await self._user_saver.save(user)
