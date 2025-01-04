from fastapi import FastAPI

from branchtalk_api.application import exceptions as app_exc
from branchtalk_api.domain import exceptions as domain_exc
from branchtalk_api.presentation.middleware.exc_handler import (
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


def include_exception_handlers(app: FastAPI):
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
