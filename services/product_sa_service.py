from typing import List

from fastapi import Query

from custom_exceptions.not_found_exception import NotFoundException
from models import Products
import models
from services.product_service_base import ProductServiceBase


class ProductSaService(ProductServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self, page) -> List[Products]:
        """
        Hae tuotteet sivutus- ja hakutoiminnoilla.
        
        :param page: Sivunumero (alkaen 1:stä).
        :return: Luettelo määritetyn sivun tuotteista.
        """
        try:
            # Rakenna peruskysely

            query: Query = self.context.query(Products)

            # Toteuta sivutus

            query = query.offset((page - 1) * 2).limit(2)

            # Suorita kysely ja palauta tulokset
            result = query.all()

            if result is None:
                raise NotFoundException('Tuotteita ei löydetty')

            return result

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException(e)
