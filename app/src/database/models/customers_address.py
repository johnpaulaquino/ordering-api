from sqlmodel import Field, SQLModel


class BaseCustomersAddress(SQLModel):

     full_name : str
     phone_number : str
     full_address : str
     postal_code : str

#Inherit all attr from BaseCustomersAddress
class CustomersAddress(BaseCustomersAddress, table= True):

     __tablename__ = 'customers_address'
     id: int = Field(primary_key=True, index=True)
     customer_id : int


class CreateCustomerAddress(BaseCustomersAddress):
     pass