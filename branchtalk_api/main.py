import argparse
import logging
from contextlib import asynccontextmanager

import uvicorn
from dishka import AsyncContainer, make_async_container
from dishka.integrations import fastapi as fastapi_integration
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from branchtalk_api.config import Config
from branchtalk_api.ioc import AppProvider
from branchtalk_api.presentation.exception_handlers import include_exception_handlers
from branchtalk_api.presentation.middleware.auth import AuthMiddleware
from branchtalk_api.presentation.routers.root import root_router

config = Config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def create_app(
    dishka_container: AsyncContainer,
    auth_middleware: AuthMiddleware,
):
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(BaseHTTPMiddleware, dispatch=auth_middleware)
    app.include_router(root_router)
    app.middleware = auth_middleware

    fastapi_integration.setup_dishka(dishka_container, app)
    include_exception_handlers(app)

    return app


def setup_logging():
    log_format = '%(asctime)s [%(levelname)-8s] [PID: %(process)-5d] ' '[%(module)-20s] %(message)s'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('asyncio').setLevel(logging.ERROR)


def parse_argument() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Launch API server with custom host and port.',
    )

    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help="The host address to bind the server to. Default is 'localhost'.",
    )

    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='The port number to bind the server to. Default is 8000.',
    )

    return parser.parse_args()


if __name__ == '__main__':
    launch_args = parse_argument()
    setup_logging()

    container = make_async_container(AppProvider(), context={Config: config})
    auth = AuthMiddleware(
        container=container,
        exclude_paths=[
            '/docs',
            '/openapi.json',
            '/user/auth/login',
            '/user/auth/signup',
            '/user/auth/refresh',
        ],
    )

    uvicorn.run(
        create_app(
            dishka_container=container,
            auth_middleware=auth,
        ),
        host=launch_args.host,
        port=launch_args.port,
        lifespan='on',
    )
