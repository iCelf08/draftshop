from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class User(UserBase):
    id: uuid.UUID

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    price: float
    brand: str

class ProductAdd(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

class Product(ProductBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    
    class Config:
        orm_mode = True

class OrderCreate(OrderBase):
    user_id: uuid.UUID
    product_ids: List[uuid.UUID]
    
    class Config:
        orm_mode = True

class OrderUpdate(OrderBase):
    pass

class Order(OrderBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    owner_id: uuid.UUID
    products: List[Product]

    class Config:
        orm_mode = True
