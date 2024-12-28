from .base import ApplicationError


class InvalidJwt(ApplicationError):
    def __init__(self, jwt: str) -> None:
        super().__init__(f'Invalid JWT: {jwt}')


class ExpiredJwt(ApplicationError):
    def __init__(self, jwt: str) -> None:
        super().__init__(f'Expired JWT: {jwt}')
