from typing import List
import uuid
from datetime import datetime
from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from schemas import PaymentMethodEnum
from db import Base

from typing import List
import uuid
from datetime import datetime
from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from schemas import PaymentMethodEnum
from db import Base


#UserModel-Table
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)

#Relationships 
    orders = relationship("Order", back_populates="owner")
    reviews = relationship("Review", back_populates="review_maker")  # Back-reference to reviews made by users


#ProductModel-Table
class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    price = Column(Numeric(precision=10, scale=2))
    brand = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

#Relationship
    reviews = relationship("Review", back_populates="product")

#OrderModel-Table
class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, default=uuid.uuid4)
    shipping_address = Column(String) 
    payment_method = Column(Enum(PaymentMethodEnum))
    
#Relationships
    owner = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="order")

#PivoteTable: To assert Order-Product ManytoMany Relationship
class OrderProduct(Base):
    __tablename__ = 'order_product'

    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True, nullable=False)
    
    #Relationships
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product")
    
#ReviewModel-Table
class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    review_content = Column(String)
    review_maker_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    product = relationship("Product", back_populates="reviews")
    review_maker = relationship("User", back_populates="reviews")