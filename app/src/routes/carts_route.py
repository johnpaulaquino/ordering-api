from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.params import Depends

from app.logs import Logger
from app.src.database.models.carts import CreateCarts
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.exceptions.app_exceptions import AppException
from app.src.services.carts_services import CartsServices

cart_router = APIRouter(
        tags=['Carts'],
        prefix='/api/v1/carts',
)


@cart_router.post('/')
async def insert_cart(cart: CreateCarts, current_user=Depends(AuthDependency.get_current_user)):
     try:
          response = await CartsServices.insert_cart(cart, current_user)
          Logger.info('Successfully added cart')
          return response
     except Exception as e:
          raise e


@cart_router.get('/')
async def get_customer_carts(current_user=Depends(AuthDependency.get_current_user)):
     try:
          response =  await CartsServices.get_customer_carts(current_user)
          Logger.info('Successfully retrieve cart')
          return response
     except Exception as e:
          if not isinstance(e, AppException):
               Logger.critical(msg=f"{e}")
          raise e
