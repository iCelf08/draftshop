from typing import List
import uuid
from datetime import datetime
from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
from db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
    orders = relationship("Order", back_populates="owner")

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    price = Column(Numeric(precision=10, scale=2))
    brand = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True, default=uuid.uuid4)
    
    owner = relationship("User", back_populates="orders")
    products = relationship("Product", secondary="order_product")

class OrderProduct(Base):
    __tablename__ = 'order_product'

    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'), primary_key=True, nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'), primary_key=True, nullable=False)

    order = relationship("Order", backref="order_product")
    product = relationship("Product", backref="order_product")