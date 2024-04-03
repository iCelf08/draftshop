from sqlalchemy.orm import Session
import models
import schemas
import bcrypt
import uuid
from datetime import datetime
from typing import List

# User CRUD functions

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password.decode('utf-8'), first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8'))

def delete_user(db: Session, email: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user

# Product CRUD functions

def get_product(db: Session, id: uuid.UUID):
    return db.query(models.Product).filter(models.Product.id == id).first()

def get_products(db: Session):
    return db.query(models.Product).all()

def add_product(db: Session, product: schemas.ProductAdd):
    db_product = models.Product(name=product.name, price=product.price, brand=product.brand)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, id: uuid.UUID):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return db_product

# Order CRUD functions

def set_order(db: Session, order: schemas.OrderCreate):
    order_info = models.Order(owner_id=order.user_id)
    db.add(order_info)
    db.commit()
    db.refresh(order_info)
    for product_id in order.product_ids:
        if product_id:
            order_product = models.OrderProduct(order_id=order_info.id, product_id=product_id)
            db.add(order_product)
    db.commit()
    return order_info

def delete_order(db: Session, order_id: uuid.UUID):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        return order
    return None
