from asyncpg import Record

from branchtalk_api.domain.entities.comments import Comment


class CommentDataMapper:
    @staticmethod
    def record_to_entity(record: Record) -> Comment:
        return Comment(
            id=record['id'],
            content=record['content'],
            created_at=record['created_at'],
            updated_at=record['updated_at'],
            user_id=record['user_id'],
            post_id=record['post_id'],
            parent_comment_id=record['parent_comment_id'],
        )
