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


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, raw_password: str) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def verify(self, raw_password: str, hashed_password: str) -> bool:
        raise NotImplementedError


class JwtService(Protocol):
    @abstractmethod
    def create_jwt(self, payload: dict, expiration_time: int, token_type: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def create_refresh_token(self, user: User) -> str:
        raise NotImplementedError

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        raise NotImplementedError
