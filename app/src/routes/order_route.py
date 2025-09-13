from typing import List

from fastapi import APIRouter, Depends

from app.src.database.models.orders import CreateOrders
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.services.order_services import OrderServices

order_router = APIRouter(
        tags=['Orders']
)


@order_router.post('/orders/batch')
async def place_orders_in_cart(orders: List[CreateOrders], current_user=Depends(AuthDependency.get_current_user)):
     try:
          return await OrderServices.insert_orders(orders, current_user)
     except Exception as e:
          raise e


@order_router.post('/order')
async def buy_specific_product():
     try:
          pass
     except Exception as e:
          raise e
