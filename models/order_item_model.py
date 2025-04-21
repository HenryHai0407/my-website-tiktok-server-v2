from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from pydantic import BaseModel
# from models.order_model import OrderModel


class OrderItemModel(SQLModel, table=True):
    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    product_id: int = Field(foreign_key="products.id")

    quantity: int
    unit_price: float
    description: Optional[str] = None

    delete_flg: bool = False

    order: "OrderModel" = Relationship(back_populates="items")


class OrderItemDTO(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: Optional[float] = None
    description: Optional[str]

    class Config:
        from_attributes = True
