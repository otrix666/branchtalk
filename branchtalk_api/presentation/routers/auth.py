from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from branchtalk_api.application.dto.user import LoginResponseDTO
from branchtalk_api.application.use_cases.login import LoginInteractor
from branchtalk_api.application.use_cases.registration import RegistrationInteractor
from branchtalk_api.presentation.schemas.user import UserCreate, UserLogin

auth_router = APIRouter(
    prefix='/auth',
    route_class=DishkaRoute,
    tags=['auth'],
)


@auth_router.post('/signup')
async def signup_user(
    interactor: FromDishka[RegistrationInteractor],
    data: UserCreate,
):
    await interactor(data.to_dto())


@auth_router.post('/login', response_model=LoginResponseDTO)
async def login_user(
    interactor: FromDishka[LoginInteractor],
    data: UserLogin,
):
    auth_credentials = await interactor(data.to_dto())
    return auth_credentials
