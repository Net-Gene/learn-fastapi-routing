from fastapi import APIRouter, Query, Depends

from dependencies import oauth2_scheme, LoggedInUser, Admin
from dtos.orders import UpdateOrderReqDto, DeleteOrderReqDto, OrderingReqDto
from mapper.mapper import ResponseMapper
from services.service_factory import ProductService, OrderService

from fastapi_versioning import VersionedFastAPI, version

router = APIRouter(prefix="/api/orders", tags=['orders'])


@router.post('/', dependencies=[Depends(oauth2_scheme)])
@version(1, 0)
async def ordering_product_in_cart(service: OrderService, req: OrderingReqDto,
                                   account: LoggedInUser):
    result = service.order(req, account)

    return result


@router.post('/{order_id}/confirm', dependencies=[Depends(Admin)])
@version(1, 0)
async def confirm_orders(service: OrderService,
                         order_id: int,
                         account: LoggedInUser):
    result = service.confirm_order(order_id, account)

    return result
