
from fastapi import APIRouter
from mapper.mapper import ResponseMapper
from services.service_factory import ProductService



router = APIRouter(prefix="/api/products", tags=['products'])


@router.get('/Kaikkien tuotteiden listaus')
async def get_products(service: ProductService, mapper: ResponseMapper):
    products = service.get_all()

    return mapper.map('product_dto', products)

