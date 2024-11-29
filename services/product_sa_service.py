from typing import List

from fastapi import Query
from models import Products
import models
from services.product_service_base import ProductServiceBase


class ProductSaService(ProductServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self, page) -> List[Products]:
        """
        Hae tuotteet sivutus-ja hakutoiminnoilla.
        
        :param page: Sivunumero (alkaen 1:stä).
        :param page_size: Tuotteiden määrä sivua kohden (oletus 2).
        :param-haku: merkkijono, jonka avulla voit etsiä tuotteita nimellä (valinnainen).
        :return: Luettelo määritetyn sivun tuotteista.
        """
        
        # Build the base query
        query: Query = self.context.query(Products)

        # Implement pagination
        query = query.offset((page - 1) * 2).limit(2)

        # Execute the query and return the results
        return query.all()