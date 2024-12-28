import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from branchtalk_api.application import exceptions as app_exc
from branchtalk_api.config import Config
from branchtalk_api.domain import exceptions as domain_exc
from branchtalk_api.infrastructure.middleware.auth_middleware import AuthMiddleware
from branchtalk_api.ioc import AppProvider
from branchtalk_api.presentation.routers.exc_handler import (
    authentication_error_handler,
    comment_not_found_error_handler,
    email_already_exists_error_handler,
    invalid_refresh_token_error_handler,
    invalid_token_error_handler,
    post_not_found_error_handler,
    token_expired_error_handler,
    user_comment_not_found_error_handler,
    user_not_found_by_id_error_handler,
    user_not_found_by_username_error_handler,
    user_post_not_found_error_handler,
    username_already_exists_error_handler,
)
from branchtalk_api.presentation.routers.root import root_router

config = Config()
container = make_async_container(AppProvider(), context={Config: config})


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app():
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    app = FastAPI(lifespan=lifespan)
    fastapi_integration.setup_dishka(container, app)

    app.include_router(root_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=AuthMiddleware(
            container=container,
            exclude_paths=[
                '/docs',
                '/openapi.json',
                '/auth/login',
                '/auth/signup',
                '/refresh',
            ],
        ),
    )

    app.add_exception_handler(
        domain_exc.UsernameAlreadyExists,
        username_already_exists_error_handler,
    )
    app.add_exception_handler(
        domain_exc.EmailAlreadyExists,
        email_already_exists_error_handler,
    )
    app.add_exception_handler(
        domain_exc.UserNotFoundById,
        user_not_found_by_id_error_handler,
    )
    app.add_exception_handler(
        domain_exc.UserNotFoundByUsername,
        user_not_found_by_username_error_handler,
    )
    app.add_exception_handler(
        app_exc.InvalidLoginOrPassword,
        authentication_error_handler,
    )
    app.add_exception_handler(
        app_exc.InvalidJwt,
        invalid_token_error_handler,
    )
    app.add_exception_handler(
        app_exc.ExpiredJwt,
        token_expired_error_handler,
    )
    app.add_exception_handler(
        app_exc.InvalidRefreshToken,
        invalid_refresh_token_error_handler,
    )
    app.add_exception_handler(
        domain_exc.PostNotFoundById,
        post_not_found_error_handler,
    )
    app.add_exception_handler(
        domain_exc.PostNotFoundForUser,
        user_post_not_found_error_handler,
    )
    app.add_exception_handler(
        domain_exc.CommentNotFoundById,
        comment_not_found_error_handler,
    )
    app.add_exception_handler(
        domain_exc.CommentNotFoundForUser,
        user_comment_not_found_error_handler,
    )

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=8000, lifespan='on')
