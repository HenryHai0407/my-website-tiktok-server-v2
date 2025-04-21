from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional, List
from models.product_model import ProductDTO, ProductModel


class CategoryModel(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    products: List["ProductModel"] = Relationship(back_populates="category")


class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class CategoryDTO(CategoryBase):
    id: int
    products: List["ProductDTO"]


class CategoryDTOCreate(CategoryBase):
    pass


class CategoryDTOUpdate(CategoryBase):
    pass
