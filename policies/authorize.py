from typing import Annotated

from fastapi import HTTPException, Depends
from starlette import status
from starlette.requests import Request

import models
from services.service_factory import UserService


# def get_logged_in_user(user_service: UserService, token: TokenTool, req: Request):
#     token_from_header = req.headers.get('Authorization')
#     if token_from_header is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     header_parts = token_from_header.split(' ')
#     if len(header_parts) != 2:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     if header_parts[0] != 'Bearer':
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     claims = token.validate_token(header_parts[1])
#     # tämä metodi puuttuu user_sevicesta
#     logged_in_user = user_service.get_user_by_id(claims['sub'])
#     if logged_in_user is None:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
#     return logged_in_user
#
#
# LoggedInUser = Annotated[models.Users, Depends(get_logged_in_user)]
