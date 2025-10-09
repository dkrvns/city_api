from fastapi import HTTPException
from starlette import status

from city_api.infrastructure.auth.exception import JWTTokenError
from city_api.infrastructure.auth.session.auth_session_transport import AuthTransport


class TokenHandler:
    def __init__(self, jwt_auth_transport: AuthTransport):
        self._jwt_auth_transport = jwt_auth_transport

    async def __call__(self) -> None:
        try:
            await self._jwt_auth_transport.get_current_user_token_info()
        except JWTTokenError as e:
            await self._jwt_auth_transport.remove_current()
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
