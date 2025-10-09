from city_api.application.interface.uuid_generator import UUIDGenerator
from city_api.domain.entities.auth.raw_password import RawPassword
from city_api.domain.entities.user import UserDM
from city_api.domain.ports.password_hasher import PasswordHasher


class UserService:
    def __init__(self, uuid_generator: UUIDGenerator, password_hasher: PasswordHasher):
        self._uuid_generator = uuid_generator
        self._password_hasher = password_hasher

    async def create(self, email: str, raw_password: RawPassword) -> UserDM:
        hashed_password = self._password_hasher.hash(raw_password)

        return UserDM(
            id=self._uuid_generator(),
            email=email,
            hashed_password=hashed_password,
        )

    async def change_password(self, user: UserDM, raw_password: RawPassword) -> UserDM:
        hashed_password = self._password_hasher.hash(raw_password)

        return UserDM(
            id=user.id,
            email=user.email,
            hashed_password=hashed_password,
        )

    async def is_password_valid(self, user: UserDM, raw_password: RawPassword) -> bool:
        return self._password_hasher.verify(raw_password, user.hashed_password)
