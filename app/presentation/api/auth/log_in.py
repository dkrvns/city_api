from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from app.application.errors import EntityNotExistsError
from app.infrastructure.auth.error import UserAlreadyLoggedInError, WrongPasswordError
from app.infrastructure.auth.handler.log_in import LogInHandler, LoginInRequest

log_in_router = APIRouter(prefix='/auth', tags=['login'])


@log_in_router.post('/login', status_code=status.HTTP_204_NO_CONTENT)
@inject
async def login(
    log_in_handler: FromDishka[LogInHandler],
    request: LoginInRequest,
) -> None:
    try:
        await log_in_handler(request)
    except EntityNotExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UserAlreadyLoggedInError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except WrongPasswordError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
