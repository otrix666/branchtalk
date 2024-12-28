from abc import abstractmethod
from typing import Protocol

from branchtalk_api.domain.entities.users import User


class UserReader(Protocol):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_username(self, username: str) -> User:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError
