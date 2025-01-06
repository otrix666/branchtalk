from branchtalk_api.domain.exceptions.base import DomainError


class PostNotFoundById(DomainError):
    def __init__(self, post_id: int):
        super().__init__(f'Post with id {post_id} not found')


class PostNotFoundForUser(DomainError):
    def __init__(self, post_id, user_id: int):
        super().__init__(f'Post with id {post_id} not found for user {user_id}')
