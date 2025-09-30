from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from app.application.errors import EntityNotExistsError
from app.infrastructure.auth.error import UserAlreadyLoggedOutError
from app.infrastructure.auth.handler.log_out import LogOutHandler, LogOutRequest

log_out_router = APIRouter(prefix='/auth', tags=['logout'])


@log_out_router.post('/logout')
@inject
async def logout(
    log_out_handler: FromDishka[LogOutHandler],
    request: LogOutRequest,
) -> dict:
    try:
        await log_out_handler(request)
    except EntityNotExistsError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UserAlreadyLoggedOutError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return {'200': 'OK'}
