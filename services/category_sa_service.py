from typing import List, Dict, Any

import models
from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.taken_exception import TakenException
from dtos.categories import AddCategoryDtoReq, UpdateCategoryDtoReq
from models import Categories, Products
from services.category_service_base import CategoryServiceBase


class CategorySaService(CategoryServiceBase):
    def __init__(self, context: models.Db):
        self.context = context

    def get_all(self) -> List[Dict[str, Any]]:
        categories = (self.context
                      .query(Categories)
                      .all())
        categories_dict = [
            {
                "Id": category.Id,
                "Name": category.Name,
                "Description": category.Description,
            }
            for category in categories
        ]
        return categories_dict

    def get_all_categories_with_products(self, page: int, category_id: int) -> List[Dict[str, Any]]:
        try:
            # Sivuparametria käytetään tuotteiden sivuttamiseen, ei itse luokkiin

            _skip = (page - 1) * 2  # Laske tuotteiden offset

            # Hae luokka, jonka id on sama kuin category_id

            category = (
                self.context.query(Categories)
                .filter(Categories.Id == category_id)
                .first()
            )
            if category is None:
                raise NotFoundException(f"Kategoriaa, jonka id olisi ${category_id} ei löydetty")

            category_with_products = []

            # Sivuttele kunkin luokan tuotteet (enintään 2 tuotetta sivulla)

            products = self.context.query(Products).filter(Products.CategoryId == category.Id).offset(_skip).limit(
                2).all()
            if not products:  # Tarkista, onko tulos tyhjä
                raise NotFoundException(f"Tuotteita ei löytynyt kategoriasta")

            category_with_products.append(
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

            return category_with_products

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten TakenException

            print(f"Virhe: {e}")
            raise NotFoundException(e)

    def add(self, req: AddCategoryDtoReq, user) -> Categories:
        try:
            category_exists = self.context.query(Categories).filter(Categories.Name == req.name).first()

            if category_exists is not None:
                raise TakenException('Luokan nimi on jo varattu')

            category = Categories(
                Name=req.name,
                Description=req.description,
                UserId=user.Id
            )

            self.context.add(category)
            self.context.commit()
            return category

        except TakenException as e:
            # Käsittele erityisiä poikkeuksia, kuten TakenException

            print(f"Virhe: {e}")
            raise TakenException(e)

    def update(self, req: UpdateCategoryDtoReq, category_id: int):
        # Hae kategoria tarkistaaksesi, onko se olemassa ja kuuluuko se kirjautuneelle käyttäjälle
        try:
            print("category_id =", category_id)
            category = (
                self.context.query(Categories)
                .filter(Categories.Id == category_id)
                .first()
            )
            category_with_same_name = (
                self.context.query(Categories)
                .filter(Categories.Name == req.name)
                .first()
            )
            if not category:
                raise NotFoundException("Kategoriaa ei löytynyt.")

            if category_with_same_name is not None:
                raise ForbiddenException("Kategorian nimi on jo varattu.")

            category.Name = req.name
            category.Description = req.description

            self.context.commit()

            return {"message": "Kategorian nimi ja kuvaus päivitys onnistui",
                    "category_id": category_id,
                    "Uusi nimi kategorialle": req.name,
                    "Uusi kuvaus kategorialle": req.description}

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException
            print(f"Virhe: {e}")

            raise NotFoundException(e)

        except ForbiddenException as e:
            # Käsittele erityisiä poikkeuksia, kuten ForbiddenException
            print(f"Virhe: {e}")

            raise ForbiddenException(e)
