from asyncpg import Record

from branchtalk_api.domain.entities.posts import Post


class PostDataMapper:
    @staticmethod
    def record_to_entity(record: Record) -> Post:
        return Post(
            id=record['id'],
            content=record['content'],
            user_id=record['user_id'],
            created_at=record['created_at'],
            updated_at=record['updated_at'],
        )
