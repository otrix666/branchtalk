from abc import abstractmethod
from typing import Protocol

from branchtalk_api.domain.entities.comments import Comment


class CommentReader(Protocol):
    @abstractmethod
    async def get_by_id(self, comment_id: int) -> Comment:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id_and_user_id(self, comment_id: int, user_id: int) -> Comment:
        raise NotImplementedError


class CommentSaver(Protocol):
    @abstractmethod
    async def save(self, comment: Comment) -> None:
        raise NotImplementedError


class CommentUpdater(Protocol):
    @abstractmethod
    async def update(self, comment: Comment) -> None:
        raise NotImplementedError


class CommentDeleter(Protocol):
    @abstractmethod
    async def delete(self, comment: Comment) -> None:
        raise NotImplementedError
