from datetime import datetime
from typing import List

from fastapi import Query
from sqlalchemy import func

from custom_exceptions.missing_field_exception import MissingFieldException
from custom_exceptions.not_found_exception import NotFoundException
from models import Orders, Db, OrdersProducts, Products
from dtos.orders import UpdateOrderDto, OrderReqDto
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
            raise ValueError("Quantity must be greater than 0")

        print(f"Request received: product_id={req.product_id}, quantity={req.quantity}, user_id={req.user_id}")

        with self.context.begin():  # Aloita tapahtuma

            try:
                # Tarkista olemassa oleva odottava tilaus

                order = (
                    self.context.query(Orders)
                    .filter(Orders.CustomerId == req.user_id, Orders.State == "Pending")
                    .first()
                )
                print(f"Order fetched: {order if order else 'No pending order found'}")

                # Luo uusi tilaus, jos sellaista ei ole

                if not order:
                    print("No pending order found. Creating a new order...")
                    order = Orders(
                        CustomerId=req.user_id,
                        CreatedDate=datetime.utcnow().isoformat(),
                        State="Pending",
                    )
                    self.context.add(order)
                    self.context.flush()  # Varmista, että tilaustunnus on luotu

                    print(f"New order created: {order}")

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
                    print(f"Updated existing product in order: {existing_order_product}")
                else:
                    # Lisää uusi tuote OrdersProductsiin

                    order_product = OrdersProducts(
                        OrderId=order.Id,
                        ProductId=req.product_id,
                        UnitCount=req.quantity,
                        UnitPrice=product.UnitPrice,
                    )
                    self.context.add(order_product)
                    print(f"Added new product to order: {order_product}")

                # Laske tilauksen päivitetty kokonaishinta

                total_price = (
                    self.context.query(OrdersProducts)
                    .filter(OrdersProducts.OrderId == order.Id)
                    .with_entities(
                        func.sum(OrdersProducts.UnitCount * OrdersProducts.UnitPrice)
                    )
                    .scalar()
                )
                print(f"Calculated total price: {total_price}")

                self.context.commit()

            except Exception as e:
                self.context.rollback()
                print(f"Error occurred: {e}")
                raise e

        # Palauta päivitetty tilaus kokonaishinnalla (laskettu ulkoisesti)

        order.TotalPrice = total_price
        return order

    def update_order(self, order_id: int, req_data: UpdateOrderDto):
        order = self.context.query(Orders).filter(Orders.Id == order_id).first()

        if order is None:
            return None
        order.OrderName = req_data.ordername
        self.context.commit()
        return order



