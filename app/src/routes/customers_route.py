from fastapi import APIRouter, Depends

from app.logs import Logger
from app.src.database.models.customers_address import CreateCustomerAddress
from app.src.dependencies.auth_dependency import AuthDependency
from app.src.exceptions.app_exceptions import AppException
from app.src.services.customer_services import CustomerServices

customers_router = APIRouter(
        tags=['Customers'],
        prefix='/api/v1/customer',

)


@customers_router.post('/address')
async def insert_customer_address(customer_address: CreateCustomerAddress,
                                  current_user=Depends(AuthDependency.get_current_user)):
     try:

          response = await CustomerServices.insert_customer_address(customer_address, current_user)
          Logger.info('Successfully added customer address')
          return response
     except Exception as e:

          raise e


@customers_router.get('/')
async def get_customer_address(current_user=Depends(AuthDependency.get_current_user)):
     try:
          response = await CustomerServices.get_customer_address(current_user)
          Logger.info('Successfully retrieve customer address')
          return response
     except Exception as e:
          if not isinstance(e, AppException):
               Logger.critical(msg=f"{e}")
          raise e
