from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.logs import Logger
from app.src.database.models import Carts
from app.src.database.models.carts import CreateCarts
from app.src.database.repositories.carts_repositories import CartsRepository
from app.src.database.repositories.customer_repositories import CustomerRepository
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.exceptions.app_exceptions import AppException, DatabaseDataNotFoundException


class CartsServices:

     @staticmethod
     async def insert_cart(cart: CreateCarts, current_user=Depends(AuthDependency.get_current_user)):
          try:
               customer_id = current_user.id
               total_price = cart.price * cart.quantity
               new_carts = Carts(price=cart.price,
                                 quantity=cart.quantity,
                                 customer_id=customer_id,
                                 product_id=cart.product_id,
                                 total_price=total_price)

               validated_data = jsonable_encoder(new_carts.model_dump())
               await CartsRepository.insert_carts(validated_data)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully Created!'},
               )
          except Exception as e:
               Logger.critical(e.__cause__)
               raise AppException

     @staticmethod
     async def get_customer_carts(current_user=Depends(AuthDependency.get_current_user)):
          try:
               customer_id = current_user.id
               data = await CustomerRepository.get_customer_by_id(customer_id)

               if not data:
                    raise DatabaseDataNotFoundException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            message = 'No customer found',
                            message_status='fail'
                    )

               customer_carts = await CartsRepository.get_customer_carts(data.id)
               if not customer_carts:
                    return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={'status': 'ok', 'message': 'No Carts found',
                                     'data'  : customer_carts, 'total_items': 0})

               total_items = await CartsRepository.get_total_items_in_carts(customer_id)
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status'     : 'ok', 'message': 'Successfully retrieved',
                                'data'       : jsonable_encoder(customer_carts),
                                "total_items": total_items})

          except Exception as e:
               raise e

