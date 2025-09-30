from starlette.requests import Request

from app.domain.entities.user import UserDM
from app.domain.ports.jwt_encoder import JwtAccessTokenEncoder
from app.infrastructure.auth.session.auth_session_transport import AuthTransport
from app.presentation.auth.cookie import CookieParams


class JWTCookieAuthTransport(AuthTransport):
    def __init__(
        self,
        request: Request,
        access_token_processor: JwtAccessTokenEncoder,
        cookie_params: CookieParams,
    ):
        self._request = request
        self._access_token_processor = access_token_processor
        self._cookie_params = cookie_params

    async def deliver(self, user: UserDM) -> None:
        access_token = await self._access_token_processor.encode(user)
        self._request.state.new_access_token = access_token
        self._request.state.cookie_params = self._cookie_params

    async def remove_current(self) -> None:
        self._request.state.delete_access_token = True
