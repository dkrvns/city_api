from abc import abstractmethod
from typing import Protocol

from city_api.domain.entities.user import UserDM


class JwtAccessTokenEncoder(Protocol):
    @abstractmethod
    async def encode(self, user: UserDM) -> str:
        pass

    @abstractmethod
    async def decode(self, token: str) -> dict:
        pass
