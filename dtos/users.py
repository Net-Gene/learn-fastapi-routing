from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    username: str


class UserDto(BaseModel):
    id: int
    username: str
    role: str


class AddUserReq(BaseModel):
    username: str
    password: str


class LoginReq(BaseModel):
    username: str
    password: str

class LoginRes(BaseModel):
    token: str
