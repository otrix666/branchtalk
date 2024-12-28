from abc import abstractmethod
from typing import Protocol

from branchtalk_api.domain.entities.posts import Post


class PostReader(Protocol):
    @abstractmethod
    async def get_by_id(self, post_id: int) -> Post:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_and_user_id(self, post_id: int, user_id: int) -> Post:
        raise NotImplementedError


class PostSaver(Protocol):
    @abstractmethod
    async def save(self, post: Post) -> None:
        raise NotImplementedError


class PostUpdater(Protocol):
    @abstractmethod
    async def update(self, post: Post) -> None:
        raise NotImplementedError


class PostDeleter(Protocol):
    @abstractmethod
    async def delete(self, post: Post) -> None:
        raise NotImplementedError
