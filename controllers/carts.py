from fastapi import APIRouter, Query, Depends

from dependencies import oauth2_scheme, LoggedInUser
from dtos.orders import OrderDto, OrderReqDto, DeleteOrderReqDto, UpdateOrderReqDto
from mapper.mapper import ResponseMapper
from services.service_factory import ProductService, OrderService

from fastapi_versioning import VersionedFastAPI, version

router = APIRouter(prefix="/api/cart", tags=['cart'])


@router.get('/')
@version(1, 0)
async def show_cart(service: OrderService,
                    mapper: ResponseMapper,
                    page: int = Query(1, alias='page', ge=1)  # Oletusarvo on 1, ja sivun on oltava >= 1 kooltaan
                    ):
    order = service.get_all(page)

    return mapper.map('order_dto', order)


@router.post('/items', dependencies=[Depends(oauth2_scheme)])
@version(1, 0)
async def add_to_cart(service: OrderService,
                      mapper: ResponseMapper,
                      req: OrderReqDto):
    order = service.add_to(req)

    return mapper.map('order_dto', order)


@router.delete('/items/{itemid}', dependencies=[Depends(oauth2_scheme)])
@version(1, 0)
async def delete_from_cart(service: OrderService,
                           itemid: int,
                           account: LoggedInUser):
    result = service.delete(itemid, account)

    return result


@router.patch('/items/{itemid}', dependencies=[Depends(oauth2_scheme)])
@version(1, 0)
async def update_product_in_cart(service: OrderService,
                                 itemid: int,
                                 req: UpdateOrderReqDto,
                                 account: LoggedInUser):
    result = service.update_order(itemid, req, account)

    return result


