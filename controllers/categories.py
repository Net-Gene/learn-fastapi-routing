
from fastapi import APIRouter
from mapper.mapper import ResponseMapper
from services.service_factory import CategoryService



router = APIRouter(prefix="/api/categories", tags=['categories'])


@router.get('/')
async def get_categories(service: CategoryService, mapper: ResponseMapper):
    categories = service.get_all()

    return mapper.map('category_dto', categories)


@router.get('/get_products_by_category')
async def get_categories_with_products(service: CategoryService, mapper: ResponseMapper):
    categories = service.get_all_categories_with_products()

    return mapper.map('category_dto', categories)