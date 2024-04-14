from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr
from sqlalchemy import Enum
from enums import PaymentMethodEnum


#User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    
    class Config:
        orm_mode = True

class UserIn(UserBase):#used to retrieve basic user data
    password:str
    
class UserInDbase(UserBase):
    id: uuid.UUID
    
    class config:
        orm_mode = True
        
class UserInDB(UserInDbase):#used to retrieve sensitive user data
    hashed_password: str
        
#Token shemas
class TokenData(BaseModel):
    username : Optional[EmailStr] = None
    
class Token(BaseModel):
    access_token: str 
    token_type: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None 

#Product Schemas
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

    class Config:
        orm_mode = True
        

#Order schemas
class OrderBase(BaseModel):
    shipping_address: str
    payment_method: PaymentMethodEnum

    class Config:
        orm_mode = True
    
class OrderCreate(OrderBase):
    user_id: uuid.UUID
    product_ids: List[uuid.UUID]
    
    class Config:
        orm_mode = True
        
class OrderUpdate(OrderBase):
    
    class Config:
        from_attributes = True
        
#Review Schemas 
class ReviewBase(BaseModel):
    product_id: uuid.UUID
    review_content: str

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(ReviewBase):
    pass

class Review(ReviewBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    review_maker_id: uuid.UUID
    
    class Config:
        orm_mode = True