from fastapi import status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.src.database.models import CustomersAddress
from app.src.database.models.customers_address import CreateCustomerAddress
from app.src.database.repositories.customer_repositories import CustomerRepository
from app.src.exceptions.app_exceptions import DatabaseDataNotFoundException


class CustomerServices:

     @staticmethod
     async def insert_customer_address(customer_address: CreateCustomerAddress, current_user):
          try:
               customer_id = current_user.id
               customer_data = await CustomerRepository.get_customer_by_id(customer_id)
               if not customer_data:
                    raise DatabaseDataNotFoundException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            message='User not found',
                            message_status='fail',
                    )
               customers_address = CustomersAddress(
                       customer_id=customer_address.customer_id,
                       full_address=customer_address.full_address,
                       full_name=customer_address.full_name,
                       postal_code=customer_address.postal_code,
                       phone_number=customer_address.phone_number,
               )
               await CustomerRepository.insert_customers_address(customers_address)
               return JSONResponse(
                       status_code=status.HTTP_201_CREATED,
                       content={'status': 'ok', 'message': 'Successfully created'})
          except Exception as e:
               raise e

     @staticmethod
     async def get_customer_address(current_user):
          try:
               customer_id = current_user.id
               data = await CustomerRepository.get_customer_address(customer_id)

               if not data:
                    return JSONResponse(
                            status_code=status.HTTP_200_OK,
                            content={'status': 'ok', 'message': 'No data to retrieve',
                                     'dat'   : []})
               return JSONResponse(
                       status_code=status.HTTP_200_OK,
                       content={'status': 'ok', 'message': 'Successfully retrieved',
                                'dat'   : jsonable_encoder(data)},
               )
          except Exception as e:
               raise e

