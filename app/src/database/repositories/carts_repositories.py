from sqlalchemy import func
from sqlalchemy.dialects.mysql import insert
from sqlmodel import select

from app.logs import Logger
from app.src.database.engine_ import create_session, safe_execute
from app.src.database.models import Carts, Products
from app.src.exceptions.app_exceptions import AppException


class CartsRepository:

     @staticmethod
     async def insert_carts(cart: dict):
          async with create_session() as db:
               try:
                    stmt = insert(Carts).values(cart).on_duplicate_key_update(
                            quantity=Carts.quantity + cart['quantity'],
                            total_price=Carts.total_price + cart['total_price'])
                    await safe_execute(db, stmt)
                    await db.commit()
               except Exception as e:
                    await db.rollback()
                    Logger.critical(msg=f"{e}")
                    raise AppException

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
                    result = await safe_execute(db, stmt)
                    data = result.mappings().all()
                    return data
               except Exception as e:
                    Logger.critical(msg=f"{e}")
                    raise AppException

     @staticmethod
     async def get_total_items_in_carts(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(func.count(Carts.id)).where(Carts.customer_id == customer_id)
                    result = await safe_execute(db, stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    Logger.critical(msg=f"{e}")
                    raise AppException

     @staticmethod
     async def get_customer_total_amount_of_carts(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(func.sum(Carts.total_price)).where(Carts.customer_id == customer_id)
                    result = await safe_execute(db, stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    Logger.critical(msg=f"{e}")
                    raise AppException
