from typing import List
from pydantic import BaseModel 
import uuid


class UserInfoBase(BaseModel):
    email:str
    fullname:str


class UserCreate(UserInfoBase):
    password:str

class UserUpdate(UserCreate):
    fullname:str
    password:str

class UserInfo(UserInfoBase):
    id:uuid.UUID
    email:str
    password:str
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email:str
    password:str

class ProductInfobase(BaseModel):
    name: str
    price: float
    brand: str
    
class ProductAdd(ProductInfobase):
    pass 

class OrderInfo(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    products: List[uuid.UUID]

    class Config:
        orm_mode = True
        
class OrderSet(BaseModel):
    user_id: uuid.UUID
    product_ids: List[uuid.UUID]

    class Config:
        orm_mode = True
        
class OrderInfoWithProductId(BaseModel):
    user_id: uuid.UUID
    product_ids: List[uuid.UUID]
