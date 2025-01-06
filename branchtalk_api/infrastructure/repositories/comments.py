from asyncpg.pool import Pool

from branchtalk_api.application import interfaces
from branchtalk_api.domain.entities.comments import Comment
from branchtalk_api.domain.exceptions.comment import CommentNotFoundById, CommentNotFoundForUser
from branchtalk_api.infrastructure.data_mappers.comment import CommentDataMapper


class CommentsRepository(
    interfaces.CommentSaver,
    interfaces.CommentReader,
    interfaces.CommentUpdater,
    interfaces.CommentDeleter,
):
    def __init__(
        self,
        pool: Pool,
        mapper: CommentDataMapper,
    ):
        self._pool = pool
        self._mapper = mapper

    async def get_by_id(self, comment_id: int) -> Comment:
        async with self._pool.acquire() as connection:
            query = (
                'SELECT id, content, created_at, updated_at, user_id, post_id, parent_comment_id '
                'FROM comments WHERE id = $1'
            )
            result = await connection.fetch(query, comment_id)
            if not result:
                raise CommentNotFoundById(comment_id)

            return self._mapper.record_to_entity(record=result)

    async def get_by_id_and_user_id(self, comment_id: int, user_id: int) -> Comment:
        async with self._pool.acquire() as connection:
            query = (
                'SELECT id, content, created_at, updated_at, user_id, post_id, parent_comment_id '
                'FROM comments WHERE id = $1 AND user_id = $2'
            )
            result = await connection.fetch(query, comment_id, user_id)
            if not result:
                raise CommentNotFoundForUser(comment_id, user_id)

            return self._mapper.record_to_entity(record=result)

    async def save(self, comment: Comment) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = (
                    'INSERT INTO comments'
                    '(content, created_at, user_id, post_id, parent_comment_id) VALUES($1, $2, $3, $4)'
                )
                await connection.execute(
                    stmt,
                    comment.content,
                    comment.created_at,
                    comment.user_id,
                    comment.post_id,
                    comment.parent_comment_id,
                )

    async def update(self, comment: Comment) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = 'UPDATE comments set content = $1 WHERE id = $2'
                await connection.execute(stmt, comment.content, comment.id)

    async def delete(self, comment: Comment) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = 'DELETE FROM comments WHERE id = $1'
                await connection.execute(stmt, comment.id)
