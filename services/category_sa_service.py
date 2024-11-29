from typing import List
from models import Categories
import models
from services.category_service_base import CategoryServiceBase


class CategorySaService(CategoryServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[Categories]:
        return self.context.query(Categories).all()
    

