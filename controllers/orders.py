from fastapi import APIRouter, Query
from mapper.mapper import ResponseMapper
from services.service_factory import ProductService, OrderService

from fastapi_versioning import VersionedFastAPI, version

router = APIRouter(prefix="/api/orders", tags=['orders'])


@router.get('/')
@version(1, 0)
async def make_orders(service: OrderService,
                      mapper: ResponseMapper,
                      page: int = Query(1, alias='page', ge=1)  # Oletusarvo on 1, ja sivun on oltava >= 1 kooltaan
                      ):
    products = service.get_all(page)

    return mapper.map('product_dto', products)


@router.get('/confirm')
@version(1, 0)
async def confirm_orders(service: OrderService,
                         mapper: ResponseMapper,
                         page: int = Query(1, alias='page', ge=1)  # Oletusarvo on 1, ja sivun on oltava >= 1 kooltaan
                         ):
    products = service.get_all(page)

    return mapper.map('product_dto', products)
