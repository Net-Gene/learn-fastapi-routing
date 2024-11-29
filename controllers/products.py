
from fastapi import APIRouter, Query
from mapper.mapper import ResponseMapper
from services.service_factory import ProductService

from fastapi_versioning import VersionedFastAPI, version


router = APIRouter(prefix="/api/products", tags=['products'])


@router.get('/')
@version(1, 0)
async def get_products(service: ProductService, 
                       mapper: ResponseMapper, 
                        page: int = Query(1, alias='page', ge=1)  # Oletusarvo on 1, ja sivun on oltava >= 1 kooltaan
                       ):
    products = service.get_all(page)

    return mapper.map('product_dto', products)

