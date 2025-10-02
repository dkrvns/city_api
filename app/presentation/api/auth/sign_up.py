from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, status

from app.domain.exception import UserAlreadyExistError
from app.infrastructure.auth.handler.sign_up import SignUpHandler, SignUpRequest

sign_up_router = APIRouter(prefix='/auth', tags=['signup'])


@sign_up_router.post('/signup', status_code=status.HTTP_201_CREATED)
@inject
async def signup(
    sign_up_handler: FromDishka[SignUpHandler],
    request: SignUpRequest,
) -> None:
    try:
        await sign_up_handler(request)
    except UserAlreadyExistError as e:
        raise HTTPException(status_code=403, detail=str(e))
