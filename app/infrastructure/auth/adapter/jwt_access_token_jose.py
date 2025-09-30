from datetime import timedelta

import jwt

from app.config import AuthSettings
from app.domain.entities.auth.jwt_payload import JwtPayload
from app.domain.entities.user import UserDM
from app.domain.ports.jwt_encoder import JwtAccessTokenEncoder


class JWTAccessTokenJose(JwtAccessTokenEncoder):
    def __init__(self, jwt_settings: AuthSettings):
        self._jwt_settings = jwt_settings

    async def encode(self, user: UserDM) -> str:
        access_token_payload = JwtPayload(
            token=user.email,
            expires_in=timedelta(
                minutes=self._jwt_settings.access_token_expire_minutes
            ).total_seconds(),
        )

        return jwt.encode(
            access_token_payload,
            key=self._jwt_settings.jwt_secret,
            algorithm=self._jwt_settings.jwt_algorithm,
        )

    async def decode(self, token: str) -> dict: ...
