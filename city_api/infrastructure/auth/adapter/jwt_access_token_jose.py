from datetime import datetime as dt
from datetime import timedelta

import jwt

from city_api.config import AuthSettings
from city_api.domain.entities.auth.jwt_payload import JwtPayload
from city_api.domain.entities.user import UserDM
from city_api.domain.ports.jwt_encoder import JwtAccessTokenEncoder
from city_api.infrastructure.auth.exception import JWTTokenError


class JWTAccessTokenJose(JwtAccessTokenEncoder):
    def __init__(self, jwt_settings: AuthSettings):
        self._jwt_settings = jwt_settings

    async def encode(self, user: UserDM) -> str:
        expires_in = (
            dt.now().timestamp()
            + timedelta(
                minutes=self._jwt_settings.access_token_expire_minutes
            ).total_seconds()
        )
        access_token_payload = JwtPayload(
            token=user.email,
            exp=expires_in,
        )

        return jwt.encode(
            access_token_payload,
            key=self._jwt_settings.jwt_secret,
            algorithm=self._jwt_settings.jwt_algorithm,
        )

    async def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                key=self._jwt_settings.jwt_secret,
                algorithms=self._jwt_settings.jwt_algorithm,
            )
        except jwt.PyJWTError as e:
            raise JWTTokenError(e)
