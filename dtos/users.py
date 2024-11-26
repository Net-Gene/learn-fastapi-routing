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


class LoginReqDto(BaseModel):
    username: str
    password: str


class LoginResDto(BaseModel):
    token: str
