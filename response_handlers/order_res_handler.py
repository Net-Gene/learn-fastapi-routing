from typing import Annotated

from fastapi import Depends

from models import Orders


class OrderResHandler:
    def send(self, order):
        return Orders(id=order.Id, customerId=order.CustomerId, handlerId=order.HandlerId, state=order.State,
                      createdDate=order.CreatedDate, removedDate=order.RemovedDate, confirmedDate=order.ConfirmedDate)


def init_order_response_handler():
    return OrderResHandler()


OrderResResponseHandler = Annotated[OrderResHandler, Depends(init_order_response_handler)]
