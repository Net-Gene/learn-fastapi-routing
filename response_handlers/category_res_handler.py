


from typing import Annotated

from fastapi import Depends
from models import Categories


class CategoryResHandler:
    def send(self, category):
        return Categories(id=category.Id, name=category.Name, unit_price=category.UnitPrice,  description=category.Description)


def init_category_response_handler():
    return CategoryResHandler()


CategoryResResponseHandler = Annotated[CategoryResHandler, Depends(init_category_response_handler)]
