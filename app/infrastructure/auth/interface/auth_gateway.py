from abc import abstractmethod
from typing import Protocol

from app.domain.entities.auth.refresh_token import RefreshTokenDM


class RefreshTokenSaver(Protocol):
    @abstractmethod
    async def save(self, refresh_token: RefreshTokenDM) -> None: ...


class RefreshTokenReader(Protocol):
    @abstractmethod
    async def get_by_username(self, username: str) -> RefreshTokenDM | None: ...


class RefreshTokenDeleter(Protocol):
    @abstractmethod
    async def delete(self, token: str) -> None: ...
