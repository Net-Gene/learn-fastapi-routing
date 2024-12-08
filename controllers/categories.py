from fastapi import APIRouter, Query, Depends
from fastapi_versioning import version

from dependencies import oauth2_scheme, LoggedInUser, Admin
from dtos.categories import CategoryDto, AddCategoryDtoReq, CategoryDtoRes, UpdateCategoryDtoReq
from mapper.mapper import ResponseMapper
from services.service_factory import CategoryService

router = APIRouter(prefix="/api/categories", tags=['categories'])


@router.get('/get_categories')
async def get_categories(service: CategoryService):
    result = service.get_all()

    return result


@router.get('/{category_id}/products')
@version(1, 0)
async def get_categories_with_products(
        service: CategoryService,
        category_id: int,
        # Kyselyparametri: sivu (oletusarvo 1, täytyy olla >= 1)
        page: int = Query(1, alias='page', ge=1),
):
    result = service.get_all_categories_with_products(page, category_id)

    return result


@router.post('/',
             dependencies=[Depends(Admin)]
             )
async def add_category(service: CategoryService,
                       mapper: ResponseMapper,
                       req: AddCategoryDtoReq,
                       account: LoggedInUser) -> CategoryDto:
    categories = service.add(req, account)

    return mapper.map('category_dto', categories)


@router.post('/{category_id}',
             dependencies=[Depends(Admin)]
             )
async def update_category(service: CategoryService,
                          category_id: int,
                          req: UpdateCategoryDtoReq):
    result = service.update(req, category_id)

    return result


@router.delete('/{category_id}',
               dependencies=[Depends(Admin)]
               )
async def delete_category(service: CategoryService,
                          category_id: int):
    result = service.delete(category_id)

    return result
