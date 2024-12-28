from dishka import AsyncContainer
from starlette.requests import Request
from starlette.responses import JSONResponse

from branchtalk_api.application.interfaces.jwt_service import JwtService
from branchtalk_api.application.services.jwt_service import TOKEN_TYPE_FIELD, TokenType


class AuthMiddleware:
    def __init__(
        self,
        container: AsyncContainer,
        exclude_paths: list,
    ):
        self._container = container
        self._exclude_paths = exclude_paths

    async def __call__(self, request: Request, call_next):
        if request.url.path in self._exclude_paths:
            return await call_next(request)

        async with self._container() as container:
            jwt_service = await container.get(JwtService)

        print(request.headers)
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JSONResponse(status_code=401, content={'detail': 'Invalid credentials'})

        token = auth_header.split(' ')[1]
        payload = jwt_service.verify_token(token=token)
        token_type = payload.get(TOKEN_TYPE_FIELD)

        if TokenType(token_type) == TokenType.REFRESH_TOKEN and not request.url.path.endswith('/refresh'):
            return JSONResponse(status_code=401, content={'detail': 'Invalid token type'})

        return await call_next(request)
