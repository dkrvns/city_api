from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.domain.exception import UserAlreadyExistError
from app.infrastructure.auth.handler.sign_up import SignUpHandler, SignUpRequest

sign_up_router = APIRouter(prefix='/auth', tags=['signup'])


class SignUpResponse(BaseModel):
    id: str


@sign_up_router.post('/signup')
@inject
async def signup(
    sign_up_handler: FromDishka[SignUpHandler],
    request: SignUpRequest,
) -> SignUpResponse:
    try:
        user_id = await sign_up_handler(request)
    except UserAlreadyExistError as e:
        raise HTTPException(status_code=403, detail=str(e))

    return SignUpResponse(id=str(user_id))
