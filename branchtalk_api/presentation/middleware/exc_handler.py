from fastapi import Request
from fastapi.responses import JSONResponse


async def username_already_exists_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={'detail': 'Username already exists'},
    )


async def email_already_exists_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content={'detail': 'Email already exists'},
    )


async def user_not_found_by_id_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'User not found'},
    )


async def user_not_found_by_username_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'User not found'},
    )


async def authentication_error_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Invalid username or password'},
    )


async def invalid_token_error_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Invalid token'},
    )


async def token_expired_error_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Token has expired'},
    )


async def invalid_refresh_token_error_handler(
    request: Request,
    exception: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=401,
        content={'detail': 'Invalid refresh token'},
    )


async def post_not_found_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'Post not found'},
    )


async def user_post_not_found_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'Post not found for user'},
    )


async def comment_not_found_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'Comment not found'},
    )


async def user_comment_not_found_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={'detail': 'Comment not found for user'},
    )
