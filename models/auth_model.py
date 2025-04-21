from sqlmodel import SQLModel, Field
from pydantic import BaseModel
from typing import Optional


class AuthModel(SQLModel, table=True):
    __tablename__ = "auth"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    is_admin: bool = Field(default=False)
    is_staff: bool = Field(default=False)
    is_active: bool = Field(default=True)
    delete_flg: bool = Field(default=False)


class AuthLoginRequest(BaseModel):
    username: str
    password: str


class AuthLoginResponse(BaseModel):
    access_token: str
