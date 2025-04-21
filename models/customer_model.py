from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional
from .auth_model import AuthModel


class CustomerModel(SQLModel, table=True):
    __tablename__ = "customers"

    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str
    first_name: str
    phone_number: str
    email: str
    address: str

    auth_id: int = Field(foreign_key="auth.id", unique=True)
    auth: AuthModel = Relationship()


class CustomerBase(BaseModel):
    last_name: str
    first_name: str
    phone_number: str
    email: str
    address: str

    class Config:
        from_attributes = True


class CustomerDTO(CustomerBase):
    pass


class CustomerDTOCreate(CustomerBase):
    username: str
    password: str


class CustomerDTOUpdate(CustomerBase):
    pass
