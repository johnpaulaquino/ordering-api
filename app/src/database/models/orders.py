from datetime import date, datetime

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from app.src.database.models.enum_class import OrderStatus, PaymentMethod


class BaseOrders(SQLModel):
     product_id: str
     order_id: str
     customer_name: str
     customer_email: str
     customer_phone: str
     shipping_address: str
     payment_method: str = PaymentMethod.COD.value
     subtotal: float
     tax: int
     discount: int
     notes: str
     quantity: int


class Orders(BaseOrders, table=True):
     id: int = Field(primary_key=True, index=True)
     order_date: date = Field(default=date.today())
     status: str = OrderStatus.PENDING.value
     total_amount: float
     created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now()))
     updated_at: datetime
     customer_id: int


class CreateOrders(BaseOrders):
     pass
