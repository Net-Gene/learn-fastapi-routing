from typing import Annotated

from fastapi import Depends


class UserResHandler:
    def send(self, user):
        return UserRes(id=user.Id, username=user.UserName, role=user.Role)


def init_user_response_handler():
    return UserResHandler()


UserResResponseHandler = Annotated[UserResHandler, Depends(init_user_response_handler)]
