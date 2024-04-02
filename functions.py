from typing import List
import uuid
from sqlalchemy.orm import Session
import models
import format
import bcrypt

#User Crud functions 

def get_user_by_email(db: Session, email: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == email).first()


def create_user(db: Session, user: format.UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    db_user = models.UserInfo(email=user.email, password=hashed_password.decode('utf-8'), fullname=user.fullname)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_Login(db: Session, email: str, password:str):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()
    if db_user is None:
        return False
    passw = bcrypt.checkpw(password.encode('utf-8'), db_user.password.encode('utf-8')) 
    return passw

    
def delete_user(db: Session, email: str):
    db_user = db.query(models.UserInfo).filter(models.UserInfo.email == email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user

#Product Crud Functions

def get_product(db: Session, id: uuid.UUID):
    return db.query(models.ProductInfo).filter(models.ProductInfo.id == id).first()

def get_products(db : Session):
    return db.query(models.ProductInfo).all()
    

def add_product(db: Session, product: format.ProductInfobase):
    db_product = models.ProductInfo(name=product.name, price=product.price, brand = product.brand)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db:Session, id: uuid.UUID):
    product = db.query(models.ProductInfo).filter(models.ProductInfo.id == id).first()
    if product is None:
        return
    else:
        db.delete(product)
        db.commit()
        return product
    
#Order Crud Functions 


from format import OrderInfoWithProductId

def set_order(db: Session, user_id: uuid.UUID, product_ids: List[uuid.UUID]):
    order = models.OrderInfo(user_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    for product_id in product_ids:
        if product_id is not None:
            order_product = models.OrderProduct(order_id=order.id, product_id=product_id)
            db.add(order_product)
    db.commit()
    
    # Create an instance of OrderInfoWithProductId with user_id and product_ids
    order_info_with_product_id = OrderInfoWithProductId(user_id=user_id, product_ids=product_ids)
    
    # Return a dictionary containing the user_id, product_ids, and products fields
    return {
        "user_id": order_info_with_product_id.user_id,
        "product_ids": order_info_with_product_id.product_ids
      }

def delete_order(db:Session, order_id: uuid.UUID):
    order = db.query(models.OrderInfo).filter(models.OrderInfo.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
        return order
    return None 
    