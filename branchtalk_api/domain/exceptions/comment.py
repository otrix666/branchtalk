from branchtalk_api.domain.exceptions.base import DomainError


class CommentNotFoundById(DomainError):
    def __init__(self, comment_id: int):
        super().__init__(f'Comment with id {comment_id} does not exist')


class CommentNotFoundForUser(DomainError):
    def __init__(self, post_id, user_id: int):
        super().__init__(f'Comment with id {post_id} not found for user {user_id}')
