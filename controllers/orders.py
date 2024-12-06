from fastapi import APIRouter, Query, Depends

from dependencies import oauth2_scheme, LoggedInUser
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


@router.get('/confirm')
@version(1, 0)
async def confirm_orders(service: OrderService,
                         mapper: ResponseMapper,
                         page: int = Query(1, alias='page', ge=1)  # Oletusarvo on 1, ja sivun on oltava >= 1 kooltaan
                         ):
    products = service.get_all(page)

    return mapper.map('product_dto', products)
