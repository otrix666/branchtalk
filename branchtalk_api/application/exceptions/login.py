from .base import ApplicationError


class InvalidLoginOrPassword(ApplicationError):
    def __init__(self):
        super().__init__('Invalid login or password')
