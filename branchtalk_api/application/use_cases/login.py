from branchtalk_api.application import interfaces
from branchtalk_api.application.dto.user import LoginResponseDTO, UserLoginDTO
from branchtalk_api.application.exceptions.login import InvalidLoginOrPassword


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
            raise InvalidLoginOrPassword

        access_token = self._jwt_service.create_access_token(user=user)
        refresh_token = self._jwt_service.create_refresh_token(user=user)
        return LoginResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )
