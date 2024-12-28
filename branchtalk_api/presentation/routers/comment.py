from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from branchtalk_api.application.use_cases.comment import (
    CreateCommentInteractor,
    DeleteCommentInteractor,
    UpdateCommentInteractor,
)
from branchtalk_api.presentation.schemas.comment import CreateComment, DeleteComment, UpdateComment

comment_router = APIRouter(
    prefix='/comment',
    route_class=DishkaRoute,
    tags=['comment'],
)


@comment_router.post('')
async def create_comment(
    interactor: FromDishka[CreateCommentInteractor],
    data: CreateComment,
):
    await interactor(data.to_dto())


@comment_router.patch('')
async def update_comment(
    interactor: FromDishka[UpdateCommentInteractor],
    data: UpdateComment,
):
    await interactor(data.to_dto())


@comment_router.delete('')
async def delete_comment(
    interactor: FromDishka[DeleteCommentInteractor],
    data: DeleteComment,
):
    await interactor(data.to_dto())
