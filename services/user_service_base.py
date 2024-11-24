import abc

from dtos.users import UpdateUserDto


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
