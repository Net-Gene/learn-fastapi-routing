from typing import Annotated
from fastapi.params import Depends
import models
from services.category_sa_service import CategorySaService
from services.category_service_base import CategoryServiceBase
from services.order_sa_service import OrderSaService
from services.order_service_base import OrderServiceBase
from services.product_sa_service import ProductSaService
from services.product_service_base import ProductServiceBase
from services.user_sa_service import UserSaService
from services.user_service_base import UserServiceBase


def init_user_service(context: models.Db):
    return UserSaService(context)


def init_product_service(context: models.Db):
    return ProductSaService(context)


def init_category_service(context: models.Db):
    return CategorySaService(context)


def init_order_service(context: models.Db):
    return OrderSaService(context)


OrderService = Annotated[OrderServiceBase, Depends(init_order_service)]

CategoryService = Annotated[CategoryServiceBase, Depends(init_category_service)]

UserService = Annotated[UserServiceBase, Depends(init_user_service)]

ProductService = Annotated[ProductServiceBase, Depends(init_product_service)]
