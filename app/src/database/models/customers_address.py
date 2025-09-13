from sqlmodel import Field, SQLModel


# create table customers_address(
# id int PRIMARY KEY AUTO_INCREMENT,
# customer_id int,
# full_name varchar(255) not null,
# phone_number varchar(20),
# full_address varchar(255),
# postal_code varchar(255),
# FOREIGN KEY(customer_id) REFERENCES customers(id)
# ON DELETE CASCADE
# );

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