import token
from datetime import datetime

import bcrypt
import fstr
from fastapi import HTTPException

import models
from dtos.users import UpdateUserDto, UserDto, AddUserReq, LoginReq
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

    def create(self, req: AddUserReq) -> models.Users:
        user = models.Users(
            UserName=req.username,
            HashedPassword=bcrypt.hashpw(req.password.encode('utf-8'), bcrypt.gensalt()),
            Role="customer"
        )

        # bcyrptia käytettäessä meidän ei itse tarvitse tallentaa saltia
        # erilliseen taulun sarakkeeseen,
        # bcrypt huolehtii tästä itse
        user.PasswordSalt = ''.encode('utf-8')
        self.context.add(user)
        self.context.commit()
        return user

    def login(self, req: LoginReq) -> fstr:
        user = self.context.query(models.Users).filter(models.Users.UserName == req.username).first()
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        # if bcrypt.checkpw(req.password.encode('utf-8'), user.HashedPassword):
        #     return token.create_token({'sub': user.Id, 'username': user.UserName, 'iat': datetime.now().timestamp(),
        #                                'exp': datetime.now().timestamp() + (3600 * 24 * 7)}, _key='supersecret')
        return ""
