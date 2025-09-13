from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseCustomer(SQLModel):
     username: str
     email: str
     phone_number: str
     password: str


class Customer(BaseCustomer, table=True):
     __tablename__ = 'customers'
     id: int = Field(primary_key=True, index=True)
     created_at: datetime


class CreateCustomer(BaseCustomer):
     password: str
     pass
