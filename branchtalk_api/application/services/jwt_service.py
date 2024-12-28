import enum
from datetime import datetime, timedelta

import jwt

from branchtalk_api.application import interfaces
from branchtalk_api.application.exceptions.jwt import ExpiredJwt, InvalidJwt
from branchtalk_api.domain.entities.users import User

TOKEN_TYPE_FIELD = 'type'


class TokenType(str, enum.Enum):
    ACCESS_TOKEN = 'access'
    REFRESH_TOKEN = 'refresh'


class JwtService(interfaces.JwtService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = 'HS256',
        expiration_access: int = 60 * 5,
        expiration_refresh: int = 60 * 60 * 24 * 30,
    ):
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expiration_access = expiration_access
        self._expiration_refresh = expiration_refresh

    def create_jwt(self, payload: dict, expiration_time: int, token_type: str) -> str:
        iat = datetime.now()
        exp = iat + timedelta(seconds=expiration_time)

        payload.update({'iat': iat, 'exp': exp, TOKEN_TYPE_FIELD: token_type})

        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return token

    def create_access_token(self, user: User) -> str:
        payload = {
            'sub': str(user.id),
            'username': user.username,
        }
        return self.create_jwt(
            payload=payload,
            expiration_time=self._expiration_access,
            token_type=TokenType.ACCESS_TOKEN,
        )

    def create_refresh_token(self, user: User) -> str:
        payload = {
            'sub': str(user.id),
        }
        return self.create_jwt(
            payload=payload,
            expiration_time=self._expiration_refresh,
            token_type=TokenType.REFRESH_TOKEN,
        )

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise ExpiredJwt(token)
        except jwt.InvalidTokenError:
            raise InvalidJwt(token)
