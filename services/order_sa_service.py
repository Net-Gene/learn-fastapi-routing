from datetime import datetime
from typing import List, Dict

from fastapi import Query, HTTPException
from sqlalchemy import func

from custom_exceptions.missing_field_exception import MissingFieldException
from custom_exceptions.not_found_exception import NotFoundException
from models import Orders, Db, OrdersProducts, Products
from dtos.orders import UpdateOrderDto, OrderReqDto, DeleteOrderReqDto
from services.order_service_base import OrderServiceBase


class OrderSaService(OrderServiceBase):
    def __init__(self, context: Db):
        self.context = context

    def get_all(self, page) -> List[Orders]:
        """
        Hae tuotteet sivutus-ja hakutoiminnoilla.

        :param page: Sivunumero (alkaen 1:stä).
        :param page_size: Tuotteiden määrä sivua kohden (oletus 2).
        :param-haku: merkkijono, jonka avulla voit etsiä tuotteita nimellä (valinnainen).
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
            raise MissingFieldException()
        if req.quantity <= 0:
            raise ValueError("Määrän on oltava suurempi kuin 0")

        print(f"Pyyntö vastaanotettu: product_id={req.product_id}, quantity={req.quantity}, user_id={req.user_id}")

        with self.context.begin():  # Aloita tapahtuma

            try:
                # Create a new order for the user
                print("Luodaan uusi tilaus...")
                order = Orders(
                    CustomerId=req.user_id,
                    CreatedDate=datetime.utcnow().isoformat(),
                    State="Pending",  # Make sure to set the state as "Pending"
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

                # Commit the changes
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
                print(f"Deleting order_product with id: {order_product.OrderId}")  # Log the deletion
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
            # Commit all changes at once
            self.context.commit()

            return {"Viesti": f"Tilaus, jonka id on {order_id}, on poistettu."}

        except NotFoundException as e:
            # Handle specific exceptions like NotFoundException
            print(f"Error: {e}")
            raise HTTPException(status_code=404, detail=str(e))

        except ValueError as e:
            # Handle ValueError exceptions
            print(f"ValueError: {e}")
            raise HTTPException(status_code=400, detail="Invalid data provided.")

        except Exception as e:
            # General exception handling with more logging
            print(f"Unexpected error: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update_order(self, order_id: int, req_data: UpdateOrderDto):
        order = self.context.query(Orders).filter(Orders.Id == order_id).first()

        if order is None:
            return None
        order.OrderName = req_data.ordername
        self.context.commit()
        return order
