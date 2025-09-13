from fastapi import APIRouter, HTTPException, status
from starlette.responses import JSONResponse

from app.src.database.models import CustomersAddress
from app.src.database.models.customers_address import CreateCustomerAddress
from app.src.database.repositories.customer_repositories import CustomerRepository

customers_router = APIRouter(
        tags=['Customers']
)


@customers_router.post('/customer/address/{customer_id}')
async def insert_customer_address(customer_id: int, customer_address: CreateCustomerAddress):
     try:
          customer_data = await CustomerRepository.get_customer_by_id(customer_id)
          if not customer_data:
               raise HTTPException(
                       status_code=status.HTTP_404_NOT_FOUND,
                       detail={'status': 'failed', 'message': 'User not found'}
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
