from sqlmodel import SQLModel

from app.src.database.models.carts import Carts
from app.src.database.models.customers import Customer
from app.src.database.models.customers_address import CustomersAddress
from app.src.database.models.orders import Orders
from app.src.database.models.products import Products

Base = SQLModel()

__all__ = ["Base",
           "Products",
           "Customer",
           "Carts",
           "Orders",
           "CustomersAddress"]
