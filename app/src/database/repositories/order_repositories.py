from typing import List

from fastapi.encoders import jsonable_encoder

from app.src.database.engine_ import create_session
from app.src.database.models.orders import CreateOrders, Orders
from app.src.database.models.products import StocksSchema
from app.src.database.repositories.products_repository import ProductRepository


class OrderRepository:
     @staticmethod
     async def insert_orders(orders: List[Orders]):
          async with create_session() as db:
               try:
                    db.add_all(orders)
                    #to get the latest data in db while not commiting in db,
                    # so that when there is an error it will not automatically
                    # save in database
                    await db.flush()
                    # to_update = []
                    # for value in orders:
                    #      #skip for now
                    #      products_stocks_ = StocksSchema(id=value.id,
                    #                                      p_id=value.product_id,
                    #                                      quantity=value.quantity)
                    #      to_update.append(products_stocks_)
                         #update
                   #commit the transaction
                    await db.commit()
                    #update the stocks in products
                    # await ProductRepository.update_products_stocks(jsonable_encoder(to_update))
               except Exception as e:
                    #rollback if encountered error
                    await db.rollback()
                    raise e

