from http.client import responses
from typing import List

from fastapi import APIRouter, Depends

from app.logs import Logger
from app.src.database.models.orders import CreateOrders
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.exceptions.app_exceptions import AppException
from app.src.services.order_services import OrderServices

order_router = APIRouter(
        tags=['Orders'],
        prefix='/api/v1/order'

)


@order_router.post('/batch')
async def place_orders_in_cart(orders: List[CreateOrders], current_user=Depends(AuthDependency.get_current_user)):
     try:

          response =  await OrderServices.insert_orders(orders, current_user)
          Logger.info('Successfully added orders')
          return response
     except Exception as e:
          if not isinstance(e, AppException):
               Logger.critical(msg=f"{e}")
          raise e

#
# @order_router.post('/')
# async def buy_specific_product():
#      try:
#           pass
#      except Exception as e:
#           raise e
