import uuid
from abc import abstractmethod
from typing import Protocol

from city_api.domain.entities.user import UserDM


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: UserDM) -> uuid.UUID: ...


class UserReader(Protocol):
    @abstractmethod
    async def read_by_email(self, email: str) -> UserDM: ...

    @abstractmethod
    async def user_exist(self, user: UserDM) -> bool: ...


class UserDeleter(Protocol):
    @abstractmethod
    async def delete(self, user: UserDM) -> None: ...


class UserUpdater(Protocol):
    @abstractmethod
    async def update(self, user: UserDM) -> None: ...
