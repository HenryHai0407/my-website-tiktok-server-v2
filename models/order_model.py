from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

from models.order_item_model import OrderItemModel, OrderItemDTO
from pydantic import BaseModel


class OrderModel(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_number: str
    customer_id: int
    user_id: Optional[int] = None
    status: str
    description: Optional[str] = None
    items: List["OrderItemModel"] = Relationship(back_populates="order")


class OrderBase(BaseModel):
    customer_id: int
    user_id: Optional[int] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


class OrderDTO(OrderBase):
    id: int
    order_number: str
    status: Optional[str] = None
    total_price: Optional[float] = None
    items: List[OrderItemDTO]


class OrderDTOCreateItem(SQLModel):
    product_id: int
    quantity: int
    unit_price: float
    description: Optional[str] = None


class OrderDTOCreate(OrderBase):
    items: List[OrderDTOCreateItem]
