from typing import Any, Callable, Coroutine

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.src.exceptions.app_exceptions import AppException


def create_exception_handler():
     async def exception_handler(_: Request, exc: AppException):
          detail = {'message': exc.message,
                    'status' : exc.message_status}
          if not exc.headers:

               return JSONResponse(
                  status_code=exc.status_code,
                  content= detail
               )
          return JSONResponse(
                  status_code=exc.status_code,
                  content=detail,
                  headers=exc.headers
          )
     return exception_handler
