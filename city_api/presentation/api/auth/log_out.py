from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from city_api.application.errors import EntityNotExistsError
from city_api.infrastructure.auth.exception import UserLoggedOutError
from city_api.infrastructure.auth.handler.log_out import LogOutHandler

log_out_router = APIRouter(prefix='/auth', tags=['logout'])


@log_out_router.post('/logout', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    log_out_handler: FromDishka[LogOutHandler],
) -> None:
    try:
        await log_out_handler()
    except UserLoggedOutError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
