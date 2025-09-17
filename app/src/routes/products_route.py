from fastapi import APIRouter

products_router = APIRouter(
        tags=['Products'],
)

#
# @products_router.put('/products')
# async def update_products_stocks(values: List[StocksSchema]):
#      try:
#           return jsonable_encoder(await CartsRepository.get_customer_carts(1))
#      except Exception as e:
#
#           raise e
