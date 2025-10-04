from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True


class UserDeactivate(BaseModel):
    is_active: bool = False
