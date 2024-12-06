import abc

from dtos.orders import UpdateOrderDto, OrderReqDto
from tools.token_tool_base import TokenToolBase


class OrderServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_to(self, req: OrderReqDto):
        raise NotImplementedError()

    def delete(self, order_id, user):
        raise NotImplementedError()

    @abc.abstractmethod
    def update_order(self, order_id: int, req_data: UpdateOrderDto):
        raise NotImplementedError()




