from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert
from sqlmodel import select

from app.src.database.engine_ import create_session
from app.src.database.models import Carts, Products


class CartsRepository:

     @staticmethod
     async def insert_carts(cart: dict):
          async with create_session() as db:
               try:

                    stmt = insert(Carts).values(cart).on_duplicate_key_update(
                            quantity=Carts.quantity + cart['quantity'],
                            total_price=Carts.total_price + cart['total_price'])
                    await db.execute(stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def get_customer_carts(customer_id: int):
          async with (create_session() as db):
               try:
                    stmt = (select(Products.id,
                                   Carts.product_id,
                                   Products.product_photo,
                                   Products.product_name,
                                   Carts.price,
                                   Carts.quantity)
                            .outerjoin(Carts, Products.product_id == Carts.product_id)
                            .where(Carts.customer_id == customer_id))
                    result = await db.execute(stmt)
                    data = result.mappings().all()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def get_total_items_in_carts(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(func.count(Carts.id)).where(Carts.customer_id == customer_id)
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise e

     @staticmethod
     async def get_customer_total_amount_of_carts(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(func.sum(Carts.total_price)).where(Carts.customer_id == customer_id)
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise e
