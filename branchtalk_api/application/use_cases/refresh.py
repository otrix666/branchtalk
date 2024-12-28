from branchtalk_api.application import exceptions, interfaces
from branchtalk_api.application.dto.refresh import RefreshDTO, RefreshResponseDTO
from branchtalk_api.application.interfaces import UserReader
from branchtalk_api.application.services.jwt_service import TOKEN_TYPE_FIELD, TokenType


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

        user_id = payload.get('sub')
        user = await self._user_reader.get_by_id(user_id=user_id)

        access_token = self._jwt_service.create_access_token(user=user)
        return RefreshResponseDTO(
            access_token=access_token,
        )
