from datetime import datetime
from typing import List

import bcrypt

import models
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.taken_exception import TakenException
from dtos.users import UpdateUserDto, AddUserReq, LoginReqDto
from services.user_service_base import UserServiceBase
from tools.token_tool_base import TokenToolBase


class UserSaService(UserServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[models.Users]:
        try:
            users = self.context.query(models.Users).all()
            if users is None:
                raise NotFoundException('Käyttäjiä ei löydetty')
            return users

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException(e)

    def get_by_id(self, user_id) -> models.Users:
        try:

            user = self.context.query(models.Users).filter(models.Users.Id == int(user_id)).first()
            if user is None:
                raise NotFoundException('Käyttäjätunnusta ei löydetty')
            return user

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException(e)

    def update_user(self, user_id: int, req_data: UpdateUserDto):
        try:

            user = self.context.query(models.Users).filter(models.Users.Id == user_id).first()

            if user is None:
                raise NotFoundException('Käyttäjätunnusta ei löydetty')
            user.UserName = req_data.username
            self.context.commit()
            return user

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException(e)

    def create(self, req: AddUserReq) -> models.Users:
        try:

            user_exists = self.context.query(models.Users).filter(models.Users.UserName == req.username).first()
            if user_exists is not None:
                raise TakenException('käyttäjätunnus on jo varattu')
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

        except TakenException as e:
            # Käsittele erityisiä poikkeuksia, kuten TakenException

            print(f"Virhe: {e}")
            raise TakenException(e)

    def login(self, req: LoginReqDto, token: TokenToolBase) -> str:
        try:
            print(f"Login request received: {req}")
            user = self.context.query(models.Users).filter(models.Users.UserName == req.username).first()
            if user is None:
                raise NotFoundException('user not found')

            if bcrypt.checkpw(req.password.encode('utf-8'), user.HashedPassword):
                return token.create_token(
                    {'sub': str(user.Id), 'username': user.UserName, 'iat': datetime.now().timestamp(),
                     'exp': datetime.now().timestamp() + (3600 * 24 * 7)})
            raise NotFoundException('user not found')

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException(e)

