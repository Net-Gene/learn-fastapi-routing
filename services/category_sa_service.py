from typing import List
from unittest import skip

from fastapi import Query
from models import Categories, Products
import models
from services.category_service_base import CategoryServiceBase


class CategorySaService(CategoryServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[Categories]:
        return self.context.query(Categories).all()
    
    def get_all_categories_with_products(self, page: int) -> List[Categories]:
        # The page parameter is used to paginate the products, not the categories themselves
        skip = (page - 1) * 2  # Calculate the offset for products

        # Get all categories (no pagination on categories)
        categories = self.context.query(Categories).all()

        categories_with_products = []

        for category in categories:
            # Paginate the products for each category (limit 2 products per page)
            products = self.context.query(Products).filter(Products.CategoryId == category.Id).offset(skip).limit(2).all()

            categories_with_products.append(
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
                        for product in products
                    ],
                }
            )

        return categories_with_products

