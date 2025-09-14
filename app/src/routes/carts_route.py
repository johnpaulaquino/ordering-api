from fastapi import APIRouter
from fastapi.params import Depends
from sentry_sdk.utils import Auth

from app.src.database.models.carts import CreateCarts
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.services.carts_services import CartsServices

cart_router = APIRouter(
        tags=['Carts'],
        prefix='/api/v1/carts'
)


@cart_router.post('/')
async def insert_cart(cart: CreateCarts, current_user = Depends(AuthDependency.get_current_user)):
     try:
          return await CartsServices.insert_cart(cart,current_user)
     except Exception as e:
          raise e


@cart_router.get('/')
async def get_customer_carts(current_user = Depends(AuthDependency.get_current_user)):
     try:
          return await CartsServices.get_customer_carts(current_user)
     except Exception as e:
          raise e
