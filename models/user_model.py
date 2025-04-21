from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .auth_model import AuthModel


class UserModel(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    last_name: str
    first_name: str
    phone_number: str
    email: str
    position: str
    department: str
    delete_flg: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    auth_id: int = Field(foreign_key="auth.id", unique=True)
    auth: AuthModel = Relationship()


class UserBase(BaseModel):
    last_name: str
    first_name: str
    phone_number: str
    email: str
    position: str
    department: str

    class Config:
        from_attributes = True


class UserDTO(UserBase):
    id: int


class UserDTOCreate(UserBase):
    username: str
    password: str


class UserDTOUpdate(UserBase):
    pass
