from sqlalchemy import func
from sqlmodel import select

from app.src.database.engine_ import create_session
from app.src.database.models import Carts


class CartsRepository:

     @staticmethod
     async def insert_carts(cart: Carts):
          async with create_session() as db:
               try:
                    db.add(cart)
                    await db.commit()
                    await db.refresh(cart)
               except Exception as e:
                    await db.rollback()
                    raise e

     @staticmethod
     async def get_customer_carts(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(Carts).where(Carts.customer_id == customer_id)
                    result = await db.execute(stmt)
                    data = result.scalars().all()
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