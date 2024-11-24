from fastapi import HTTPException

import models
from dtos.users import UpdateUserDto, UserDto
from services.user_service_base import UserServiceBase


class UserSaService(UserServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self):
        users = self.context.query(models.Users).all()
        return users

    def get_by_id(self, user_id):
        users = self.context.query(models.Users).filter(models.Users.Id == user_id).first()
        return users

    def update_user(self, user_id: int, req_data: UpdateUserDto):
        user = self.context.query(models.Users).filter(models.Users.Id == user_id).first()

        if user is None:
            return None
        user.UserName = req_data.username
        self.context.commit()
        return user
