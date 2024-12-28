from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from branchtalk_api.application.use_cases.post import CreatePostInteractor, DeletePostInteractor, UpdatePostInteractor
from branchtalk_api.presentation.schemas.post import CreatePost, DeletePost, UpdatePost

post_router = APIRouter(
    prefix='/post',
    route_class=DishkaRoute,
    tags=['post'],
)


@post_router.post('')
async def create_post(
    interactor: FromDishka[CreatePostInteractor],
    data: CreatePost,
):
    await interactor(data.to_dto())


@post_router.patch('')
async def update_post(
    interactor: FromDishka[UpdatePostInteractor],
    data: UpdatePost,
):
    await interactor(data.to_dto())


@post_router.delete('')
async def delete_post(
    interactor: FromDishka[DeletePostInteractor],
    data: DeletePost,
):
    await interactor(data.to_dto())
