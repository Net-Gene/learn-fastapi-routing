import abc

from dtos.orders import UpdateOrderReqDto, OrderReqDto, OrderingReqDto
from tools.token_tool_base import TokenToolBase


class OrderServiceBase(abc.ABC):
    @abc.abstractmethod
    def get_all(self, page):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_to(self, req: OrderReqDto):
        raise NotImplementedError()

    def delete(self, order_id: int, user):
        raise NotImplementedError()

    @abc.abstractmethod
    def update_order(self, order_id: int, req: UpdateOrderReqDto, user):
        raise NotImplementedError()

    @abc.abstractmethod
    def order(self, req: OrderingReqDto, user):
        raise NotImplementedError()

    @abc.abstractmethod
    def confirm_order(self, order_id: int, user):
        raise NotImplementedError()

