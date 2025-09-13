from typing import List

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.src.database.models.products import StocksSchema
from app.src.database.repositories.products_repository import ProductRepository

products_router = APIRouter(
        tags=['Products']
)


@products_router.put('/products')
async def update_products_stocks(values: List[StocksSchema]):
     try:
          await ProductRepository.update_products_stocks(jsonable_encoder(values))
     except Exception as e:
          raise e
