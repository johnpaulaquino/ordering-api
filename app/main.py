import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.logs import Logger
from app.src.exceptions.app_exceptions import AppException
from app.src.exceptions.exceptions_handler import create_exception_handler
from app.src.routes.auth_route import auth_router
from app.src.routes.carts_route import cart_router
from app.src.routes.customers_route import customers_router
from app.src.routes.order_route import order_router
from app.src.routes.products_route import products_router

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"], )
app.add_exception_handler(
        handler=create_exception_handler(), exc_class_or_status_code=AppException, )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
     validation_error = exc.errors()[0]
     Logger.error(f'{validation_error['msg']} for {validation_error['loc'][1]}')
     return JSONResponse(
             status_code=422,
             content={"status" : "error",
                      "details": {'type'    : validation_error['type'],
                                  'location': validation_error['loc'][1],
                                  'message' : validation_error['msg']}})


app.include_router(cart_router)
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(customers_router)

if __name__ == '__main__':

     uvicorn.run('main:app', reload=True, host='0.0.0.0', port=9090)
