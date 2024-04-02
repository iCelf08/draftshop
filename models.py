import uuid
from sqlalchemy import Column, Numeric, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship 
from db import Base




class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True)
    password = Column(String)
    fullname = Column(String, unique=True)
    
    orders = relationship("OrderInfo", back_populates="user")

class ProductInfo(Base):
    __tablename__ = "product_info"
    
    id = Column(UUID(as_uuid=True), primary_key=True, index = True, default=uuid.uuid4)
    name = Column(String, unique=True)
    price = Column(Numeric(precision=10, scale=2))
    brand = Column(String)
    

    orders = relationship("OrderInfo", secondary="order_product", back_populates="products",
                          primaryjoin="ProductInfo.id == OrderProduct.product_id",
                          secondaryjoin="OrderProduct.order_id == OrderInfo.id")
    

class OrderInfo(Base):
    __tablename__ = "order_info"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user_info.id'))
    
    user = relationship("UserInfo", back_populates="orders")
    products = relationship("ProductInfo", secondary="order_product", backref="Orders", primaryjoin="OrderInfo.id == OrderProduct.order_id")

class OrderProduct(Base):
    __tablename__ = "order_product"

    order_id = Column(UUID(as_uuid=True), ForeignKey("order_info.id"), primary_key=True)
    product_id = Column(UUID(as_uuid=True), ForeignKey("product_info.id"), primary_key=True)
    