from typing import List
from models import Products
import models
from services.product_service_base import ProductServiceBase


class ProductSaService(ProductServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[Products]:
        return self.context.query(Products).all()

