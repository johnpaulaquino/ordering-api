from typing import List

from app.logs import Logger
from app.src.database.engine_ import create_session, safe_commit
from app.src.database.models.orders import Orders
from app.src.exceptions.app_exceptions import AppException


class OrderRepository:
     @staticmethod
     async def insert_orders(orders: List[Orders]):
          async with create_session() as db:
               try:
                    db.add_all(orders)
                    await safe_commit(db)
               except Exception as e:
                    # rollback if encountered error
                    await db.rollback()
                    Logger.critical(msg=f"{e}")
                    raise AppException
