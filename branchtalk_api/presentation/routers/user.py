from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from branchtalk_api.application.dto.user import LoginResponseDTO, RefreshResponseDTO
from branchtalk_api.application.use_cases.user import LoginInteractor, RefreshInteractor, RegistrationInteractor
from branchtalk_api.presentation.schemas.user import RefreshToken, UserCreate, UserLogin

user_router = APIRouter(
    prefix='/user',
    route_class=DishkaRoute,
    tags=['user'],
)


@user_router.post('/auth/signup')
async def signup_user(
    interactor: FromDishka[RegistrationInteractor],
    data: UserCreate,
):
    await interactor(data.to_dto())


@user_router.post('/auth/login', response_model=LoginResponseDTO)
async def login_user(
    interactor: FromDishka[LoginInteractor],
    data: UserLogin,
):
    auth_credentials = await interactor(data.to_dto())
    return auth_credentials


@user_router.post('/auth/refresh', response_model=RefreshResponseDTO)
async def refresh_auth_token(
    interactor: FromDishka[RefreshInteractor],
    data: RefreshToken,
):
    access_token = await interactor(data.to_dto())
    return access_token
