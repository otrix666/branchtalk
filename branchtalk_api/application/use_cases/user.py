from concurrent.futures import ThreadPoolExecutor

from branchtalk_api.application import exceptions, interfaces
from branchtalk_api.application.dto.user import (
    LoginResponseDTO,
    RefreshDTO,
    RefreshResponseDTO,
    UserCreateDTO,
    UserLoginDTO,
)
from branchtalk_api.application.interfaces import UserReader
from branchtalk_api.application.services.jwt_service import TOKEN_TYPE_FIELD, TokenType
from branchtalk_api.domain.entities.users import User


class RegistrationInteractor:
    def __init__(
        self,
        user_saver: interfaces.UserSaver,
        hasher: interfaces.PasswordHasher,
        thread_pool: ThreadPoolExecutor,
    ):
        self._user_saver = user_saver
        self._hasher = hasher
        self._thread_pool = thread_pool

    async def __call__(self, data: UserCreateDTO):
        future_hashed_password = self._thread_pool.submit(self._hasher.hash, data.password)
        hashed_password = future_hashed_password.result()

        user = User(
            id=None,
            username=data.username,
            email=data.email,
            password=hashed_password.decode(),
        )

        await self._user_saver.save(user=user)


class LoginInteractor:
    def __init__(
        self,
        user_reader: interfaces.UserReader,
        jwt_service: interfaces.JwtService,
        password_service: interfaces.PasswordHasher,
    ):
        self._user_reader = user_reader
        self._jwt_service = jwt_service
        self._password_service = password_service

    async def __call__(self, data: UserLoginDTO) -> LoginResponseDTO:
        user = await self._user_reader.get_by_username(username=data.username)

        if not user or not self._password_service.verify(data.password, user.password):
            raise exceptions.InvalidLoginOrPassword

        access_token = self._jwt_service.create_access_token(user=user)
        refresh_token = self._jwt_service.create_refresh_token(user=user)
        return LoginResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )


class RefreshInteractor:
    def __init__(
        self,
        user_reader: UserReader,
        jwt_service: interfaces.JwtService,
    ):
        self._user_reader = user_reader
        self._jwt_service = jwt_service

    async def __call__(self, data: RefreshDTO) -> RefreshResponseDTO:
        payload = self._jwt_service.verify_token(token=data.refresh_token)
        token_type = payload.get(TOKEN_TYPE_FIELD)

        if TokenType(token_type) != TokenType.REFRESH_TOKEN:
            raise exceptions.InvalidRefreshToken

        user_id = int(payload.get('sub'))
        user = await self._user_reader.get_by_id(user_id=user_id)

        access_token = self._jwt_service.create_access_token(user=user)
        return RefreshResponseDTO(
            access_token=access_token,
        )
