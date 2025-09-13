from fastapi import Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.src.database.models import Carts
from app.src.database.models.carts import CreateCarts
from app.src.database.repositories.carts_repositories import CartsRepository
from app.src.database.repositories.customer_repositories import CustomerRepository
from app.src.dependencies.auth_dependency import AuthDependency


class CartsServices:

     @staticmethod
     async def insert_cart(cart: CreateCarts,current_user = Depends(AuthDependency.get_current_user)):
          try:
               customer_id = current_user.id
               total_price = cart.price * cart.quantity
               new_carts = Carts(price=cart.price,
                                 quantity=cart.quantity,
                                 customer_id=customer_id,
                                 product_id=cart.product_id,
                                 total_price=total_price)

               await CartsRepository.insert_carts(new_carts)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully Created!'},
               )
          except Exception as e:
               raise e

     @staticmethod
     async def get_customer_carts(get_current_user=Depends(AuthDependency.get_current_user)):
          try:
               customer_id = get_current_user.id
               data = await CustomerRepository.get_customer_by_id(customer_id)

               if not data:
                    raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail={'status': 'failed', 'message': 'No customer found'},
                    )

               customer_carts = await CartsRepository.get_customer_carts(data.id)
               if not customer_carts:
                    return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={'status': 'ok', 'message': 'No Carts found',
                                     'data'  : customer_carts}, )
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully retrieved',
                                'data'  : jsonable_encoder(customer_carts)})

          except Exception as e:
               raise e
