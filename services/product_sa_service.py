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

        # Rakenna peruskysely

        query: Query = self.context.query(Products)

        # Toteuta sivutus

        query = query.offset((page - 1) * 2).limit(2)

        # Suorita kysely ja palauta tulokset

        return query.all()
