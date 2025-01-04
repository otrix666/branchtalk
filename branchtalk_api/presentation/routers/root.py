from fastapi import APIRouter

from .comment import comment_router
from .post import post_router
from .user import user_router

root_router = APIRouter()

root_router.include_router(user_router)
root_router.include_router(post_router)
root_router.include_router(comment_router)
