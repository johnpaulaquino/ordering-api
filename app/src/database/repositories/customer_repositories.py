from sqlalchemy import and_
from sqlmodel import select

from app.logs import Logger
from app.src.database.engine_ import create_session
from app.src.database.models import CustomersAddress
from app.src.database.models.customers import Customer
from app.src.exceptions.app_exceptions import AppException


class CustomerRepository:

     @staticmethod
     async def get_customer_by_id(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(Customer).where(and_(Customer.id == customer_id))
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise AppException

     @staticmethod
     async def create_user(customer: Customer):
          async with create_session() as db:
               try:
                    db.add(customer)
                    await db.commit()
                    await db.refresh(customer)
               except Exception as e:
                    await db.rollback()
                    raise AppException

     @staticmethod
     async def get_customer_by_email(email: str):
          async with create_session() as db:
               try:
                    stmt = select(Customer).where(and_(Customer.email == email))
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    raise AppException

     @staticmethod
     async def insert_customers_address(customer_address: CustomersAddress):
          async with create_session() as db:
               try:
                    db.add(customer_address)
                    await db.commit()
                    await db.refresh(customer_address)
               except Exception as e:
                    await db.rollback()
                    raise AppException

     @staticmethod
     async def get_customer_address(customer_id: int):
          async with create_session() as db:
               try:
                    stmt = select(CustomersAddress).where(CustomersAddress.customer_id == customer_id)
                    result = await db.execute(stmt)
                    data = result.scalar()
                    return data
               except Exception as e:
                    Logger.critical(msg=str(e.__cause__))
                    raise AppException
