from typing import List

from fastapi import status
from starlette.responses import JSONResponse

from app.src.database.models.orders import CreateOrders, Orders
from app.src.database.repositories.order_repositories import OrderRepository


class OrderServices:

     @staticmethod
     async def insert_orders(orders_: List[CreateOrders], current_user):
          try:
               customer_id = current_user.id
               list_of_orders: List[Orders] = []

               total_amount  = 0 #calculate total amount
               for value in orders_:
                    # set values for orders
                    order = Orders(order_id=value.order_id,
                                   customer_id=customer_id,
                                   product_id=value.product_id,
                                   tax=value.tax,
                                   quantity=value.quantity,
                                   shipping_address=value.shipping_address,
                                   customer_email=value.customer_email,
                                   customer_name=value.customer_name,
                                   discount=value.discount,
                                   notes=value.notes,
                                   total_amount = total_amount,
                                   customer_phone=value.customer_phone,
                                   payment_method=value.payment_method,
                                   subtotal=value.subtotal)
                    # append orders
                    list_of_orders.append(order)

               # insert in database
               await OrderRepository.insert_orders(list_of_orders)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Success placed order(s)'},
               )
          except Exception as e:
               raise e
