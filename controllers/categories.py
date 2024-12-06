from fastapi import APIRouter, Query
from fastapi_versioning import version
from mapper.mapper import ResponseMapper
from services.service_factory import CategoryService

router = APIRouter(prefix="/api/categories", tags=['categories'])


@router.get('/')
async def get_categories(service: CategoryService, mapper: ResponseMapper):
    categories = service.get_all()

    return mapper.map('category_dto', categories)


@router.get('/{id}/products')
@version(1, 0)
async def get_categories_with_products(
        service: CategoryService,
        mapper: ResponseMapper,
        id: int,  # Polkuparametri: luokan tunnus
        page: int = Query(1, alias='page', ge=1),  # Query parameter: page (default to 1, must be >= 1)
):
    categories = service.get_all_categories_with_products(page)

    # Etsi luokka määritetyllä tunnuksella
    category = next((cat for cat in categories if cat["id"] == id), None)

    if not category:
        return {"error": "Category not found"}

    return mapper.map('category_dto', [category])
