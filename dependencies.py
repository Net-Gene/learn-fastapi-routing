from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

import models
from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.unauthorized_exception import UnauthorizedException
from services.service_factory import UserService
from tools.token_factory import AppToken


def get_logged_in_user(user_service: UserService, token: AppToken, req: Request) -> models.Users:
    token_from_header = req.headers.get('Authorization')

    if token_from_header is None:
        raise UnauthorizedException()
    header_parts = token_from_header.split(' ')

    if len(header_parts) != 2:
        raise UnauthorizedException()

    if header_parts[0] != 'Bearer':
        raise UnauthorizedException()
    claims = token.validate_token(header_parts[1])

    # tämä metodi puuttuu user_sevicesta
    logged_in_user = user_service.get_by_id(claims['sub'])

    if logged_in_user is None:
        raise UnauthorizedException()
    return logged_in_user


def require_admin(user_service: UserService, token: AppToken, req: Request) -> models.Users:
    user = get_logged_in_user(user_service, token, req)

    if user.Role != 'admin':
        raise ForbiddenException()
    return user


LoggedInUser = Annotated[models.Users, Depends(get_logged_in_user)]
Admin = Annotated[models.Users, Depends(require_admin)]
