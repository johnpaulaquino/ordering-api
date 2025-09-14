from typing import List

from sqlalchemy import bindparam
from sqlmodel import update

from app.src.database.engine_ import create_session
from app.src.database.models import Products


class ProductRepository:

     @staticmethod
     async def update_products_stocks(values: List[dict]):
          """
          To update stocks products after orders.


          For now this case is solved via Trigger on sql.
          :param values:
          :return:
          """
          async with create_session() as db:
               try:
                    stmt = (
                            update(Products)
                            .where(Products.product_id == bindparam("p_id"))
                            .values(stocks=Products.stocks - bindparam("quantity"))
                              .execution_options(synchronize_session=False))

                    await db.execute(stmt,values)
                    await db.commit()

               except Exception as e:
                    await db.rollback()
                    raise e
