import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.src.routes.auth_route import auth_router
from app.src.routes.carts_route import cart_router
from app.src.routes.customers_route import customers_router
from app.src.routes.order_route import order_router
from app.src.routes.products_route import products_router

app = FastAPI()

app.include_router(cart_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(customers_router)


app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"])

if __name__ == '__main__':

     uvicorn.run('main:app', reload=True, host='0.0.0.0', port=9090)
