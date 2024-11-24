from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    username: str


class UserDto(BaseModel):
    id: int
    username: str
    role: str
