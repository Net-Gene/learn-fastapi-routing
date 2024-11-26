from typing import Annotated

from fastapi import Depends

from models import Users


class UserResHandler:
    def send(self, user):
        return Users(id=user.Id, username=user.UserName, role=user.Role)


def init_user_response_handler():
    return UserResHandler()


UserResResponseHandler = Annotated[UserResHandler, Depends(init_user_response_handler)]
