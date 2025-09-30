from abc import abstractmethod
from typing import Protocol

from app.domain.entities.user import UserDM


class AuthTransport(Protocol):
    @abstractmethod
    async def deliver(self, user: UserDM) -> None: ...

    @abstractmethod
    async def remove_current(self) -> None: ...
