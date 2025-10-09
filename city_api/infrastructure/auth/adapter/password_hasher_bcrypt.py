import bcrypt

from city_api.domain.entities.auth.raw_password import RawPassword
from city_api.domain.ports.password_hasher import PasswordHasher


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, raw_password: RawPassword) -> bytes:
        salt: bytes = bcrypt.gensalt()

        return bcrypt.hashpw(raw_password.password.encode(), salt)

    def verify(self, raw_password: RawPassword, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(raw_password.password.encode(), hashed_password)
