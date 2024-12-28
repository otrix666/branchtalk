from fastapi import APIRouter

from .auth import auth_router
from .comment import comment_router
from .post import post_router
from .refresh import refresh_router

root_router = APIRouter()

root_router.include_router(auth_router)
root_router.include_router(post_router)
root_router.include_router(comment_router)
root_router.include_router(refresh_router)
