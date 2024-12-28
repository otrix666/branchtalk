from .base import ApplicationError


class InvalidRefreshToken(ApplicationError):
    def __init__(self):
        super().__init__('Invalid refresh token')
