import abc

from dtos.users import UpdateUserDto, AddUserReq, LoginReqDto
from tools.token_tool_base import TokenToolBase


class UserServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_by_id(self, _id):
        raise NotImplementedError()

    @abc.abstractmethod
    def update_user(self, user_id: int, req_data: UpdateUserDto):
        raise NotImplementedError()

    @abc.abstractmethod
    def create(self, req: AddUserReq):
        raise NotImplementedError()

    @abc.abstractmethod
    def login(self, req: LoginReqDto, token: TokenToolBase) -> str:
        raise NotImplementedError()

