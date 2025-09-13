from datetime import datetime

from sqlalchemy import func
from sqlmodel import Column, DateTime, Field, SQLModel


class BaseCarts(SQLModel):
     product_id: str = Field(nullable=False)
     quantity: int = Field(nullable=False)
     price: float = Field(nullable=False)



class Carts(BaseCarts, table=True):
     __tablename__ = 'carts'
     id: int = Field(primary_key=True, index=True)
     customer_id: int = Field(nullable=False)
     total_price: float = Field(nullable=False)
     created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),
                                                   server_default=func.now()))


class CreateCarts(BaseCarts):
     pass
