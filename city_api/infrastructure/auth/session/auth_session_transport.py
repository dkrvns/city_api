from abc import abstractmethod
from typing import Protocol

from city_api.domain.entities.user import UserDM


class AuthTransport(Protocol):
    @abstractmethod
    async def deliver(self, user: UserDM) -> None: ...

    @abstractmethod
    async def remove_current(self) -> None: ...

    @abstractmethod
    async def get_current_user_token_info(self) -> dict | None: ...
