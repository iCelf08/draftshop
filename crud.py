from sqlalchemy.orm import Session
import models
import schemas
import bcrypt
import uuid
from datetime import datetime
from typing import List

# User CRUD functions

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

"""                                  ------ My Fisrt Loging with bcrypt.hashpwd ------

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.User(email=user.email, password=hashed_password.decode('utf-8'), first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user"""

"""                                  ----- Login with bcrypt.checkpwd ----- 

def login(db: Session, email: str, password: str):
    db_user = db.query(models.User).filter(models.User.email == email).first()
    if db_user is None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8'))"""

def delete_user_by_id(db: Session, user_id: uuid.UUID):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
    
def update_user(db: Session, username: str, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        for attr, value in vars(user_update).items():
            if value is not None:
                setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

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

def get_order(db: Session, order_id: uuid.UUID):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def set_order(db: Session, order_data: schemas.OrderCreate):
    order_info = models.Order(
        owner_id=order_data.user_id,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method
    )
    db.add(order_info)
    db.commit()
    
    db.refresh(order_info)
    
    for product_id in order_data.product_ids:
        product = db.query(models.Product).filter(models.Product.id == product_id).first()
        if product:
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

def update_order(db: Session, order_id: uuid.UUID, order_update: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        for attr, value in vars(order_update).items():
            if value is not None:
                setattr(db_order, attr, value)
        db.commit()
        db.refresh(db_order)
        return db_order
    return None

# Review CRUD
def create_review(db: Session, review: schemas.ReviewCreate, user_id: uuid.UUID):
    db_review = models.Review(**review.dict(), review_maker_id=user_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_review(db: Session, review_id: uuid.UUID):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def update_review(db: Session, review_id: uuid.UUID, review: schemas.ReviewUpdate):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        for key, value in review.dict().items():
            setattr(db_review, key, value)
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: uuid.UUID):
    db_review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if db_review:
        db.delete(db_review)
        db.commit()
    return db_review