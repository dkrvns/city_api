from http import HTTPStatus

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.application.errors import EntityNotExistsError
from app.infrastructure.auth.error import UserAlreadyLoggedInError, WrongPasswordError
from app.infrastructure.auth.handler.log_in import LogInHandler, LoginInRequest

log_in_router = APIRouter(prefix='/auth', tags=['login'])


class LogInResponse(BaseModel):
    access_token: str
    refresh_token: str


@log_in_router.post('/login')
@inject
async def login(
    log_in_handler: FromDishka[LogInHandler],
    request: LoginInRequest,
):
    try:
        await log_in_handler(request)
    except EntityNotExistsError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
    except UserAlreadyLoggedInError as e:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(e))
    except WrongPasswordError as e:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=str(e))
