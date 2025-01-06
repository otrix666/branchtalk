from branchtalk_api.domain.exceptions.base import DomainError


class UsernameAlreadyExists(DomainError):
    def __init__(self, username: str):
        super().__init__(f'User with username {username} already exists')


class EmailAlreadyExists(DomainError):
    def __init__(self, email: str):
        super().__init__(f'User with email {email} already exists')


class UserNotFoundById(DomainError):
    def __init__(self, user_id: int):
        super().__init__(f'User with id {user_id} not found')


class UserNotFoundByUsername(DomainError):
    def __init__(self, username: str):
        super().__init__(f'User with username {username} not found')
