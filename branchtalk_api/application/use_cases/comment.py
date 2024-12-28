from typing import Protocol

from branchtalk_api.application import interfaces
from branchtalk_api.application.dto.comment import CreateCommentDTO, DeleteCommentDTO, UpdateCommentDTO
from branchtalk_api.domain.entities.comments import Comment


class CreateCommentInteractor:
    def __init__(
        self,
        comment_saver: interfaces.CommentSaver,
    ) -> None:
        self._comment_saver = comment_saver

    async def __call__(self, data: CreateCommentDTO) -> None:
        comment = Comment(
            id=None,
            content=data.content,
            created_at=data.created_at,
            updated_at=data.updated_at,
            user_id=data.user_id,
            post_id=data.post_id,
            parent_comment_id=data.parent_comment_id,
        )

        await self._comment_saver.save(comment=comment)


class CommentUpdateManager(interfaces.CommentReader, interfaces.CommentUpdater, Protocol): ...


class UpdateCommentInteractor:
    def __init__(
        self,
        update_manager: CommentUpdateManager,
    ):
        self._update_manager = update_manager

    async def __call__(self, data: UpdateCommentDTO) -> None:
        comment = await self._update_manager.get_by_id_and_user_id(comment_id=data.comment_id, user_id=data.user_id)
        comment.content = data.content

        await self._update_manager.update(comment=comment)


class CommentDeleteManager(interfaces.CommentReader, interfaces.CommentDeleter, Protocol): ...


class DeleteCommentInteractor:
    def __init__(
        self,
        delete_manager: CommentDeleteManager,
    ):
        self._delete_manager = delete_manager

    async def __call__(self, data: DeleteCommentDTO) -> None:
        comment = await self._delete_manager.get_by_id_and_user_id(comment_id=data.comment_id, user_id=data.comment_id)

        await self._delete_manager.delete(comment=comment)
