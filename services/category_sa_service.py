from typing import List
from models import Categories
import models
from services.category_service_base import CategoryServiceBase


class CategorySaService(CategoryServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[Categories]:
        return self.context.query(Categories).all()
    
    def get_all_categories_with_products(self) -> List[Categories]:
        categories = self.context.query(Categories).all()
        return [
            {
                "id": category.Id,
                "name": category.Name,
                "description": category.Description,
                "products": [
                    {
                        "id": product.Id,
                        "name": product.Name,
                        "description": product.Description,
                        "unit_price": product.UnitPrice,
                    }
                    for product in category.Products
                ],
            }
            for category in categories
        ]

