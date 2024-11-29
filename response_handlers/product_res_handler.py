


from typing import Annotated

from fastapi import Depends
from models import Products


class ProductResHandler:
    def send(self, product):
        return Products(id=product.Id, name=product.Name, unit_price=product.UnitPrice,  description=product.Description)


def init_product_response_handler():
    return ProductResHandler()


ProductResResponseHandler = Annotated[ProductResHandler, Depends(init_product_response_handler)]
