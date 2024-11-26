from datetime import datetime
from typing import List

import bcrypt

import models
from custom_exceptions.not_found_exception import NotFoundexception
from custom_exceptions.username_taken_exception import UsernameTakenException
from dtos.users import UpdateUserDto, AddUserReq, LoginReqDto
from services.user_service_base import UserServiceBase
from tools.token_tool_base import TokenToolBase


class UserSaService(UserServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[models.Users]:
        return self.context.query(models.Users).all()

    def get_by_id(self, user_id) -> models.Users:
        return self.context.query(models.Users).filter(models.Users.Id == user_id).first()

    def update_user(self, user_id: int, req_data: UpdateUserDto):
        user = self.context.query(models.Users).filter(models.Users.Id == user_id).first()

        if user is None:
            return None
        user.UserName = req_data.username
        self.context.commit()
        return user

    def create(self, req: AddUserReq) -> models.Users:
        user_exists = self.context.query(models.Users).filter(models.Users.UserName == req.username).first()
        if user_exists is not None:
            # tätä exception tyyppiä meillä ei vielä ole
            raise UsernameTakenException('username already taken')
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

    def login(self, req: LoginReqDto, token: TokenToolBase) -> str:
        user = self.context.query(models.Users).filter(models.Users.UserName == req.username).first()
        if user is None:
            raise NotFoundexception('user not found')

        if bcrypt.checkpw(req.password.encode('utf-8'), user.HashedPassword):
            return token.create_token(
                {'sub': user.Id, 'username': user.UserName, 'iat': datetime.now().timestamp(),
                 'exp': datetime.now().timestamp() + (3600 * 24 * 7)})
        raise NotFoundexception('user not found')

