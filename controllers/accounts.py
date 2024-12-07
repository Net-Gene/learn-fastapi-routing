from fastapi import APIRouter, Depends
from fastapi_versioning import version

from dependencies import oauth2_scheme, LoggedInUser, Admin
from dtos.orders import OrderingReqDto
from services.service_factory import OrderService

router = APIRouter(prefix="/api/account", tags=['account'])


@router.delete('/orders/{order_id}', dependencies=[Depends(oauth2_scheme)])
@version(1, 0)
async def delete_account_order(service: OrderService, order_id: int, account: LoggedInUser):
    result = service.delete_order(order_id, account)

    return result
