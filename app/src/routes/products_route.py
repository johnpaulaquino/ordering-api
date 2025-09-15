from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.logs import Logger
from app.src.database.models.products import StocksSchema
from app.src.database.repositories.products_repository import ProductRepository
from app.src.exceptions.app_exceptions import AppException, DatabaseDataNotFoundException

products_router = APIRouter(
        tags=['Products']
)


# @products_router.put('/products')
# async def update_products_stocks(values: List[StocksSchema]):
#      try:
#           raise DatabaseDataNotFoundException(status_code=404,
#                                               message='Not Found')
#      except Exception as e:
#           Logger.info('hey')
#           raise e
