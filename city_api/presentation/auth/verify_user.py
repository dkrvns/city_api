from dishka.integrations.fastapi import FromDishka, inject

from city_api.infrastructure.auth.handler.token_handler import TokenHandler


@inject
async def verify_token(token_handler: FromDishka[TokenHandler]) -> None:
    await token_handler()
