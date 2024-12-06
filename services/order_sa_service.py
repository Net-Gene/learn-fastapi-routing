from datetime import datetime
from typing import List

from fastapi import Query, HTTPException
from sqlalchemy import func

from custom_exceptions.forbidden_exception import ForbiddenException
from custom_exceptions.general_exception import GeneralException
from custom_exceptions.not_found_exception import NotFoundException
from custom_exceptions.taken_exception import TakenException
from dtos.orders import UpdateOrderReqDto, OrderReqDto, OrderingReqDto
from models import Orders, Db, OrdersProducts, Products
from services.order_service_base import OrderServiceBase


class OrderSaService(OrderServiceBase):
    def __init__(self, context: Db):
        self.context = context

    def get_all(self, page) -> List[Orders]:
        """
        Hae tuotteet sivutus-ja hakutoiminnoilla.

        :param page: Sivunumero (alkaen 1:stä).
        :return: Luettelo määritetyn sivun tuotteista.
        """

        # Rakenna peruskysely

        query: Query = self.context.query(Orders)

        # Toteuta sivutus

        query = query.offset((page - 1) * 2).limit(2)

        # Suorita kysely ja palauta tulokset

        return query.all()

    def add_to(self, req: OrderReqDto) -> Orders:
        # Vahvista syötteet

        if not req.product_id or not req.quantity or not req.user_id:
            raise NotFoundException()
        if req.quantity <= 0:
            raise ValueError("Määrän on oltava suurempi kuin 0")

        print(f"Pyyntö vastaanotettu: product_id={req.product_id}, quantity={req.quantity}, user_id={req.user_id}")

        with self.context.begin():  # Aloita tapahtuma

            try:
                # Luo käyttäjälle uusi tilaus

                print("Luodaan uusi tilaus...")
                order = Orders(
                    CustomerId=req.user_id,
                    CreatedDate=datetime.utcnow().isoformat(),
                    State="Pending",  # Muista asettaa tilaksi "Odottaa"

                )
                self.context.add(order)
                self.context.flush()  # Varmista, että tilaustunnus on luotu

                print(f"Uusi tilaus luotu: {order}")

                # Vahvista tuotteen olemassaolo

                product = self.context.query(Products).filter(Products.Id == req.product_id).first()
                if not product:
                    raise NotFoundException()

                # Tarkista, onko tuote jo tilauksessa

                existing_order_product = (
                    self.context.query(OrdersProducts)
                    .filter(
                        OrdersProducts.OrderId == order.Id,
                        OrdersProducts.ProductId == req.product_id,
                    )
                    .first()
                )

                if existing_order_product:
                    # Päivitä nykyisen merkinnän yksikkömäärä

                    existing_order_product.UnitCount += req.quantity
                    print(f"Päivitetty olemassa oleva tuote järjestyksessä: {existing_order_product}")
                else:
                    # Lisää uusi tuote OrdersProductsiin

                    order_product = OrdersProducts(
                        OrderId=order.Id,
                        ProductId=req.product_id,
                        UnitCount=req.quantity,
                        UnitPrice=product.UnitPrice,
                    )
                    self.context.add(order_product)
                    print(f"Lisätty uusi tuote tilaukseen: {order_product}")

                # Laske tilauksen päivitetty kokonaishinta

                total_price = (
                    self.context.query(OrdersProducts)
                    .filter(OrdersProducts.OrderId == order.Id)
                    .with_entities(
                        func.sum(OrdersProducts.UnitCount * OrdersProducts.UnitPrice)
                    )
                    .scalar()
                )
                print(f"Laskettu kokonaishinta: {total_price}")

                # Sitoudu muutokset

                self.context.commit()

            except Exception as e:
                self.context.rollback()
                print(f"Tapahtui virhe: {e}")
                raise e

        # Palauta päivitetty tilaus kokonaishinnalla (laskettu ulkoisesti)

        order.TotalPrice = total_price
        return order

    def delete(self, order_id, user) -> dict[str, str]:
        """
        Poista kaikki tuotteet tilauksesta ja päivitä RemovedDate Tilaukset-taulukossa.
        """
        try:
            # Hae kaikki asiaan liittyvät orderProducts

            order_products = (
                self.context.query(OrdersProducts)
                .filter(OrdersProducts.OrderId == order_id)
                .all()
            )

            print("Hae liittyvät tilaustuotteet: order_products", order_products)

            if not order_products:
                raise NotFoundException("Vastaavia tilaustuotteita ei löytynyt.")

            # Poista kaikki orderProducts tilauksesta

            for order_product in order_products:
                print(f"Deleting order_product with id: {order_product.OrderId}")  # Kirjaa poisto

                self.context.delete(order_product)

            # Päivitä RemovedDate ja State Orders-taulukossa

            order = (
                self.context.query(Orders)
                .filter(Orders.Id == order_id)
                .first()
            )

            if not order:
                raise NotFoundException("Tilausta ei löytynyt.")

            print(f"Updating RemovedDate ja State for order with id: {order_id}")
            order.RemovedDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order.State = "Removed"
            order.HandlerId = user.Id
            # Tee kaikki muutokset kerralla

            self.context.commit()

            return {"Viesti": f"Tilaus, jonka id on {order_id}, on poistettu."}

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException()

        except ValueError as e:
            # Käsittele ValueError-poikkeuksia

            print(f"ValueError: {e}")
            raise TakenException("Invalid data provided.")

        except Exception as e:
            # Yleinen poikkeuskäsittely enemmän kirjaamalla

            print(f"Odottamaton virhe: {e}")
            raise GeneralException()

    def update_order(self, order_id: int, req: UpdateOrderReqDto, user):
        # Hae tilaus tarkistaaksesi, onko se olemassa ja kuuluuko se kirjautuneelle käyttäjälle

        order = (
            self.context.query(Orders)
            .filter(Orders.Id == order_id)
            .first()
        )
        if not order:
            raise NotFoundException()

        # Tarkista, kuuluuko tilaus sisäänkirjautuneelle käyttäjälle

        if order.CustomerId != user.Id:
            raise ForbiddenException()

        order_product = (
            self.context.query(OrdersProducts)
            .filter(OrdersProducts.OrderId == order_id, OrdersProducts.ProductId == req.product_id)
            .first()
        )
        if not order_product:
            raise NotFoundException()  # Jos tilattua tuotetta ei ole olemassa

        order_product.UnitCount = req.unit_count
        self.context.commit()

        return {"message": "Tuotteen määrän päivitys onnistui", "order_id": order_id,
                "product_id": req.product_id, "unit_count": req.unit_count}

    def order(self, req: OrderingReqDto, user) -> dict[str, str]:
        """
        Ostoskorin tavaroiden "tilaaminen"
        """
        try:
            # Hae kaikki asiaan liittyvät orderProducts

            order_products = (
                self.context.query(OrdersProducts)
                .filter(OrdersProducts.OrderId == req.order_id)
                .all()
            )

            print("Hae liittyvät tilaustuotteet: order_products", order_products)

            if not order_products:
                raise NotFoundException("Vastaavia tilaustuotteita ei löytynyt.")

            order = (
                self.context.query(Orders)
                .filter(Orders.Id == req.order_id)
                .first()
            )

            if order.CustomerId != user.Id:
                raise ForbiddenException()

            # Poista kaikki orderProducts tilauksesta

            for order_product in order_products:
                print(f"Deleting order_product with id: {order_product.OrderId}")  # Kirjaa poisto

                self.context.delete(order_product)

            # Päivitä RemovedDate ja State Orders-taulukossa

            order = (
                self.context.query(Orders)
                .filter(Orders.Id == req.order_id)
                .first()
            )

            if not order:
                raise NotFoundException("Tilausta ei löytynyt.")

            print(f"Updating RemovedDate ja State for order with id: {req.order_id}")
            order.ConfirmedDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            order.State = "Ordered"
            order.HandlerId = user.Id

            # Tee kaikki muutokset kerralla

            self.context.commit()

            return {"Viesti": f"Tilaus, jonka id on {req.order_id}, on tilattu."}

        except NotFoundException as e:
            # Käsittele erityisiä poikkeuksia, kuten NotFoundException

            print(f"Virhe: {e}")
            raise NotFoundException()

        except ValueError as e:
            # Käsittele ValueError-poikkeuksia

            print(f"ValueError: {e}")
            raise TakenException("Invalid data provided.")

        except Exception as e:
            # Yleinen poikkeuskäsittely enemmän kirjaamalla

            print(f"Odottamaton virhe: {e}")
            raise GeneralException()
