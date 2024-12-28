from typing import Protocol

from branchtalk_api.application import interfaces
from branchtalk_api.application.dto.post import CreatePostDTO, DeletePostDTO, UpdatePostDTO
from branchtalk_api.domain.entities.posts import Post


class CreatePostInteractor:
    def __int__(
        self,
        post_saver: interfaces.PostSaver,
    ):
        self._post_saver = post_saver

    async def __call__(self, data: CreatePostDTO) -> None:
        post = Post(
            id=None,
            content=data.content,
            user_id=data.user_id,
            created_at=data.created_at,
            updated_at=data.updated_at,
        )
        await self._post_saver.save(post=post)


class PostUpdateManager(interfaces.PostReader, interfaces.PostUpdater, Protocol): ...


class UpdatePostInteractor:
    def __init__(
        self,
        update_manager: PostUpdateManager,
    ):
        self._update_manager = update_manager

    async def __call__(self, data: UpdatePostDTO) -> None:
        post = await self._update_manager.get_by_id_and_user_id(post_id=data.post_id, user_id=data.user_id)
        post.content = data.content

        await self._update_manager.update(post=post)


class PostDeleteManager(interfaces.PostReader, interfaces.PostDeleter, Protocol): ...


class DeletePostInteractor:
    def __init__(
        self,
        delete_manager: PostDeleteManager,
    ):
        self._delete_manager = delete_manager

    async def __call__(self, data: DeletePostDTO) -> None:
        post = await self._delete_manager.get_by_id_and_user_id(post_id=data.post_id, user_id=data.user_id)
        await self._delete_manager.delete(post=post)
