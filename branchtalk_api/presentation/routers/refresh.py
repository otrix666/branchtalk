from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from branchtalk_api.application.dto.refresh import RefreshResponseDTO
from branchtalk_api.application.use_cases.refresh import RefreshInteractor
from branchtalk_api.presentation.schemas.refresh import RefreshToken

refresh_router = APIRouter(
    prefix='/refresh',
    route_class=DishkaRoute,
    tags=['refresh'],
)


@refresh_router.get('', response_model=RefreshResponseDTO)
async def refresh_auth_token(
    interactor: FromDishka[RefreshInteractor],
    data: RefreshToken,
):
    await interactor(data.to_dto())
