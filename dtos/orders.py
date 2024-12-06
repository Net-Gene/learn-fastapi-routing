from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderDto(BaseModel):
    id: int
    createdDate: datetime = Field(..., alias="created_date")
    confirmedDate: Optional[datetime] = Field(None, alias="confirmed_date")
    removedDate: Optional[datetime] = Field(None, alias="removed_date")
    state: str
    customerId: int = Field(..., alias="customer_id")
    handlerId: Optional[int] = Field(None, alias="handler_id")

    class Config:
        # Allow Pydantic to use alias for serialization
        populate_by_name = True


class OrderReqDto(BaseModel):
    product_id: int
    quantity: int
    user_id: int


class DeleteOrderReqDto(BaseModel):
    order_id: int
    product_id: int


class UpdateOrderReqDto(BaseModel):
    product_id: int
    unit_count: int


class OrderingReqDto(BaseModel):
    order_id: int
