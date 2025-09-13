from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class BaseProducts(SQLModel):
     product_id: str
     product_photo: Optional[str] = Field(default=None)
     product_name: str
     category: str
     stocks: int
     price: float
     expiration_date: date
     status: str


class Products(BaseProducts, table=True):
     __tablename__ = 'products'
     id: int = Field(primary_key=True, index=True)
     batch_tracking: Optional[bool] = Field(default=True)
     created_from_production: bool = Field(default=False)
     created_by: int = Field(default=None)
     production_reference: Optional[str] = None
     created_at: datetime = Field(sa_column=Column(DateTime(timezone=True),server_default=func.now()))
     updated_at: datetime


class CreateProducts(BaseProducts):
     pass


class StocksSchema(BaseModel):
     id: int
     p_id: str
     quantity: int
