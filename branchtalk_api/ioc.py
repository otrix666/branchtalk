from collections.abc import AsyncIterable, Iterable
from concurrent.futures import ThreadPoolExecutor

import asyncpg
from dishka import AnyOf, Provider, Scope, from_context, provide

from branchtalk_api.application import interfaces
from branchtalk_api.application.services.jwt_service import JwtService
from branchtalk_api.application.use_cases.comment import (
    CommentDeleteManager,
    CommentUpdateManager,
    CreateCommentInteractor,
    DeleteCommentInteractor,
    UpdateCommentInteractor,
)
from branchtalk_api.application.use_cases.post import (
    CreatePostInteractor,
    DeletePostInteractor,
    PostDeleteManager,
    PostUpdateManager,
    UpdatePostInteractor,
)
from branchtalk_api.application.use_cases.user import LoginInteractor, RefreshInteractor, RegistrationInteractor
from branchtalk_api.config import Config
from branchtalk_api.infrastructure.data_mappers.comment import CommentDataMapper
from branchtalk_api.infrastructure.data_mappers.post import PostDataMapper
from branchtalk_api.infrastructure.data_mappers.user import UserDataMapper
from branchtalk_api.infrastructure.repositories.comments import CommentsRepository
from branchtalk_api.infrastructure.repositories.posts import PostRepository
from branchtalk_api.infrastructure.repositories.user import UserRepository
from branchtalk_api.infrastructure.services.password_hasher import BcryptPasswordHasher


class AppProvider(Provider):
    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST, provides=interfaces.PasswordHasher)
    def get_hasher(self) -> BcryptPasswordHasher:
        return BcryptPasswordHasher()

    @provide(scope=Scope.REQUEST, provides=interfaces.JwtService)
    def get_jwt_service(self, config: Config) -> JwtService:
        return JwtService(
            secret_key=config.access_config.secrete,
            algorithm=config.access_config.algorithm,
            expiration_access=config.access_config.access_token_lifetime_sec,
            expiration_refresh=config.access_config.refresh_token_lifetime_sec,
        )

    @provide(scope=Scope.APP)
    def get_thread_pool(self) -> Iterable[ThreadPoolExecutor]:
        thread_pool = ThreadPoolExecutor(max_workers=8)
        yield thread_pool
        thread_pool.shutdown()

    @provide(scope=Scope.APP)
    async def get_connection_pool(self, config: Config) -> AsyncIterable[asyncpg.Pool]:
        pool = await asyncpg.create_pool(
            host=config.pg.host,
            port=config.pg.port,
            user=config.pg.user,
            database=config.pg.db,
            password=config.pg.password,
            min_size=70,
            max_size=100,
        )
        yield pool
        await pool.close()

    user_data_mapper = provide(UserDataMapper, scope=Scope.REQUEST)
    user_repo = provide(
        UserRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[interfaces.UserReader, interfaces.UserSaver],
    )

    post_data_mapper = provide(PostDataMapper, scope=Scope.REQUEST)
    post_repo = provide(
        PostRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.PostSaver,
            PostUpdateManager,
            PostDeleteManager,
        ],
    )

    comment_data_mapper = provide(CommentDataMapper, scope=Scope.REQUEST)
    comment_repo = provide(
        CommentsRepository,
        scope=Scope.REQUEST,
        provides=AnyOf[
            interfaces.CommentSaver,
            CommentUpdateManager,
            CommentDeleteManager,
        ],
    )

    login_interactor = provide(LoginInteractor, scope=Scope.REQUEST)
    register_interactor = provide(RegistrationInteractor, scope=Scope.REQUEST)

    create_post_interactor = provide(CreatePostInteractor, scope=Scope.REQUEST)
    update_post_interactor = provide(UpdatePostInteractor, scope=Scope.REQUEST)
    delete_post_interactor = provide(DeletePostInteractor, scope=Scope.REQUEST)

    create_comment_interactor = provide(CreateCommentInteractor, scope=Scope.REQUEST)
    update_comment_interactor = provide(UpdateCommentInteractor, scope=Scope.REQUEST)
    delete_comment_interactor = provide(DeleteCommentInteractor, scope=Scope.REQUEST)

    refresh_token_interactor = provide(RefreshInteractor, scope=Scope.REQUEST)
