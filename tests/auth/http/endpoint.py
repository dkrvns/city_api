from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security

from city_api.presentation.auth.fastapi_marker import cookie_scheme
from city_api.presentation.auth.verify_user import verify_token

test_router = APIRouter(
    prefix='/test_end',
    dependencies=[Security(cookie_scheme), Security(verify_token)],
)


@test_router.get('/test_security')
@inject
async def test_security() -> dict:
    return {'200': 'OK'}
