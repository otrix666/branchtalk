from abc import abstractmethod
from typing import Protocol

from branchtalk_api.domain.entities.users import User


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
