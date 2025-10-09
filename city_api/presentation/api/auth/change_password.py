from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from city_api.infrastructure.auth.exception import (
    AuthenticationChangeError,
    UserLoggedOutError,
    WrongPasswordError,
)
from city_api.infrastructure.auth.handler.change_password import (
    ChangePasswordHandler,
    ChangePasswordRequest,
)

change_password_router = APIRouter(prefix='/auth', tags=['change_password'])


@change_password_router.post('/change_password', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def change_password(
    change_password_handler: FromDishka[ChangePasswordHandler],
    request: ChangePasswordRequest,
) -> None:
    try:
        await change_password_handler(request)
    except (AuthenticationChangeError, WrongPasswordError, UserLoggedOutError) as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
