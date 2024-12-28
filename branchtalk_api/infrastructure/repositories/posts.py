from asyncpg.pool import Pool

from branchtalk_api.application import interfaces
from branchtalk_api.domain.entities.posts import Post
from branchtalk_api.domain.exceptions.post import PostNotFoundById, PostNotFoundForUser
from branchtalk_api.infrastructure.data_mappers.post import PostDataMapper


class PostRepository(
    interfaces.PostReader,
    interfaces.PostSaver,
    interfaces.PostUpdater,
    interfaces.PostDeleter,
):
    def __init__(
        self,
        pool: Pool,
        mapper: PostDataMapper,
    ):
        self._pool = pool
        self._mapper = mapper

    async def get_by_id(self, post_id: int) -> Post:
        async with self._pool.acquire() as connection:
            query = 'SELECT id, content, user_id, created_at, updated_at FROM posts WHERE id = $1'
            result = await connection.fetchrow(query, post_id)
            if not result:
                raise PostNotFoundById(post_id)

            return self._mapper.record_to_entity(record=result)

    async def get_by_id_and_user_id(self, post_id: int, user_id: int) -> Post:
        async with self._pool.acquire() as connection:
            query = 'SELECT id, content, user_id, created_at, updated_at FROM posts WHERE id = $1 AND user_id = $2'
            result = await connection.fetchrow(query, post_id, user_id)
            if not result:
                raise PostNotFoundForUser(post_id, user_id)

            return self._mapper.record_to_entity(record=result)

    async def save(self, post: Post) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = 'INSERT INTO posts (content, user_id, created_at) VALUES ($1, $2, $3, $4)'
                await connection.execute(stmt, post.content, post.user_id, post.created_at, post.updated_at)

    async def update(self, post: Post) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = 'UPDATE posts set content, updated_at  = $1, $2 WHERE id = $3'
                await connection.execute(stmt, post.content, post.updated_at, post.id)

    async def delete(self, post: Post) -> None:
        async with self._pool.acquire() as connection:
            async with connection.transaction():
                stmt = 'DELETE FROM posts WHERE id = $1'
                await connection.execute(stmt, post.id)
